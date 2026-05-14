"""Key hierarchy: user keys override owner defaults."""

from app.config import settings
from app.db.client import get_supabase_client
from app.models.api_keys import Provider
from app.utils.encryption import decrypt_api_key


class APIKeys:
    """API keys with provider and key mapping."""

    def __init__(
        self,
        anthropic_key: str | None = None,
        openai_key: str | None = None,
        openrouter_key: str | None = None,
    ):
        """
        Initialize API keys.

        Args:
            anthropic_key: Anthropic API key
            openai_key: OpenAI API key
            openrouter_key: OpenRouter API key
        """
        self.anthropic_key = anthropic_key
        self.openai_key = openai_key
        self.openrouter_key = openrouter_key

    def get_key(self, provider: Provider) -> str | None:
        """
        Get API key for a provider.

        Args:
            provider: Provider name

        Returns:
            API key or None if not set
        """
        if provider == "anthropic":
            return self.anthropic_key
        elif provider == "openai":
            return self.openai_key
        elif provider == "openrouter":
            return self.openrouter_key
        return None


async def get_api_keys(user_id: str) -> APIKeys:
    """
    Get API keys for a user with fallback to owner defaults.

    Hierarchy:
    1. User's saved keys (if present)
    2. Owner's default keys from settings

    Args:
        user_id: User ID to fetch keys for

    Returns:
        APIKeys object with resolved keys
    """
    # Start with owner defaults
    keys = APIKeys(
        anthropic_key=settings.anthropic_api_key,
        openai_key=settings.openai_api_key,
        openrouter_key=settings.openrouter_api_key,  # Load from environment
    )

    # Fetch user keys from database
    supabase = get_supabase_client()

    try:
        response = (
            supabase.table("user_api_keys")
            .select("provider, encrypted_key")
            .eq("user_id", user_id)
            .execute()
        )

        # Override defaults with user keys
        if response.data:
            for row in response.data:
                provider = row["provider"]
                encrypted_key = row["encrypted_key"]

                # Decrypt the key
                decrypted_key = decrypt_api_key(encrypted_key)

                # Override default with user key
                if provider == "anthropic":
                    keys.anthropic_key = decrypted_key
                elif provider == "openai":
                    keys.openai_key = decrypted_key
                elif provider == "openrouter":
                    keys.openrouter_key = decrypted_key

    except Exception as e:
        # Log error but continue with defaults
        print(f"[KEY_HIERARCHY] Failed to fetch user keys for {user_id}: {e}")
        print("[KEY_HIERARCHY] Falling back to owner defaults")

    return keys
