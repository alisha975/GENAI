import os
import sys
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agent.prompts import (
    get_current_date,
    query_writer_instructions,
    web_searcher_instructions,
    reflection_instructions,
    answer_instructions
)

def test_get_current_date():
    """Test that the date is returned in the expected format."""
    date_str = get_current_date()
    # Check format like "October 26, 2023"
    try:
        datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        assert False, f"Date format incorrect: {date_str}"

def test_prompts_content():
    """Test that prompts contain necessary placeholders."""
    assert "{research_topic}" in query_writer_instructions
    assert "{current_date}" in query_writer_instructions
    
    assert "{research_topic}" in web_searcher_instructions
    assert "{current_date}" in web_searcher_instructions
    
    assert "{research_topic}" in reflection_instructions
    assert "{summaries}" in reflection_instructions
    
    assert "{research_topic}" in answer_instructions
    assert "{summaries}" in answer_instructions
    assert "{current_date}" in answer_instructions