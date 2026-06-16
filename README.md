# Rustle docs

The source for the [Rustle](https://rustle.cloud) developer documentation, published at
**[docs.rustle.cloud](https://docs.rustle.cloud)**.

Built with [mdBook](https://rust-lang.github.io/mdBook/). The REST Hook API reference is an
[OpenAPI](./src/api/openapi.json) spec generated from the product's Rust handlers and
rendered with [Redoc](https://github.com/Redocly/redoc).

## Develop locally

```bash
mdbook serve   # live-reload at http://localhost:3000
mdbook build   # output to ./book
```

## Layout

- `src/` — the pages (`SUMMARY.md` is the table of contents)
- `src/api/openapi.json` — the generated API spec (regenerated in the product repo via
  `scripts/gen-openapi.sh`; do not edit by hand)
- `theme/rustle.css` — the Rosé Pine brand tint

## Deploy

Pushing to `main` builds and publishes to GitHub Pages via
[`.github/workflows/docs.yml`](./.github/workflows/docs.yml).

## License

[MIT](./LICENSE). The code examples are yours to copy freely; the "Rustle" name and logo are
trademarks and are not licensed.
