"""Tests for sandbox detection helpers."""
from peanut_review import sandbox


def test_detects_bwrap_die_with_parent_cmdline():
    assert sandbox.is_bwrap_die_with_parent_cmdline([
        "bwrap",
        "--new-session",
        "--die-with-parent",
        "--",
        "codex",
    ])


def test_detects_bwrap_pid_namespace_cmdline():
    assert sandbox.is_bwrap_pid_namespace_cmdline([
        "bwrap",
        "--new-session",
        "--unshare-pid",
        "--",
        "codex",
    ])


def test_ignores_bwrap_without_die_with_parent():
    assert not sandbox.is_bwrap_die_with_parent_cmdline([
        "bwrap",
        "--new-session",
        "--",
        "codex",
    ])


def test_ignores_bwrap_without_unshare_pid_for_pid_namespace():
    assert not sandbox.is_bwrap_pid_namespace_cmdline([
        "bwrap",
        "--new-session",
        "--",
        "codex",
    ])


def test_ignores_non_bwrap_pid_one():
    assert not sandbox.is_bwrap_die_with_parent_cmdline([
        "/sbin/init",
        "--die-with-parent",
    ])
