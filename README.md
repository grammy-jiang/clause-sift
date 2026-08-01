# ClauseSift

ClauseSift is an accuracy-first evidence retrieval engine for engineering
standards, codes, design guidelines, technical manuals, and product
specifications.

The project uses an offline knowledge-base build pipeline and a lightweight,
read-only runtime exposed through Python, CLI, and MCP interfaces.

## Design

The initial architecture and quality requirements are documented in
[`docs/design.md`](docs/design.md).

## Development

Documentation quality checks are configured through `pre-commit` and GitHub
Actions. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup and usage.
