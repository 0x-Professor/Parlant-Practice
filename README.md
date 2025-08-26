# Parlant Healthcare Agent with Google Gemini

A healthcare conversational agent powered by the Parlant framework and Google's Gemini AI models.

## Features

- 🤖 **Google Gemini Integration**: Custom NLP service using Gemini 1.5/2.0 models
- 🏥 **Healthcare Domain**: Pre-configured with healthcare-specific knowledge and terminology
- 💬 **Conversational AI**: Full conversation management and context awareness
- 🔒 **Content Safety**: Built-in moderation using Gemini's safety features
- 🎯 **Vector Embeddings**: Semantic search using Google's text-embedding-004

## Quick Setup

### 1. Get Your Gemini API Key
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Copy the generated key

### 2. Configure Environment
Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-1.5-flash
```

### 3. Install and Run
```bash
# Install dependencies (if not already installed)
pip install -e .

# Run the healthcare agent
python main.py
```

## Project Structure

```
├── main.py                 # Main application entry point
├── gemini_service.py       # Custom Gemini NLP service for Parlant
├── .env                    # Environment variables (API keys)
├── pyproject.toml          # Project dependencies
├── setup_env.py            # Interactive environment setup script
├── setup_gemini_env.ps1    # PowerShell setup script for Windows
└── README.md              # This file
```

## Usage

The application creates a healthcare agent with pre-configured domain knowledge including:
- Office contact information
- Business hours
- Medical specialists (e.g., Charles Xavier/Professor X)
- Healthcare-specific terminology

### Supported Models

- **Text Generation**: `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash-exp`
- **Embeddings**: `text-embedding-004`
- **Context Window**: Up to 1-2M tokens depending on model

### Key Components

1. **GeminiSchematicGenerator**: Handles structured content generation
2. **GeminiEmbedder**: Creates vector embeddings for semantic search
3. **GeminiModerationService**: Content safety and filtering
4. **GeminiNLPService**: Main service coordinator

## Development

### Environment Setup Scripts

**Interactive Python Setup:**
```bash
python setup_env.py
```

**PowerShell Setup (Windows):**
```powershell
.\setup_gemini_env.ps1
```

### Customization

- **Add Domain Terms**: Modify the `add_domain_glossary()` function in `main.py`
- **Adjust Model Settings**: Change the `GEMINI_MODEL` environment variable
- **Custom Prompts**: Edit the prompt generation in `gemini_service.py`

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your `GEMINI_API_KEY` is valid and has quota
2. **Model Availability**: Some models may require special access
3. **Import Errors**: Ensure all dependencies are installed in your environment

### Logs

Check the `parlant-data/parlant.log` file for detailed error information.

## Contributing

This project demonstrates integrating Google Gemini with the Parlant conversational AI framework. Feel free to extend it with additional healthcare features or adapt it for other domains.

## License

MIT License - see LICENSE file for details.
