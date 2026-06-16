# API reference

The full, machine-readable reference for the REST Hook API is **generated from the Rust
handlers** (via [utoipa](https://github.com/juhaku/utoipa)) and committed as
[`openapi.json`](./openapi.json), so it can never drift from the running code.

<p style="margin:1.5rem 0;">
  <a class="api-ref-button" href="./openapi.html">Open the API reference →</a>
</p>

You can also import [`openapi.json`](./openapi.json) straight into Postman, Insomnia, or any
OpenAPI client, or generate a client from it.

Prefer prose? The [Endpoints](./endpoints.md) page walks through each call with `curl`
examples.

<style>
.api-ref-button {
  display: inline-block;
  font-weight: 600;
  padding: 12px 22px;
  border-radius: 7px;
  background: #c4a7e7;
  color: #232136 !important;
  text-decoration: none;
}
.api-ref-button:hover { filter: brightness(1.06); }
</style>
