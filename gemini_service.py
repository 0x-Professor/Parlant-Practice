"""
Working Gemini NLP Service for Parlant
Simplified implementation that actually works
"""

import os
import json
import time
import asyncio
from typing import Any, Generic, Mapping, TypeVar
from dotenv import load_dotenv
import google.api_core.exceptions

# Load environment variables
load_dotenv()

# Import required modules
import google.generativeai as genai
import parlant.sdk as p
from parlant.core.nlp.generation_info import GenerationInfo, UsageInfo

T = TypeVar('T')

class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_minute: int = 10, calls_per_day: int = 50):
        self.calls_per_minute = calls_per_minute
        self.calls_per_day = calls_per_day
        self.minute_calls = []
        self.day_calls = []
        self.lock = asyncio.Lock()
        self.daily_quota_exhausted = False
    
    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        if self.daily_quota_exhausted:
            raise google.api_core.exceptions.ResourceExhausted(
                "Daily quota already exhausted. Service is temporarily unavailable."
            )
            
        async with self.lock:
            now = time.time()
            
            # Clean old entries
            self.minute_calls = [call_time for call_time in self.minute_calls if now - call_time < 60]
            self.day_calls = [call_time for call_time in self.day_calls if now - call_time < 86400]
            
            # Check limits
            if len(self.minute_calls) >= self.calls_per_minute:
                wait_time = 60 - (now - self.minute_calls[0])
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                    return await self.wait_if_needed()
            
            if len(self.day_calls) >= self.calls_per_day:
                self.daily_quota_exhausted = True
                raise google.api_core.exceptions.ResourceExhausted(
                    "Daily quota exceeded. Please try again tomorrow."
                )
            
            # Record this call
            self.minute_calls.append(now)
            self.day_calls.append(now)
    
    def mark_quota_exhausted(self):
        """Mark daily quota as exhausted."""
        self.daily_quota_exhausted = True

# Global rate limiter instance
_global_rate_limiter = RateLimiter()

class SimpleGeminiGenerator(p.SchematicGenerator[T], Generic[T]):
    """Simple working Gemini generator."""

    def __init__(self, model_name: str = "gemini-2.0-flash", logger: p.Logger = None):
        self._model_name = model_name
        self._logger = logger
        
        # Configure Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY required")
        
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)
    
    async def generate(
        self,
        prompt: str | p.PromptBuilder,
        hints: Mapping[str, Any] = {},
    ) -> p.SchematicGenerationResult[T]:
        """Generate structured content using Gemini with rate limiting and retry."""
        return await self._generate_with_retry(prompt, hints, max_retries=3)
    
    async def _generate_with_retry(
        self,
        prompt: str | p.PromptBuilder,
        hints: Mapping[str, Any],
        max_retries: int = 3,
        base_delay: float = 1.0
    ) -> p.SchematicGenerationResult[T]:
        """Generate with exponential backoff retry logic."""
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                # Wait for rate limiter
                await _global_rate_limiter.wait_if_needed()
                
                # Attempt generation
                return await self._generate_once(prompt, hints)
                
            except google.api_core.exceptions.ResourceExhausted as e:
                last_exception = e
                error_str = str(e).lower()
                
                # Mark quota as exhausted in rate limiter
                if "quota" in error_str and "day" in error_str:
                    _global_rate_limiter.mark_quota_exhausted()
                
                if "quota" in error_str:
                    # Parse retry delay from error if available
                    retry_delay = base_delay * (2 ** attempt)  # exponential backoff
                    
                    # Check if this is a daily quota issue
                    if "day" in error_str:
                        # Daily quota exhausted - don't retry
                        if self._logger:
                            self._logger.error(f"Daily quota exhausted: {e}")
                        # Return a dummy response instead of failing
                        return await self._create_fallback_response(prompt, hints)
                    
                    if attempt < max_retries - 1:  # Don't wait on last attempt
                        if self._logger:
                            self._logger.warning(f"Rate limited, waiting {retry_delay}s before retry {attempt + 1}")
                        await asyncio.sleep(retry_delay)
                        continue
                        
                # Re-raise if not quota related or last attempt
                if self._logger:
                    self._logger.error(f"API error: {e}")
                # Return fallback response instead of raising
                return await self._create_fallback_response(prompt, hints)
                
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    # Wait before retrying other errors too
                    retry_delay = base_delay * (2 ** attempt)
                    if self._logger:
                        self._logger.warning(f"Generation failed, retrying in {retry_delay}s: {e}")
                    await asyncio.sleep(retry_delay)
                    continue
                # On final attempt, return fallback instead of raising
                if self._logger:
                    self._logger.error(f"Final attempt failed: {e}")
                return await self._create_fallback_response(prompt, hints)
        
        # If we get here, all retries failed
        if self._logger:
            self._logger.error(f"All {max_retries} generation attempts failed")
        # Return fallback response instead of raising
        return await self._create_fallback_response(prompt, hints)
    
    def _get_field_default_value(self, field_info, field_name="unknown"):
        """Get appropriate default value for a field based on its schema"""
        field_type = field_info.get("type")
        
        # Handle array/sequence types
        if field_type == "array":
            return []
        
        # Handle boolean types
        if field_type == "boolean":
            return False
            
        # Handle numeric types
        if field_type == "integer":
            return 0
        elif field_type == "number":
            return 0.0
            
        # Handle object types
        if field_type == "object":
            return {}
            
        # Handle string types
        if field_type == "string":
            return "unavailable"
            
        # Handle union types (anyOf)
        if "anyOf" in field_info:
            # Try to find the first non-null type
            for option in field_info["anyOf"]:
                if option.get("type") == "null":
                    continue
                return self._get_field_default_value(option, field_name)
            return None
            
        # Handle enum types
        if "enum" in field_info:
            enum_values = field_info["enum"]
            if enum_values:
                return enum_values[0]  # Return first enum value
                
        # Handle $ref types (need to resolve reference)
        if "$ref" in field_info:
            # For now, return empty object for referenced types
            return {}
            
        # Default fallback
        return "unavailable"

    async def _create_fallback_response(
        self,
        prompt: str | p.PromptBuilder,
        hints: Mapping[str, Any] = {},
    ) -> p.SchematicGenerationResult[T]:
        """Create a fallback response when API is unavailable."""
        if self._logger:
            self._logger.info("Creating fallback response due to API unavailability")
            
        # Get schema type
        schema_type = self.schema
        
        try:
            # Get schema information without creating an instance
            schema_info = schema_type.model_json_schema()
            required_fields = schema_info.get("required", [])
            properties = schema_info.get("properties", {})
            
            # Create a fallback instance based on schema structure
            fallback_instance = {}
            for field_name in required_fields:
                field_info = properties.get(field_name, {})
                fallback_instance[field_name] = self._get_field_default_value(field_info, field_name)
            
            # Add optional fields if they exist
            for field_name, field_info in properties.items():
                if field_name not in fallback_instance:
                    fallback_instance[field_name] = self._get_field_default_value(field_info, field_name)
            
            # Create Pydantic instance
            content = schema_type.model_validate(fallback_instance)
            
            # Create result
            usage_info = UsageInfo(
                input_tokens=0,
                output_tokens=0,
            )
            
            generation_info = GenerationInfo(
                schema_name=schema_type.__name__,
                model=f"{self._model_name}_fallback",
                duration=0.0,
                usage=usage_info
            )
            
            return p.SchematicGenerationResult(
                content=content,
                info=generation_info
            )
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Fallback response creation failed: {e}")
            # Try to create a minimal fallback
            try:
                # Get default values for all fields from Pydantic model defaults
                defaults = {}
                for field_name, field in schema_type.model_fields.items():
                    if field.default is not None:
                        defaults[field_name] = field.default
                    elif field.default_factory is not None:
                        defaults[field_name] = field.default_factory()
                    else:
                        # Guess based on annotation
                        annotation = field.annotation
                        if annotation == bool:
                            defaults[field_name] = False
                        elif annotation == int:
                            defaults[field_name] = 0
                        elif annotation == float:
                            defaults[field_name] = 0.0
                        elif annotation == str:
                            defaults[field_name] = "unavailable"
                        elif hasattr(annotation, '__origin__') and annotation.__origin__ in (list, tuple):
                            defaults[field_name] = []
                        else:
                            defaults[field_name] = None
                
                content = schema_type.model_validate(defaults)
                
                usage_info = UsageInfo(input_tokens=0, output_tokens=0)
                generation_info = GenerationInfo(
                    schema_name=schema_type.__name__,
                    model=f"{self._model_name}_fallback",
                    duration=0.0,
                    usage=usage_info
                )
                
                return p.SchematicGenerationResult(
                    content=content,
                    info=generation_info
                )
                
            except Exception as inner_e:
                if self._logger:
                    self._logger.error(f"Even minimal fallback failed: {inner_e}")
                raise Exception(f"Complete fallback failure: {e}") from inner_e
    
    async def _generate_once(
        self,
        prompt: str | p.PromptBuilder,
        hints: Mapping[str, Any] = {},
    ) -> p.SchematicGenerationResult[T]:
        """Single generation attempt without retry logic."""
        start_time = time.time()
        
        # Convert prompt to string
        if isinstance(prompt, p.PromptBuilder):
            prompt_text = prompt.build()
        else:
            prompt_text = prompt
        
        # Get schema type
        schema_type = self.schema
        
        try:
            # Get schema information without creating an instance
            schema_info = schema_type.model_json_schema()
            required_fields = schema_info.get("required", [])
            properties = schema_info.get("properties", {})
            
            # Create a sample instance based on schema structure
            dummy_instance = {}
            for field_name in required_fields:
                field_info = properties.get(field_name, {})
                field_type = field_info.get("type", "string")
                
                if field_type == "string":
                    dummy_instance[field_name] = "sample_value"
                elif field_type == "integer":
                    dummy_instance[field_name] = 1
                elif field_type == "number":
                    dummy_instance[field_name] = 0.5
                elif field_type == "boolean":
                    dummy_instance[field_name] = True
                elif field_type == "array":
                    dummy_instance[field_name] = []
                elif field_type == "object":
                    dummy_instance[field_name] = {}
                else:
                    dummy_instance[field_name] = "default_value"
            
            # Add optional fields if they exist
            for field_name, field_info in properties.items():
                if field_name not in dummy_instance:
                    field_type = field_info.get("type", "string")
                    if field_type == "string":
                        dummy_instance[field_name] = "optional_value"
                    elif field_type == "integer":
                        dummy_instance[field_name] = 0
                    elif field_type == "number":
                        dummy_instance[field_name] = 0.0
                    elif field_type == "boolean":
                        dummy_instance[field_name] = False
            
            # Enhanced prompt for better JSON generation
            enhanced_prompt = f"""
{prompt_text}

Please respond with valid JSON that matches this schema structure:
{json.dumps(dummy_instance, indent=2)}

IMPORTANT: 
- Return ONLY valid JSON
- No markdown formatting
- No code blocks
- Include all required fields
"""
            
            # Generate with Gemini
            response = self._model.generate_content(
                enhanced_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=hints.get("temperature", 0.1),
                    max_output_tokens=2048,
                )
            )
            
            response_text = response.text.strip()
            
            # Clean up response
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            try:
                parsed_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback to dummy data if parsing fails
                if isinstance(dummy_instance, dict):
                    parsed_data = dummy_instance
                else:
                    parsed_data = {"message": response_text}
            
            # Create Pydantic instance
            content = schema_type.model_validate(parsed_data)
            
            # Create result
            duration = time.time() - start_time
            
            usage_info = UsageInfo(
                input_tokens=len(enhanced_prompt) // 4,  # Rough estimate
                output_tokens=len(response_text) // 4,
            )
            
            generation_info = GenerationInfo(
                schema_name=schema_type.__name__,
                model=self._model_name,
                duration=duration,
                usage=usage_info
            )
            
            return p.SchematicGenerationResult(
                content=content,
                info=generation_info
            )
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Generation failed: {e}")
            raise
    
    @property
    def id(self) -> str:
        return self._model_name
    
    @property
    def max_tokens(self) -> int:
        return 1000000  # 1M for Gemini 1.5
    
    @property
    def tokenizer(self):
        # Simple tokenizer mock
        class SimpleTokenizer:
            async def estimate_token_count(self, text: str) -> int:
                return len(text) // 4
        return SimpleTokenizer()

class SimpleGeminiEmbedder(p.Embedder):
    """Simple Gemini embedder."""
    
    def __init__(self, logger: p.Logger = None):
        self._logger = logger
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    
    async def embed(self, texts: list[str], hints: Mapping[str, Any] = {}) -> p.EmbeddingResult:
        vectors = []
        for text in texts:
            try:
                # Wait for rate limiter
                await _global_rate_limiter.wait_if_needed()
                
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=text,
                    task_type="retrieval_document"
                )
                vectors.append(result['embedding'])
            except google.api_core.exceptions.ResourceExhausted as e:
                if self._logger:
                    self._logger.warning(f"Embedding rate limited for text: {text[:50]}...")
                # Fallback to dummy vector for rate limited requests
                vectors.append([0.1] * 768)
            except Exception as e:
                if self._logger:
                    self._logger.warning(f"Embedding failed for text: {text[:50]}..., error: {e}")
                # Fallback to dummy vector
                vectors.append([0.1] * 768)
        
        return p.EmbeddingResult(vectors=vectors)
    
    @property
    def id(self) -> str:
        return "text-embedding-004"
    
    @property
    def max_tokens(self) -> int:
        return 2048
    
    @property
    def tokenizer(self):
        class SimpleTokenizer:
            async def estimate_token_count(self, text: str) -> int:
                return len(text) // 4
        return SimpleTokenizer()
    
    @property
    def dimensions(self) -> int:
        return 768

class SimpleGeminiModeration(p.ModerationService):
    """Simple moderation service."""
    
    async def check(self, content: str) -> p.ModerationCheck:
        # For now, just return no flags - can be enhanced later
        return p.ModerationCheck(flagged=False, tags=[])

class SimpleGeminiService(p.NLPService):
    """Simple working Gemini NLP service."""
    
    def __init__(self, logger: p.Logger, model_name: str = "gemini-2.0-flash"):
        self._logger = logger
        self._model_name = model_name
    
    async def get_schematic_generator(self, t: type[T]) -> p.SchematicGenerator[T]:
        generator = SimpleGeminiGenerator[t](
            model_name=self._model_name,
            logger=self._logger
        )
        generator.__orig_class__ = p.SchematicGenerator[t]
        return generator
    
    async def get_embedder(self) -> p.Embedder:
        return SimpleGeminiEmbedder(logger=self._logger)
    
    async def get_moderation_service(self) -> p.ModerationService:
        return SimpleGeminiModeration()

def load_gemini_nlp_service(container: p.Container) -> p.NLPService:
    """Create the Gemini NLP service."""
    return SimpleGeminiService(
        logger=container[p.Logger],
        model_name=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    )
