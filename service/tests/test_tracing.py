"""Tracing-config logic tests. Uses a DUMMY key set inline — never the real one
in .env — and restores the environment afterward. No network, no langsmith dep.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from graph import tracing  # noqa: E402

_LS_VARS = ["LANGSMITH_API_KEY", "LANGSMITH_TRACING", "LANGSMITH_PROJECT",
            "LANGCHAIN_API_KEY", "LANGCHAIN_TRACING_V2", "LANGCHAIN_PROJECT"]


def _clear():
    for v in _LS_VARS:
        os.environ.pop(v, None)


def test_no_key_means_tracing_off():
    _clear()
    try:
        assert tracing.configure() is False
        assert tracing.status()["tracing_enabled"] is False
    finally:
        _clear()


def test_key_auto_enables_tracing_and_sets_project():
    _clear()
    os.environ["LANGSMITH_API_KEY"] = "ls-test-DUMMY"
    try:
        assert tracing.configure() is True
        st = tracing.status()
        assert st["tracing_enabled"] is True
        assert st["project"]  # defaulted
        assert os.environ["LANGCHAIN_API_KEY"] == "ls-test-DUMMY"  # legacy mirror
    finally:
        _clear()


def test_explicit_disable_is_respected():
    _clear()
    os.environ["LANGSMITH_API_KEY"] = "ls-test-DUMMY"
    os.environ["LANGSMITH_TRACING"] = "false"
    try:
        assert tracing.configure() is False
    finally:
        _clear()


def test_run_config_is_tagged_by_persona():
    cfg = tracing.run_config("muslim", "Was Jesus made God at Nicaea?")
    assert cfg["run_name"] == "debate:muslim"
    assert "persona:muslim" in cfg["tags"]
    assert cfg["metadata"]["persona"] == "muslim"


if __name__ == "__main__":
    import traceback

    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except Exception:  # noqa: BLE001
            failed += 1
            print(f"  ✗ {t.__name__}")
            traceback.print_exc()
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
