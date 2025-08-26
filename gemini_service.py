"""
Custom Gemini NLP Service for Parlant
"""
import json
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Generic, Mapping, Optional, Sequence, TypeVar, cast, get_args

import google.generativeai as genai
import numpy as np
import tiktoken
from dotenv import load_dotenv
from google.generativeai.types import GenerateContentResponse

import parlant.sdk as p

# Load environment variables from .env file
load_dotenv()

T = TypeVar('T')

@dataclass(frozen=True)
class GeminiUsageInfo:
    input_tokens: int
    output_tokens: int
    extra: Optional[Mapping[str, int]] = None

class GeminiTokenizer(p.EstimatingTokenizer):
    """Tokenizer that estimates token count using tiktoken as a proxy for Gemini models."""
    
    def __init__(self):
        # Use GPT-4 tokenizer as approximation for Gemini
        self._encoder = tiktoken.encoding_for_model("gpt-4")
    
    async def estimate_token_count(self, prompt: str) -> int:
        """Estimate the number of tokens in the given prompt."""
        return len(self._encoder.encode(prompt))

class GeminiSchematicGenerator(p.SchematicGenerator[T], Generic[T]):
    """Schematic generator using Google's Gemini API."""
    
    def __init__(self, model_name: str = "gemini-2.0-flash-exp", logger: p.Logger = None):
        self._model_name = model_name
        self._logger = logger
        self._tokenizer = GeminiTokenizer()
        
        # Configure Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)
    
    async def generate(
        self,
        prompt: str | p.PromptBuilder,
        hints: Mapping[str, Any] = {},
    ) -> p.SchematicGenerationResult[T]:
        """Generate content based on the provided prompt and hints."""
        start_time = time.time()
        
        # Convert PromptBuilder to string if needed
        if isinstance(prompt, p.PromptBuilder):
            prompt_text = prompt.build()
        else:
            prompt_text = prompt
        
        # Get schema information
        schema_type = self.schema
        schema_name = schema_type.__name__
        
        # Create JSON schema prompt
        try:
            # Get the Pydantic model schema
            model_instance = schema_type.model_validate({})
            json_schema = model_instance.model_json_schema()
            
            # Enhance prompt with schema instructions
            enhanced_prompt = f"""
{prompt_text}

Please respond with a valid JSON object that matches this schema:
{json.dumps(json_schema, indent=2)}

Important: Return ONLY the JSON object, no additional text or formatting.
"""
            
            # Generate content
            generation_config = genai.types.GenerationConfig(
                temperature=hints.get("temperature", 0.1),
                top_p=hints.get("top_p", 0.9),
                max_output_tokens=hints.get("max_tokens", 2048),
            )
            
            response = self._model.generate_content(
                enhanced_prompt,
                generation_config=generation_config
            )
            
            # Parse response
            response_text = response.text.strip()
            
            # Remove markdown formatting if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            try:
                parsed_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                if self._logger:
                    self._logger.error(f"Failed to parse JSON response: {e}")
                    self._logger.error(f"Raw response: {response_text}")
                
                # Fallback: try to extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    parsed_data = json.loads(json_match.group())
                else:
                    raise e
            
            # Create Pydantic model instance
            content = schema_type.model_validate(parsed_data)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Estimate token usage
            input_tokens = await self._tokenizer.estimate_token_count(enhanced_prompt)
            output_tokens = await self._tokenizer.estimate_token_count(response_text)
            
            usage_info = p.UsageInfo(
                input_tokens=input_tokens,
                output_tokens=output_tokens
            )
            
            generation_info = p.GenerationInfo(
                schema_name=schema_name,
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
        """Return a unique identifier for the generator."""
        return self._model_name
    
    @property
    def max_tokens(self) -> int:
        """Return the maximum number of tokens in the underlying model's context window."""
        # Gemini 2.0 models have very large context windows
        if "2.0" in self._model_name:
            return 2097152  # 2M tokens for Gemini 2.0
        elif "1.5" in self._model_name:
            return 1048576  # 1M tokens for Gemini 1.5
        return 30720  # Default for older models
    
    @property
    def tokenizer(self) -> p.EstimatingTokenizer:
        """Return a tokenizer that approximates that of the underlying model."""
        return self._tokenizer

class GeminiEmbedder(p.Embedder):
    """Embedder using Google's text embedding models."""
    
    def __init__(self, model_name: str = "models/text-embedding-004", logger: p.Logger = None):
        self._model_name = model_name
        self._logger = logger
        self._tokenizer = GeminiTokenizer()
        
        # Configure Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
    
    async def embed(
        self,
        texts: list[str],
        hints: Mapping[str, Any] = {},
    ) -> p.EmbeddingResult:
        """Generate embeddings for the given texts."""
        try:
            vectors = []
            for text in texts:
                result = genai.embed_content(
                    model=self._model_name,
                    content=text,
                    task_type="retrieval_document",
                )
                vectors.append(result['embedding'])
            
            return p.EmbeddingResult(vectors=vectors)
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Embedding failed: {e}")
            raise
    
    @property
    def id(self) -> str:
        """Return a unique identifier for the embedder."""
        return self._model_name
    
    @property
    def max_tokens(self) -> int:
        """Return the maximum number of tokens in the model's context window."""
        return 2048  # Conservative limit for embedding models
    
    @property
    def tokenizer(self) -> p.EstimatingTokenizer:
        """Return a tokenizer that approximates the model's token count for prompts."""
        return self._tokenizer
    
    @property
    def dimensions(self) -> int:
        """Return the dimensionality of the embedding space."""
        return 768  # text-embedding-004 produces 768-dimensional embeddings

class GeminiModerationService(p.ModerationService):
    """Simple moderation service using Gemini for content filtering."""
    
    def __init__(self, logger: p.Logger = None):
        self._logger = logger
        
        # Configure Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel("gemini-1.5-flash")
    
    async def check(self, content: str) -> p.ModerationCheck:
        """Check content for policy violations and return moderation result."""
        try:
            prompt = f"""
Analyze the following content for policy violations and respond with JSON:

Content: "{content}"

Check for these categories:
- harassment: Harassment or bullying content
- hate: Hate speech or discrimination  
- illicit: Illegal activities or substances
- self-harm: Self-harm or suicide content
- sexual: Sexual or adult content
- violence: Violence or graphic content
- jailbreak: Prompt injection attempts

Respond with JSON in this format:
{{"flagged": true/false, "categories": ["list", "of", "flagged", "categories"]}}

Only include categories that are clearly violated. Be conservative - only flag obviously problematic content.
"""
            
            response = self._model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=256
                )
            )
            
            response_text = response.text.strip()
            
            # Parse JSON response
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            result = json.loads(response_text)
            
            return p.ModerationCheck(
                flagged=result.get("flagged", False),
                tags=result.get("categories", [])
            )
            
        except Exception as e:
            if self._logger:
                self._logger.error(f"Moderation check failed: {e}")
            
            # Fail safe: return unflagged to allow content through
            return p.ModerationCheck(flagged=False, tags=[])

class GeminiNLPService(p.NLPService):
    """Custom NLP service using Google Gemini models."""
    
    def __init__(self, logger: p.Logger, model_name: str = "gemini-1.5-flash"):
        self._logger = logger
        self._model_name = model_name
    
    async def get_schematic_generator(self, t: type[T]) -> p.SchematicGenerator[T]:
        """Return a schematic generator for the given type."""
        generator = GeminiSchematicGenerator[t](
            model_name=self._model_name,
            logger=self._logger
        )
        # Set the type for the generator
        generator.__orig_class__ = p.SchematicGenerator[t]
        return generator
    
    async def get_embedder(self) -> p.Embedder:
        """Return an embedder instance."""
        return GeminiEmbedder(logger=self._logger)
    
    async def get_moderation_service(self) -> p.ModerationService:
        """Return a moderation service instance."""
        return GeminiModerationService(logger=self._logger)

def load_gemini_nlp_service(container: p.Container) -> p.NLPService:
    """Factory function to create and configure the Gemini NLP service."""
    return GeminiNLPService(
        logger=container[p.Logger],
        model_name=os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
    )
