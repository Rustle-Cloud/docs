# Receiving & verifying events

Rustle delivers each event as an HTTPS `POST` to your hook's `target_url`. This page covers
how to receive it safely.

## The request

```http
POST /your/webhook HTTP/1.1
Content-Type: application/json
x-radar-event-id: 6f1c…
x-radar-signature: sha256=9a0b…
```

Respond `2xx` to acknowledge. Anything else (or a timeout) is treated as a failure and
retried with exponential backoff; exhausted retries go to a dead-letter queue, never a
silent drop.

## Two things to do on every request

1. **Verify `x-radar-signature`**: prove the body really came from Rustle (below).
2. **[Dedupe on `x-radar-event-id`](../concepts/exactly-once.md)**: delivery is at-least-once.

## Verifying the signature

The signature is **HMAC-SHA256 over the exact raw body bytes**, using your hook's signing
secret (returned once when you [created the hook](../api/endpoints.md#post-apiv1hooks)). The
header value format is:

```text
x-radar-signature: sha256=<lowercase hex digest>
```

> **Verify against the raw bytes**, before any JSON parse-and-re-serialize. Re-stringifying
> the parsed JSON can change whitespace or key order and break the signature. Most frameworks
> expose the raw body (e.g. a `rawBody` buffer); use that.

### Node.js

```js
const crypto = require("crypto");

function verify(secret, rawBody, header) {
  const expected =
    "sha256=" + crypto.createHmac("sha256", secret).update(rawBody).digest("hex");
  const a = Buffer.from(header || "");
  const b = Buffer.from(expected);
  return a.length === b.length && crypto.timingSafeEqual(a, b); // constant-time
}
```

### Python

```python
import hmac, hashlib

def verify(secret: str, raw_body: bytes, header: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header or "")  # constant-time
```

### Rust

Rustle signs with the same routine it ships for verification, `radar_dispatch::sign::verify`:

```rust
use hmac::{Hmac, Mac};
use sha2::Sha256;

pub fn verify(secret: &str, body: &[u8], header_value: &str) -> bool {
    let Some(hex_tag) = header_value.strip_prefix("sha256=") else { return false };
    let Some(tag) = hex::decode(hex_tag).ok() else { return false };
    let mut mac = Hmac::<Sha256>::new_from_slice(secret.as_bytes()).unwrap();
    mac.update(body);
    mac.verify_slice(&tag).is_ok() // constant-time
}
```

If verification fails, reject the request (`401`) and do not process the body.

## A minimal receiver

```python
@app.post("/webhooks/rustle")
def receive():
    raw = request.get_data()  # raw bytes — do not use request.json here
    if not verify(SECRET, raw, request.headers.get("x-radar-signature", "")):
        return "", 401
    event_id = request.headers["x-radar-event-id"]
    if already_processed(event_id):     # idempotency
        return "", 200
    handle(request.get_json())
    mark_processed(event_id)
    return "", 200
```
