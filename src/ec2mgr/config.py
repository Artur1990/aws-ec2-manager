from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    region: str = "us-east-1"
    profile: str | None = None


def load_config(path: str | None) -> AppConfig:
    """
    Load simple JSON config:
      {
        "region": "us-east-1",
        "profile": "dev"
      }
    """
    if not path:
        return AppConfig()

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")

    data = json.loads(p.read_text(encoding="utf-8"))
    return AppConfig(
        region=data.get("region", "us-east-1"),
        profile=data.get("profile", None),
    )
