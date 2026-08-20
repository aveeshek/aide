from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables and `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    knowledge_root: Path = Path(".")
    canonical_dir: str = "wiki"
    openwiki_dir: str = "openwiki"
    generated_dir: str = "generated"
    operations_dir: str = "operations"

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "change-me-now"
    neo4j_database: str = "neo4j"

    graph_group_id: str = "engineering-knowledge"
    enable_graphiti: bool = False
    max_graph_depth: int = Field(default=3, ge=1, le=5)
    max_search_results: int = Field(default=12, ge=1, le=50)

    mcp_transport: str = "stdio"
    mcp_host: str = "127.0.0.1"
    mcp_port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = "INFO"

    @field_validator("knowledge_root", mode="before")
    @classmethod
    def expand_root(cls, value: object) -> Path:
        return Path(str(value)).expanduser().resolve()

    @field_validator("mcp_transport")
    @classmethod
    def validate_transport(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"stdio", "streamable-http"}:
            raise ValueError("MCP_TRANSPORT must be stdio or streamable-http")
        return normalized

    @property
    def canonical_path(self) -> Path:
        return self.knowledge_root / self.canonical_dir

    @property
    def openwiki_path(self) -> Path:
        return self.knowledge_root / self.openwiki_dir

    @property
    def generated_path(self) -> Path:
        return self.knowledge_root / self.generated_dir

    @property
    def operations_path(self) -> Path:
        return self.knowledge_root / self.operations_dir


settings = Settings()
