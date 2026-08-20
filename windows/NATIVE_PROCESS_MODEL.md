# Native Windows process model

## Always running

- `Neo4j` Windows service on localhost ports 7474 and 7687.

## Started by Kiro

- `.venv\Scripts\python.exe -m knowledge_plane.server --transport stdio`
- No MCP listening port is needed for normal Kiro use.

## On demand or scheduled

- `knowledge-plane-validate`
- `knowledge-plane-ingest`
- `openwiki code --update --print`
- `mkdocs serve` or `mkdocs build`

## Not required

- Docker Desktop
- Docker Engine
- Docker Compose
- Podman
- WSL
- Kubernetes
