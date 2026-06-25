# client.account

Account utilities.

## get_credits

```python
credits = client.account.get_credits()
print(credits.remaining)
```

**Returns:** `Credits`  
**Endpoint:** `GET /api/v1/generate/credit`

Synchronous — no task, no webhook.

The API may return credits as a plain integer or a dict with `creditsRemaining`; the SDK normalizes both.

## See also

- [Models](../models.md) — `Credits`
