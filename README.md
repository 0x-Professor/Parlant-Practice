# Parlant with Gemini Integration

This project demonstrates how to use Google's Gemini AI models with the Parlant agent development framework.

## Setup

1. **Get a Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the API key

2. **Set Environment Variables**
   
   On Windows (PowerShell):
   ```powershell
   $env:GEMINI_API_KEY = "your-api-key-here"
   $env:GEMINI_MODEL = "gemini-1.5-flash"  # Optional, defaults to gemini-1.5-flash
   ```
   
   Or create a `.env` file in this directory:
   ```
   GEMINI_API_KEY=your-api-key-here
   GEMINI_MODEL=gemini-1.5-flash
   ```

3. **Install Dependencies**
   
   The dependencies are already configured in `pyproject.toml`. The virtual environment should be set up automatically.

## Features

This implementation provides:

- **Custom Gemini Schematic Generator**: Uses Gemini models to generate structured JSON responses
- **Gemini Embeddings**: Uses Google's text-embedding-004 model for vector embeddings  
- **Gemini Moderation**: Uses Gemini for content moderation and safety filtering
- **Token Estimation**: Uses tiktoken as a proxy for token counting

## Supported Models

- **Text Generation**: gemini-1.5-flash, gemini-1.5-pro, gemini-pro
- **Embeddings**: text-embedding-004
- **Context Length**: Up to 1M tokens for Gemini 1.5 models

## Usage

Run the example:
```bash
python main.py
```

The script will create a healthcare agent with domain-specific terms and demonstrate the Gemini integration.

## File Structure

- `main.py` - Main application entry point
- `gemini_service.py` - Custom Gemini NLP service implementation
- `pyproject.toml` - Project dependencies
- `parlant-data/` - Parlant's data directory (auto-created)

## Custom NLP Service Components

1. **GeminiSchematicGenerator**: Generates structured Pydantic models from prompts
2. **GeminiEmbedder**: Creates vector embeddings for semantic search
3. **GeminiModerationService**: Filters harmful content
4. **GeminiNLPService**: Main service class that coordinates all components

## Notes

- The implementation uses tiktoken for token estimation as Gemini doesn't provide exact token counts
- JSON schema generation is enhanced with detailed prompts to improve structured output quality
- Moderation uses Gemini itself to classify potentially harmful content
- All components include proper error handling and logging
