"""Unit tests for psychscanner.download_lib (primal) -- parameter validation
and path construction. _sync_repo is monkeypatched everywhere so no test
touches the network or git.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from psychscanner import library_download as ld
from psychscanner.library_download import download_lib


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    calls = []
    monkeypatch.setattr(ld, "_sync_repo", lambda dest, ref: calls.append((dest, ref)))
    return calls


@pytest.fixture
def installed_as(monkeypatch):
    def _set(distro):
        monkeypatch.setattr(ld, "_installed_distro", lambda: distro)

    return _set


def test_rejects_bad_library():
    with pytest.raises(ValueError, match="library"):
        download_lib(library="bogus")


def test_distro_mismatch_raises_before_network_call(installed_as, no_network):
    installed_as("psychscanner")  # not primal
    with pytest.raises(RuntimeError, match="primal"):
        download_lib(library="primal")
    assert no_network == []


def test_matching_distro_returns_tasks_only(tmp_path, installed_as):
    installed_as("primal")
    paths = download_lib(library="primal", dest=tmp_path)
    assert paths == {"tasks": tmp_path / "tasks" / "primal"}


def test_library_psychscanner_bypasses_installed_check_for_browsing(tmp_path, installed_as):
    installed_as("primal")
    paths = download_lib(library="psychscanner", dest=tmp_path)
    assert paths == {"tasks": tmp_path / "tasks" / "psychscanner"}


def test_library_all_skips_distro_check_and_covers_both(tmp_path, installed_as):
    installed_as("primal")
    paths = download_lib(library="all", dest=tmp_path)
    assert paths == {
        "psychscanner": {"tasks": tmp_path / "tasks" / "psychscanner"},
        "primal": {"tasks": tmp_path / "tasks" / "primal"},
    }


def test_sync_repo_called_with_dest_and_ref(tmp_path, installed_as, no_network):
    installed_as("primal")
    download_lib(library="primal", dest=tmp_path, ref="v1.2")
    assert no_network == [(tmp_path, "v1.2")]


def test_default_dest_is_shared_cache_dir(installed_as):
    installed_as("primal")
    paths = download_lib(library="primal")
    assert paths["tasks"] == Path.home() / ".cache" / "psychscanner" / "psyscan-library" / "tasks" / "primal"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
