"""Helpers for detecting sandbox modes that cannot safely spawn reviewers."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence


def _proc_cmdline(pid: int = 1) -> list[str]:
    """Return argv for a process from /proc, or [] when unavailable."""
    try:
        raw = (Path("/proc") / str(pid) / "cmdline").read_bytes()
    except OSError:
        return []
    return [part.decode(errors="replace") for part in raw.split(b"\0") if part]


def _is_bwrap_cmdline(argv: Sequence[str]) -> bool:
    if not argv:
        return False
    exe = Path(argv[0]).name
    return exe in {"bwrap", "bubblewrap", "codex-linux-sandbox"}


def is_bwrap_die_with_parent_cmdline(argv: Sequence[str]) -> bool:
    """Return true for bubblewrap argv using --die-with-parent."""
    return _is_bwrap_cmdline(argv) and "--die-with-parent" in argv


def is_bwrap_pid_namespace_cmdline(argv: Sequence[str]) -> bool:
    """Return true for bubblewrap argv that unshares the PID namespace."""
    return _is_bwrap_cmdline(argv) and "--unshare-pid" in argv


def bwrap_die_with_parent_sandbox_detected() -> bool:
    """Detect the Codex-style bubblewrap sandbox that kills child agents."""
    return is_bwrap_die_with_parent_cmdline(_proc_cmdline(1))


def bwrap_pid_namespace_detected() -> bool:
    """Detect a bubblewrap PID namespace where outside PIDs are invisible."""
    return is_bwrap_pid_namespace_cmdline(_proc_cmdline(1))
