# Authentication

The REST Hook API is authenticated with an **API token**. Issue one in the console at
[app.rustle.cloud](https://app.rustle.cloud) → **Integrations**.

- Tokens look like `rsk_…` and are shown **once**, when created. Store the value securely.
- A token is scoped to the account that created it. Every call is automatically limited to
  that account's hooks. One account's token can never see or touch another's.
- Tokens are stored **only as a SHA-256 hash** server-side; Rustle can verify a token but
  never reproduce it. Lost it? Revoke it and issue a new one.
- Revoke a token any time from the same Integrations page.

## Presenting the token

Send it as either header (both are accepted):

```http
Authorization: Bearer rsk_your_token
```
```http
X-API-Key: rsk_your_token
```

A missing or invalid token returns `401`.

```bash
curl https://app.rustle.cloud/api/v1/hooks \
  -H "Authorization: Bearer rsk_your_token"
```

> **Base URL:** `https://app.rustle.cloud`. All endpoints below are under `/api/v1`.

The signing **secret** returned when you create a hook is a *different* credential: it is
not an API token, and is used only to [verify webhook signatures](../webhooks/signatures.md).
