from dataclasses import dataclass
from typing import Dict
import httpx

@dataclass
class ModelSpec:
    name: str
    provider: str
    context_window: int
    max_output: int
    price_input: float  # per 1M tokens
    price_output: float  # per 1M tokens

# API URLs
LITELLM_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
OPENROUTER_URL = "https://openrouter.ai/api/v1/models"

# Cache for fetched models
_models_cache: Dict[str, ModelSpec] = {}

def fetch_litellm_pricing() -> Dict[str, ModelSpec]:
    """Fetch pricing from LiteLLM's community-maintained JSON file."""
    try:
        response = httpx.get(LITELLM_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        models = {}
        for name, info in data.items():
            # Skip entries without pricing info
            if "input_cost_per_token" not in info:
                continue

            # Skip sample/test/fine-tuned models
            if any(x in name.lower() for x in ['sample', 'ft:', 'ft-', 'finetune']):
                continue

            try:
                # Extract provider from litellm_provider field if available, otherwise from model name
                provider = info.get("litellm_provider", "")
                if not provider:
                    # Try to extract from model name (e.g., "openai/gpt-4" -> "openai")
                    if "/" in name:
                        provider = name.split("/")[0]
                    else:
                        provider = "Other"

                # Clean up provider name
                provider = provider.replace("_", " ").replace("-", " ").title()

                models[name] = ModelSpec(
                    name=info.get("litellm_model", name),  # Use display name if available
                    provider=provider,
                    context_window=info.get("max_input_tokens") or info.get("max_tokens", 4096),
                    max_output=info.get("max_output_tokens") or 4096,
                    price_input=round(info.get("input_cost_per_token", 0) * 1_000_000, 4),
                    price_output=round(info.get("output_cost_per_token", 0) * 1_000_000, 4)
                )
            except (ValueError, TypeError, KeyError):
                continue

        return models
    except Exception as e:
        print(f"Error fetching LiteLLM pricing: {e}")
        return {}

def fetch_openrouter_pricing() -> Dict[str, ModelSpec]:
    """Fetch pricing from OpenRouter API."""
    try:
        response = httpx.get(OPENROUTER_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        models = {}
        for m in data.get("data", []):
            try:
                pricing = m.get("pricing", {})
                price_in = float(pricing.get("prompt", 0)) * 1_000_000
                price_out = float(pricing.get("completion", 0)) * 1_000_000

                # Skip free/zero-cost models
                if price_in == 0 and price_out == 0:
                    continue

            except (ValueError, TypeError):
                continue

            model_id = m.get("id", "")

            # Extract provider from model ID (e.g., "openai/gpt-4" -> "Openai")
            if "/" in model_id:
                provider = model_id.split("/")[0].replace("-", " ").replace("_", " ").title()
            else:
                provider = "Other"

            # Get max_output from top_provider if available
            max_output = 4096
            if "top_provider" in m and m["top_provider"]:
                max_output = m["top_provider"].get("max_completion_tokens") or 4096

            models[model_id] = ModelSpec(
                name=m.get("name", model_id),
                provider=provider,
                context_window=m.get("context_length") or 4096,
                max_output=max_output,
                price_input=round(price_in, 4),
                price_output=round(price_out, 4)
            )
        return models
    except Exception as e:
        print(f"Error fetching OpenRouter pricing: {e}")
        return {}

def get_default_models() -> Dict[str, ModelSpec]:
    """Get hardcoded default models as fallback."""
    return {
        # OpenAI
        "gpt-4o": ModelSpec("gpt-4o", "OpenAI", 128000, 16384, 2.50, 10.00),
        "gpt-4o-mini": ModelSpec("gpt-4o-mini", "OpenAI", 128000, 16384, 0.15, 0.60),
        "gpt-4-turbo": ModelSpec("gpt-4-turbo", "OpenAI", 128000, 4096, 10.00, 30.00),
        "gpt-3.5-turbo": ModelSpec("gpt-3.5-turbo", "OpenAI", 16385, 4096, 0.50, 1.50),
        # Anthropic
        "claude-3-5-sonnet-20241022": ModelSpec("claude-3-5-sonnet-20241022", "Anthropic", 200000, 8192, 3.00, 15.00),
        "claude-3-opus-20240229": ModelSpec("claude-3-opus-20240229", "Anthropic", 200000, 4096, 15.00, 75.00),
        "claude-3-haiku-20240307": ModelSpec("claude-3-haiku-20240307", "Anthropic", 200000, 4096, 0.25, 1.25),
        # Google
        "gemini/gemini-1.5-pro": ModelSpec("gemini-1.5-pro", "Google", 2000000, 8192, 1.25, 5.00),
        "gemini/gemini-1.5-flash": ModelSpec("gemini-1.5-flash", "Google", 1000000, 8192, 0.075, 0.30),
    }

def get_models(force_refresh: bool = False) -> Dict[str, ModelSpec]:
    """Get model specifications. Fetches from APIs with fallback to defaults.

    Args:
        force_refresh: If True, bypass cache and fetch fresh data

    Returns:
        Dictionary of model_id -> ModelSpec
    """
    global _models_cache

    # Return cached models if available and not forcing refresh
    if _models_cache and not force_refresh:
        return _models_cache

    # Try fetching from LiteLLM first (more comprehensive)
    models = fetch_litellm_pricing()

    # If LiteLLM failed, try OpenRouter
    if not models:
        models = fetch_openrouter_pricing()

    # If both failed, use defaults
    if not models:
        print("API fetch failed, using default models")
        models = get_default_models()

    # Filter to keep only models with pricing > 0
    models = {k: v for k, v in models.items()
              if v.price_input > 0 or v.price_output > 0}

    # Cache the results
    _models_cache = models

    return models
