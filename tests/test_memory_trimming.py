"""Regression test for Convo memory context trimming (memory_k / summary_k).

Covers a real bug found in review: _trim_history removed overflow messages
from state on every call regardless of whether the summary_k threshold was
actually met, so any summary_k that doesn't line up with the per-turn
message growth rate silently dropped trimmed history forever instead of
ever folding it into a summary.
"""
from __future__ import annotations

from langchain_core.messages import HumanMessage

from psychscanner.memories.base.mock_llm import ChatMockModel
from psychscanner.memories.single_turn_convo import single_turn_convo_node
from psychscanner.scanner_models.agent_config import AgentConfig


def _build_graph(memory_k, summary_k, repeat_buffer_length=10):
    agent_cfg = AgentConfig(
        modelname="mock-chat-model",
        familyname="mock-llm",
        parameters=None,
        modelobject=ChatMockModel(model="mock-chat-model", repeat_buffer_length=repeat_buffer_length),
        memory_type="Convo",
        memory_k=memory_k,
        summary_k=summary_k,
        chain_type="task",
        system_msg=None,
        parser=None,
        parser_raw=False,
        parser_config={},
    )
    return single_turn_convo_node(agent_cfg)


def _run_turns(graph, n_turns, thread_id="t1"):
    config = {"configurable": {"thread_id": thread_id}}
    state = None
    for i in range(n_turns):
        state = graph.invoke(
            {
                "inputs": [HumanMessage(content=f"turn {i}")],
                "system_message": "sys",
                "trcode": f"tr{i}",
            },
            config=config,
        )
    return state


def test_memory_k_caps_history_length():
    graph = _build_graph(memory_k=4, summary_k=0)
    state = _run_turns(graph, n_turns=6)
    assert len(state["inputs"]) <= 5


def test_summary_k_populates_rolling_summary_once_overflow_hits_threshold():
    graph = _build_graph(memory_k=4, summary_k=2)
    state = _run_turns(graph, n_turns=6)
    assert state.get("summary")


def test_unlimited_memory_k_grows_history():
    graph = _build_graph(memory_k=-1, summary_k=0)
    state = _run_turns(graph, n_turns=6)
    assert len(state["inputs"]) == 12


def test_summary_k_does_not_silently_drop_overflow_below_threshold():
    """summary_k=3 with memory_k=4 never lines up with this graph's
    2-messages-per-turn growth (overflow batches land at 2, not a multiple
    of 3), so the pre-fix code deleted every overflow batch without ever
    reaching the threshold -- silently losing all trimmed history,
    permanently. Turn 0's content must still be recoverable from the
    summary once enough turns have accumulated overflow past the
    threshold.
    """
    graph = _build_graph(memory_k=4, summary_k=3, repeat_buffer_length=2000)
    state = _run_turns(graph, n_turns=6)
    assert state.get("summary"), "overflow should have accumulated past the threshold by now"
    assert "turn 0" in state["summary"], (
        "turn 0's content was lost before ever being folded into a summary "
        f"-- got summary: {state['summary']!r}"
    )
