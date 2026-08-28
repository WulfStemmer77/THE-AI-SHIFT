# Krea media adapter

Use Krea as an optional execution provider for brand-governed images, videos, enhancement, upscaling, trained styles, and multi-step workflows. The brand package remains authoritative; Krea-specific parameters belong in the execution request and run record.

## Connection profiles

### MCP with OAuth — preferred for interactive agent use

- Transport: Streamable HTTP
- Server: `https://api.krea.ai/mcp`
- Authentication: OAuth through the client
- Billing: compute units from the workspace selected during consent

Do not claim Krea is connected merely because the server URL is configured. Perform a harmless authenticated discovery/status call first. If the tool returns Connect, Reconnect, or an authorization request, stop and let the user complete it.

### Direct API — for managed server runtimes

- Base URL: `https://api.krea.ai/`
- Authentication: bearer token from the deployment secret store
- Billing: the workspace API balance

Never place a real token in prompts, `brand-source.json`, media requests, logs, generated artifacts, Git, or MCP configuration committed to a repository.

## Credential and tenant isolation

The adapter is generic and must not be primed with any individual's account or credentials.

- Resolve OAuth sessions through the current host/client at execution time.
- Resolve API tokens through the current tenant's secret store at execution time.
- Never fall back to a remembered personal session, default account, email address, or hard-coded workspace.
- Ask the executing user/tenant to select or confirm the workspace when the connection exposes more than one.
- Store only an opaque tenant-local `workspace_reference`; never store an email, username, token, cookie, OAuth artifact, or credential identifier that is meaningful outside that tenant.
- A successful connection in one environment says nothing about another environment. Run the harmless authenticated preflight separately for every deployment and session that requires it.

The request contract enforces `credential_binding: runtime-injected`. Any personal/default/static binding must fail before execution.

## Live discovery is mandatory

Before each production run, discover the currently available Krea operation and its schema. Do not rely on a remembered model list: models, parameter sets, and deprecations change. Pin the selected `model_id` or `workflow_id` and record a schema snapshot identifier/time in the run manifest.

Krea currently exposes operations for image/video generation, enhancement/upscaling, trained styles, and workflows. Only request a capability returned by the live connection.

## Request construction

Create a request conforming to `schema/krea-media-request.schema.json` and validate it:

```bash
python scripts/validate_media_request.py path/to/krea-media-request.json
```

Map the brand package into Krea as follows:

| Brand contract | Krea request |
| --- | --- |
| allowed imagery | positive subject/style direction |
| forbidden imagery | explicit exclusions/negative direction |
| composition | camera, framing, hierarchy, subject placement |
| colors | palette direction; do not request fake logos or text |
| formats | aspect ratio and intended output dimensions |
| people policy | identity, releases, recognisability constraints |
| disclosure policy | downstream review and labelling decision |

Use an approved Krea trained style only when its workspace asset ID and ownership are known. A textual claim such as “use our style” is not sufficient.

## Execution gates

1. Brand package validation is `PASS`.
2. Krea connection and workspace are verified.
3. Current tool/model schema is discovered.
4. Input assets and rights are recorded.
5. Credit spending and maximum attempts are explicitly authorized.
6. Request validator returns `PASS`.

Do not retry indefinitely. Use the request's `max_attempts`; after that, return the failed candidates and require human direction.

## Output and provenance

For every candidate retain:

- Krea job ID and operation
- connection profile and workspace reference without secrets
- model/workflow/style IDs
- normalized request and prompt hash
- input asset IDs/hashes
- timestamps and status
- result URLs/references and downloaded file hashes
- human selection/rejection and reason

Inspect each candidate at full size for brand alignment, text/data hallucinations, people/rights issues, unintended logos/watermarks, crop suitability, and disclosure requirements. Krea success means the job completed; it does not mean the asset passed brand or legal review.

## Official documentation

- MCP: https://www.krea.ai/docs/developers/mcp
- API reference: https://www.krea.ai/docs/api-reference/introduction
- API keys/billing: https://www.krea.ai/docs/developers/api-keys-and-billing
- Deprecations: https://www.krea.ai/docs/developers/deprecations
