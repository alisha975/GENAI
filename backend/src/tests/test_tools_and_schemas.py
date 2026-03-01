import os
import sys
import pytest
from pydantic import ValidationError

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agent.tools_and_schemas import SearchQueryList, Reflection

def test_search_query_list_valid():
    data = {
        "query": ["query1", "query2"],
        "rationale": "Testing rationale"
    }
    model = SearchQueryList(**data)
    assert model.query == ["query1", "query2"]
    assert model.rationale == "Testing rationale"

def test_search_query_list_invalid():
    with pytest.raises(ValidationError):
        SearchQueryList(query="not a list", rationale=123)

def test_reflection_valid():
    data = {
        "is_sufficient": True,
        "knowledge_gap": "None",
        "follow_up_queries": []
    }
    model = Reflection(**data)
    assert model.is_sufficient is True
    assert model.knowledge_gap == "None"
    assert model.follow_up_queries == []

def test_reflection_invalid():
    with pytest.raises(ValidationError):
        # is_sufficient should be bool, follow_up_queries should be list
        Reflection(is_sufficient="maybe", knowledge_gap=None, follow_up_queries="string")