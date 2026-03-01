import os
import sys
from unittest.mock import MagicMock, patch
import pytest
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Send

# Set dummy env vars to prevent AzureChatOpenAI from failing on import if it validates
os.environ["AZURE_OPENAI_API_KEY"] = "dummy"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://dummy.openai.azure.com/"
os.environ["AZURE_DEPLOYMENT_NAME"] = "dummy-deployment"

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Patch llm before importing graph to ensure we control it
with patch("langchain_openai.AzureChatOpenAI"):
    from agent.graph import (
        generate_query,
        continue_to_web_research,
        web_research,
        reflection,
        evaluate_research,
        finalize_answer
    )
    from agent.tools_and_schemas import SearchQueryList, Reflection

@pytest.fixture
def mock_llm():
    with patch("agent.graph.llm") as mock:
        yield mock

def test_generate_query(mock_llm):
    state = {"messages": [HumanMessage(content="test topic")], "initial_search_query_count": 2}
    config = {"configurable": {}}
    
    # Mock the structured output runnable
    mock_structured_runnable = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured_runnable
    
    # Mock the result of invoke
    expected_queries = SearchQueryList(query=["q1", "q2"], rationale="test")
    mock_structured_runnable.invoke.return_value = expected_queries
    
    result = generate_query(state, config)
    
    assert result["search_query"] == ["q1", "q2"]
    mock_llm.with_structured_output.assert_called_with(SearchQueryList)

def test_continue_to_web_research():
    state = {"search_query": ["q1", "q2"]}
    result = continue_to_web_research(state)
    
    assert len(result) == 2
    assert isinstance(result[0], Send)
    assert result[0].node == "web_research"
    assert result[0].arg == {"search_query": "q1", "id": 0}
    assert result[1].arg == {"search_query": "q2", "id": 1}

def test_web_research(mock_llm):
    state = {"search_query": "test query", "id": 1}
    config = {"configurable": {}}
    
    mock_response = MagicMock()
    mock_response.content = "search result content"
    mock_llm.invoke.return_value = mock_response
    
    result = web_research(state, config)
    
    assert result["web_research_result"] == ["search result content"]
    assert result["sources_gathered"] == []
    assert result["search_query"] == ["test query"]

def test_reflection(mock_llm):
    state = {
        "messages": [HumanMessage(content="topic")],
        "web_research_result": ["summary1"],
        "research_loop_count": 0,
        "search_query": ["q1"]
    }
    config = {"configurable": {}}
    
    mock_structured_runnable = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured_runnable
    
    expected_reflection = Reflection(
        is_sufficient=False,
        knowledge_gap="gap",
        follow_up_queries=["fq1"]
    )
    mock_structured_runnable.invoke.return_value = expected_reflection
    
    result = reflection(state, config)
    
    assert result["is_sufficient"] is False
    assert result["knowledge_gap"] == "gap"
    assert result["follow_up_queries"] == ["fq1"]
    assert result["research_loop_count"] == 1

def test_evaluate_research_continue():
    state = {
        "is_sufficient": False,
        "research_loop_count": 1,
        "max_research_loops": 3,
        "follow_up_queries": ["fq1"],
        "number_of_ran_queries": 5
    }
    config = {"configurable": {}}
    
    result = evaluate_research(state, config)
    
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].node == "web_research"
    assert result[0].arg["search_query"] == "fq1"
    # id should be number_of_ran_queries + idx = 5 + 0 = 5
    assert result[0].arg["id"] == 5

def test_evaluate_research_stop_sufficient():
    state = {
        "is_sufficient": True,
        "research_loop_count": 1,
        "max_research_loops": 3
    }
    config = {"configurable": {}}
    
    result = evaluate_research(state, config)
    assert result == "finalize_answer"

def test_evaluate_research_stop_max_loops():
    state = {
        "is_sufficient": False,
        "research_loop_count": 3,
        "max_research_loops": 3
    }
    config = {"configurable": {}}
    
    result = evaluate_research(state, config)
    assert result == "finalize_answer"

def test_finalize_answer(mock_llm):
    state = {
        "messages": [HumanMessage(content="topic")],
        "web_research_result": ["res1"],
        "sources_gathered": ["s1"]
    }
    config = {"configurable": {}}
    
    mock_response = MagicMock()
    mock_response.content = "Final Answer"
    mock_llm.invoke.return_value = mock_response
    
    result = finalize_answer(state, config)
    
    assert isinstance(result["messages"][0], AIMessage)
    assert result["messages"][0].content == "Final Answer"
    assert result["sources_gathered"] == ["s1"]