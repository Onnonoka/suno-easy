"""Shared constants for the Suno API client."""

# Placeholder required by the Suno API when using polling-only workflows.
# Point ``callback_url`` to your own endpoint when handling webhooks.
DEFAULT_CALLBACK_URL = "https://example.com/suno-callback"

# File upload API uses a separate host (temporary storage, 3-day retention).
DEFAULT_UPLOAD_BASE_URL = "https://sunoapiorg.redpandaai.co"
