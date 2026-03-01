import os
import sys
import operator
from typing import get_type_hints
from langgraph.graph import add_messages

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agent.state import (
    OverallState,
    ReflectionState,
    Query,
    WebSearchState,
    SearchStateOutput
)

def test_search_state_output_defaults():
    """Test SearchStateOutput dataclass defaults."""
    output = SearchStateOutput()
    assert output.running_summary is None

def test_search_state_output_init():
    """Test SearchStateOutput dataclass initialization."""
    output = SearchStateOutput(running_summary="summary")
    assert output.running_summary == "summary"

def test_overall_state_reducers():
    """
    Test that OverallState has the correct reducers configured via Annotated.
    """
    # include_extras=True is required to see Annotated metadata when using get_type_hints
    hints = get_type_hints(OverallState, include_extras=True)
    
    # Check messages reducer
    assert "messages" in hints
    # The first metadata item should be the reducer function
    assert hints["messages"].__metadata__[0] == add_messages
    
    # Check other list reducers
    assert hints["search_query"].__metadata__[0] == operator.add
    assert hints["web_research_result"].__metadata__[0] == operator.add
    assert hints["sources_gathered"].__metadata__[0] == operator.add

def test_reflection_state_reducers():
    """Test ReflectionState reducers."""
    hints = get_type_hints(ReflectionState, include_extras=True)
    assert hints["follow_up_queries"].__metadata__[0] == operator.add

def test_simple_typed_dicts():
    """Test instantiation of simple TypedDicts."""
    # Since TypedDict is just a dict at runtime, we just check we can create them
    # matching the structure.
    q: Query = {"query": "test", "rationale": "r"}
    assert q["query"] == "test"
    
    ws: WebSearchState = {"search_query": "q", "id": "1"}
    assert ws["id"] == "1"