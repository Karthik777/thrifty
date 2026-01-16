# AI Cost Calculator

A web application for calculating AI/LLM costs across multiple providers (OpenAI, Anthropic, Google, Azure, AWS Bedrock, etc.) with support for multiple agents, iterations, and dynamic context windows.

## Features

- **Multi-Provider Support**: OpenAI, Anthropic, Google Gemini, Azure OpenAI, AWS Bedrock, and more
- **Dynamic Model Selection**: Context windows and pricing automatically update based on selected model
- **Flexible Configuration**: Adjust number of agents, iterations, input/output tokens
- **Real-time Calculation**: Instant cost estimates as you adjust parameters
- **Export Results**: Export calculations as CSV or JSON
- **Clean UI**: Built with FastHTML and MonsterUI for a modern, responsive interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Then open your browser to `http://localhost:5000`

## Model Updates

Model specifications are stored in `models.json`. To update with latest pricing:

1. Edit `models.json` directly, or
2. Implement API fetching in `models.py`'s `update_models_from_api()` function

## Project Structure

- `main.py` - FastHTML application with UI and calculation logic
- `models.py` - Model specifications and data management
- `models.json` - Model data cache (auto-generated)

## License

MIT