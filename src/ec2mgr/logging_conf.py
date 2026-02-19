from __future__ import annotations

import logging
import os


def setup_logging(level: str | None = None) -> None:
    """
    Simple, production-friendly logging setup.
    Priority:
      1) CLI --log-level
      2) ENV EC2MGR_LOG_LEVEL
      3) INFO
    """
    chosen = (level or os.getenv("EC2MGR_LOG_LEVEL") or "INFO").upper()

    logging.basicConfig(
        level=getattr(logging, chosen, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
