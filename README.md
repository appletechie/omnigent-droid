# omnigent-droid

[Factory AI's Droid CLI](https://factory.ai) as an [Omnigent](https://github.com/omnigent-ai/omnigent)
harness, driven over the Agent Client Protocol.

Install it and `droid` becomes a selectable harness — no changes to Omnigent itself:

```bash
pip install omnigent-droid
curl -fsSL https://app.factory.ai/cli | sh    # the droid CLI itself
```

```yaml
executor:
  type: omnigent
  config:
    harness: droid
```

## Why this is a separate package

Omnigent 0.4.0 added a harness plugin system so vendor harnesses can ship on
their own release cycle. This package registers through the
`omnigent.community.harness` entry point and mounts under Omnigent's
`omnigent.community.harness.*` namespace; core discovers it at startup and
merges it into the harness registry.

Nothing here patches Omnigent. Uninstalling the package removes the harness.

## What you get

- `droid` as a first-class harness id, with the Droid label in pickers.
- Binary-gated readiness — Omnigent reports Droid unavailable when the `droid`
  CLI isn't on PATH, instead of failing at the first turn.
- Install metadata, so a spec naming `droid` without this package installed
  tells you to `pip install omnigent-droid` rather than erroring opaquely.
- Streaming turns, interrupt (ACP `session/cancel`), and tool approvals routed
  through Omnigent's policy + elicitation gates.

## Auth

Droid's own — a `FACTORY_API_KEY` environment variable, or the CLI's login
flow. This package stores no credential and Omnigent manages none, so auth
problems surface from Droid itself on the first turn.

## Sandboxing

When an agent spec requests OS sandboxing (`os_env.sandbox`), the whole Droid
process tree is wrapped at spawn using Omnigent's platform sandbox
(bubblewrap on Linux, Seatbelt on macOS). When no sandbox is requested, or the
backend is unavailable, Droid launches unwrapped — startup is never blocked on
it.

## Development

```bash
pip install -e ".[dev]"
pytest
```

The suite covers the ACP executor against captured live stream shapes, plus the
plugin contract itself — including running Omnigent's own contribution
validator, so a packaging mistake fails here rather than silently disabling the
harness in someone's install.

## Status

Alpha, and deliberately narrow: it wraps `droid exec --output-format acp` and
nothing else. Droid has no native-TUI surface in Omnigent — this ACP path is
the only one — and community plugins cannot register native terminal harnesses
today.

## License

Apache-2.0, matching Omnigent.
# Testing Polly Webhook Fri Jul 31 06:16:37 PDT 2026
# Test 1785504173
# Test 1785504261
# Test 1785504290
# Final test 1785504326
# Test with ID token exchange 1785504436
# Test with cloud-platform scope 1785504455
# Test with new secret 1785504778
# Debug logging test 1785504802
# Token format test 1785504831
# Using external omnigent URL 1785504926
# Polly webhook live test 2026-08-01T00:45:57Z
