from dataclasses import dataclass
from typing import Dict
import json
import os

@dataclass
class ModelSpec:
    name: str
    provider: str
    context_window: int
    max_output: int
    price_input: float  # per 1M tokens
    price_output: float  # per 1M tokens

def get_models() -> Dict[str, ModelSpec]:
    """Get model specifications. Updates from API or local cache."""
    models_file = "models.json"
    
    # Try to load from file, otherwise use defaults
    if os.path.exists(models_file):
        try:
            with open(models_file, 'r') as f:
                data = json.load(f)
                return {k: ModelSpec(**v) for k, v in data.items()}
        except:
            pass
    
    # Default models (latest as of 2024-2025)
    defaults = {
        # OpenAI - Latest
        "gpt-5.2": ModelSpec("GPT-5.2", "OpenAI", 400000, 128000, 1.75, 14.00),
        "gpt-5.2-pro": ModelSpec("GPT-5.2 Pro", "OpenAI", 400000, 128000, 21.00, 168.00),
        "gpt-4o": ModelSpec("GPT-4o", "OpenAI", 128000, 16384, 2.50, 10.00),
        "gpt-4o-mini": ModelSpec("GPT-4o Mini", "OpenAI", 128000, 16384, 0.15, 0.60),
        "gpt-4-turbo": ModelSpec("GPT-4 Turbo", "OpenAI", 128000, 4096, 10.00, 30.00),
        "gpt-3.5-turbo": ModelSpec("GPT-3.5 Turbo", "OpenAI", 16385, 4096, 0.50, 1.50),
        "gpt-4": ModelSpec("GPT-4", "OpenAI", 8192, 4096, 30.00, 60.00),
        # Azure OpenAI (same models, typically same pricing)
        "azure-gpt-4o": ModelSpec("Azure GPT-4o", "Azure OpenAI", 128000, 16384, 2.50, 10.00),
        "azure-gpt-4-turbo": ModelSpec("Azure GPT-4 Turbo", "Azure OpenAI", 128000, 4096, 10.00, 30.00),
        "azure-gpt-35-turbo": ModelSpec("Azure GPT-3.5 Turbo", "Azure OpenAI", 16385, 4096, 0.50, 1.50),
        # Anthropic - Latest
        "claude-opus-4.5": ModelSpec("Claude Opus 4.5", "Anthropic", 200000, 64000, 5.00, 25.00),
        "claude-opus-4": ModelSpec("Claude Opus 4", "Anthropic", 200000, 32000, 5.00, 25.00),
        "claude-sonnet-4": ModelSpec("Claude Sonnet 4", "Anthropic", 200000, 32000, 3.00, 15.00),
        "claude-haiku-3": ModelSpec("Claude Haiku 3", "Anthropic", 200000, 32000, 0.25, 1.25),
        "claude-3-opus": ModelSpec("Claude 3 Opus", "Anthropic", 200000, 4096, 15.00, 75.00),
        "claude-3-sonnet": ModelSpec("Claude 3 Sonnet", "Anthropic", 200000, 4096, 3.00, 15.00),
        "claude-3-haiku": ModelSpec("Claude 3 Haiku", "Anthropic", 200000, 4096, 0.25, 1.25),
        # Google Gemini - Latest
        "gemini-3-flash": ModelSpec("Gemini 3 Flash", "Google", 1000000, 8192, 0.50, 3.00),
        "gemini-3-pro": ModelSpec("Gemini 3 Pro", "Google", 1000000, 8192, 1.50, 6.00),
        "gemini-2.0-flash": ModelSpec("Gemini 2.0 Flash", "Google", 1000000, 8192, 0.075, 0.30),
        "gemini-2.0-pro": ModelSpec("Gemini 2.0 Pro", "Google", 1000000, 8192, 0.50, 1.50),
        "gemini-1.5-pro": ModelSpec("Gemini 1.5 Pro", "Google", 2000000, 8192, 1.25, 5.00),
        "gemini-1.5-flash": ModelSpec("Gemini 1.5 Flash", "Google", 1000000, 8192, 0.075, 0.30),
        # AWS Bedrock
        "bedrock-claude-opus": ModelSpec("Bedrock Claude Opus", "AWS Bedrock", 200000, 4096, 15.00, 75.00),
        "bedrock-claude-sonnet": ModelSpec("Bedrock Claude Sonnet", "AWS Bedrock", 200000, 4096, 3.00, 15.00),
        "bedrock-claude-haiku": ModelSpec("Bedrock Claude Haiku", "AWS Bedrock", 200000, 4096, 0.25, 1.25),
        "bedrock-llama-3-70b": ModelSpec("Bedrock Llama 3 70B", "AWS Bedrock", 131072, 4096, 0.65, 0.65),
        "bedrock-llama-3-8b": ModelSpec("Bedrock Llama 3 8B", "AWS Bedrock", 131072, 4096, 0.05, 0.05),
        "bedrock-titan-text": ModelSpec("Bedrock Titan Text", "AWS Bedrock", 8000, 4096, 0.80, 0.80),
        # Meta Llama
        "llama-3-70b": ModelSpec("Llama 3 70B", "Meta", 131072, 4096, 0.65, 0.65),
        "llama-3-8b": ModelSpec("Llama 3 8B", "Meta", 131072, 4096, 0.05, 0.05),
    }
    
    # Save defaults to file
    with open(models_file, 'w') as f:
        json.dump({k: {
            "name": v.name,
            "provider": v.provider,
            "context_window": v.context_window,
            "max_output": v.max_output,
            "price_input": v.price_input,
            "price_output": v.price_output
        } for k, v in defaults.items()}, f, indent=2)
    
    return defaults

def update_models_from_api():
    """Fetch latest model specs from APIs. Placeholder for future implementation."""
    # TODO: Implement API fetching from:
    # - OpenAI API pricing endpoint
    # - Anthropic pricing page
    # - Google Cloud pricing API
    # - AWS Bedrock pricing API
    pass