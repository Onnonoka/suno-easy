from ..models import Credits


class AccountResource:
    """Resource manager for account-related endpoints."""

    def __init__(self, client):
        self.client = client

    def get_credits(self) -> Credits:
        """Return the number of credits remaining on the account."""
        response = self.client.get("/api/v1/generate/credit")
        return Credits.from_api_data(response["data"])
