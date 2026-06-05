"""Shared pytest fixtures for the Mefan framework test suite.

These fixtures provide:
- `repo_root` — absolute path to the mefan project root
- `agents_dir` — path to .claude/agents/
- `hooks_dir` — path to .claude/hooks/
- `skills_dir` — path to .claude/skills/
- `superpowers_dir` — path to the installed superpowers plugin
- `tmp_sprint` — a tmp_path-based simulation of .claude/iterations/sprint-latest/
- `mock_adr` — minimal ADR.md fixture (for stage 4 integration tests)
- `mock_sprint_status` — minimal sprint-status.md fixture
- `mock_consistency_baseline` — minimal consistency-baseline.md fixture
"""

from __future__ import annotations

import os
from pathlib import Path
import textwrap
import pytest


# Repository root (the mefan project itself)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Installed superpowers plugin location
SUPERPOWERS_DIR = Path(
    "/home/amdin/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills"
)


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Absolute path to the mefan project root."""
    return REPO_ROOT


@pytest.fixture(scope="session")
def agents_dir(repo_root: Path) -> Path:
    """Path to .claude/agents/."""
    return repo_root / ".claude" / "agents"


@pytest.fixture(scope="session")
def hooks_dir(repo_root: Path) -> Path:
    """Path to .claude/hooks/."""
    return repo_root / ".claude" / "hooks"


@pytest.fixture(scope="session")
def skills_dir(repo_root: Path) -> Path:
    """Path to .claude/skills/."""
    return repo_root / ".claude" / "skills"


@pytest.fixture(scope="session")
def superpowers_dir() -> Path:
    """Path to the installed superpowers plugin directory."""
    return SUPERPOWERS_DIR


@pytest.fixture
def tmp_sprint(tmp_path: Path) -> Path:
    """A fresh tmp_path simulating `.claude/iterations/sprint-latest/`.

    Returns a directory that contains the minimum structure needed for
    stage 4 integration tests:
      - reviews/
      - task-summary/
    """
    sprint = tmp_path / "sprint-latest"
    sprint.mkdir()
    (sprint / "reviews").mkdir()
    (sprint / "task-summary").mkdir()
    return sprint


@pytest.fixture
def mock_adr(tmp_path: Path) -> Path:
    """A minimal ADR.md with §2.4 MG table, §5 API, §7 pseudocode.

    Returns the path to the file. Suitable for stage 4 integration tests
    that read ADR sections.
    """
    adr = tmp_path / "ADR.md"
    adr.write_text(
        textwrap.dedent(
            """\
            # ADR

            ## 2.4 Modular Group (MG) 划分

            | MG ID | US 列表 | 说明 |
            |-------|---------|------|
            | MG-001 | US-101, US-102 | 基础模块 |

            ## 5 API 设计

            ### POST /api/v1/items
            - Request: { "name": str, "value": int }
            - Response: { "id": int, "name": str, "value": int }
            - 错误码: 400 (参数错), 409 (重复)

            ## 7 任务与伪代码

            ### T-001 创建 Item 实体
            - 文件: src/api/items.py
            - 函数: create_item(name: str, value: int) -> Item
            """
        )
    )
    return adr


@pytest.fixture
def mock_sprint_status(tmp_path: Path) -> Path:
    """A minimal sprint-status.md with a 7-state machine row.

    Returns the path to the file.
    """
    s = tmp_path / "sprint-status.md"
    s.write_text(
        textwrap.dedent(
            """\
            # Sprint Status

            ## 1. 任务看板

            | Task ID | US | MG | Owner | 状态 |
            |---------|----|----|-------|------|
            | T-001 | US-101 | MG-001 | Dev | ToDo |

            ## 2. 状态机

            | MG ID | 当前状态 |
            |-------|----------|
            | MG-001 | Dev |
            """
        )
    )
    return s


@pytest.fixture
def mock_consistency_baseline(tmp_path: Path) -> Path:
    """A minimal consistency-baseline.md."""
    cb = tmp_path / "consistency-baseline.md"
    cb.write_text(
        textwrap.dedent(
            """\
            # Consistency Baseline

            ## 命名约定
            - Python: snake_case
            - TypeScript: camelCase
            """
        )
    )
    return cb
