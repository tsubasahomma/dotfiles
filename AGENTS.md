# Agent Instructions

Start with the portable contract index at
[docs/agent-context/README.md](docs/agent-context/README.md).

If a consumer-owned local extension exists under `docs/project/**`, read the
relevant local files after the portable contracts. Local extension files may add
repository-specific identity, surfaces, commands, workflow exceptions, and policy
details.

Keep portable contract files free of repository identity, host details, personal
identifiers, secrets, vendor-specific baseline assumptions, and local operational
facts. Put those details in the project extension instead.
