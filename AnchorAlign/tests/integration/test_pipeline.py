import pytest
from anchoralign.pipeline.orchestrator import run_pipeline
from ..fixtures.synthetic import FIXTURES

def test_pipeline_basic():
    res = run_pipeline("ACGT", "ACGT")
    assert res.reference_length == 4
    assert res.query_length == 4

def test_pipeline_empty():
    res = run_pipeline("", "")
    assert res.reference_length == 0
    assert res.query_length == 0

@pytest.mark.parametrize("case_name, case_data", FIXTURES.items())
def test_pipeline_fixtures(case_name, case_data):
    res = run_pipeline(case_data["ref"], case_data["query"])
    assert res.reference_length == len(case_data["ref"])
    assert res.query_length == len(case_data["query"])
