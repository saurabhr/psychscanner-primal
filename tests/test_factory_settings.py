"""Regression test: PSCAN_OLLAMA_DEFAULT_FACTORY must not mutate DEFAULT_FACTORY.

`{**DEFAULT_FACTORY}` is a shallow copy -- the nested "EXP_CARD_INIT" dict
stayed the same object in both, so setting the ollama variant's
familyname/modelname silently corrupted DEFAULT_FACTORY's too.
"""
from __future__ import annotations

from psychscanner.staging.factory_settings import DEFAULT_FACTORY, PSCAN_OLLAMA_DEFAULT_FACTORY


def test_ollama_variant_does_not_mutate_default_factory():
    assert DEFAULT_FACTORY["EXP_CARD_INIT"]["familyname"] == "mock-llm"
    assert DEFAULT_FACTORY["EXP_CARD_INIT"]["modelname"] == "mock-chat-model"
    assert PSCAN_OLLAMA_DEFAULT_FACTORY["EXP_CARD_INIT"]["familyname"] == "ollama"
    assert PSCAN_OLLAMA_DEFAULT_FACTORY["EXP_CARD_INIT"]["modelname"] == "llama2"
