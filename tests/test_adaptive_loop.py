"""
Unit tests for the Adaptive Epistemic Research Loop.
"""

import os
import sys
import json
from pathlib import Path
import pytest

# Ensure adaptive_loop is importable
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from adaptive_loop.regional_anchors import enforce_regional_query_bounding, normalize_region
from adaptive_loop.evidence_ledger import EvidenceLedger
from adaptive_loop.pipeline import prepare_litellm_kwargs, resolve_model_with_fallback, calculate_calibrated_score


def test_enforce_regional_query_bounding():
    # Global query should remain untouched
    assert enforce_regional_query_bounding("AI tools", region="global") == "AI tools"

    # Caribbean query without anchor should have anchors injected
    bounded = enforce_regional_query_bounding("Shopify VAT tax plugin", region="caribbean")
    assert "Caribbean" in bounded
    assert "Trinidad" in bounded

    # Caribbean query already possessing an anchor should not duplicate
    already_bounded = enforce_regional_query_bounding("Trinidad POS merchants e-invoicing", region="caribbean")
    assert already_bounded == "Trinidad POS merchants e-invoicing"


def test_evidence_ledger_metrics():
    ledger = EvidenceLedger(target_region="caribbean")

    # Add regional source (.tt)
    ledger.add_source(
        url="https://ird.gov.tt/guidelines",
        content="Official tax guidelines for VAT registration.",
        round_num=1
    )
    # Add another regional source (authoritative domain)
    ledger.add_source(
        url="https://guardian.co.tt/business/news",
        content="Central Bank liquidity reports.",
        round_num=1
    )
    # Add generic non-regional source
    ledger.add_source(
        url="https://techcrunch.com/global-venture-trends",
        content="Global funding rounds in 2026.",
        round_num=2
    )
    # Duplicate URL should be ignored
    ledger.add_source(url="https://ird.gov.tt/guidelines", round_num=2)

    metrics = ledger.calculate_metrics()
    assert metrics["total_sources"] == 3
    assert metrics["regional_sources"] == 2
    assert metrics["regional_grounding_ratio"] == 0.67
    assert metrics["source_grounding_index"] > 0.5


def test_litellm_kwargs_preparation(monkeypatch):
    monkeypatch.setenv("BASETEN_API_KEY", "baseten_test_key")
    monkeypatch.setenv("FIREWORKS_API_KEY", "fw_test_key")

    baseten_kwargs = prepare_litellm_kwargs("baseten/meta-models/muse-spark-open-1026")
    assert baseten_kwargs["model"] == "openai/meta-models/muse-spark-open-1026"
    assert "baseten.co" in baseten_kwargs["api_base"]
    assert baseten_kwargs["timeout"] == 35.0

    fireworks_kwargs = prepare_litellm_kwargs("fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct")
    assert fireworks_kwargs["model"] == "openai/accounts/fireworks/models/llama-v3p3-70b-instruct"
    assert "fireworks.ai" in fireworks_kwargs["api_base"]


def test_provenance_dataset_integrity():
    prov_file = Path(__file__).parent.parent / "provenance" / "eval_results.json"
    assert prov_file.exists(), "eval_results.json provenance file must exist"

    with open(prov_file, "r") as f:
        cases = json.load(f)

    assert len(cases) == 5, "Benchmark evaluation must cover all 5 archetypes"
    total_voids = sum(c.get("adaptive", {}).get("evidence_voids_detected", 0) for c in cases)
    assert total_voids == 36, "Proven 36 evidentiary voids must be recorded"


def test_normalize_region():
    assert normalize_region("caribbean") == "caribbean"
    assert normalize_region("SEA") == "southeast_asia"
    assert normalize_region("latin_america") == "latam"
    assert normalize_region("US") == "us_eu"
    assert normalize_region("unknown_mars") == "global"


def test_calculate_calibrated_score():
    # Baseline returns raw base score
    base_score = calculate_calibrated_score(
        base_market_score=80.0,
        confidence=0.90,
        evidence_voids_count=0,
        sgi=1.0,
        is_adaptive=False
    )
    assert base_score == 80.0

    # Adaptive loop heavily penalizes voids and scales with confidence
    adaptive_score = calculate_calibrated_score(
        base_market_score=80.0,
        confidence=0.45,
        evidence_voids_count=6,
        sgi=0.8,
        is_adaptive=True
    )
    # Expected: (80 * 0.45) + (0.8 * 12) - (6 * 3.5) = 36 + 9.6 - 21 = 24.6
    assert 20.0 <= adaptive_score <= 35.0
    assert adaptive_score < base_score


@pytest.mark.asyncio
async def test_pipeline_run_research_mocked(monkeypatch):
    """
    Guarantees pipeline.run_research() executes without prompt formatting
    or attribute lookup errors (protects against F-01 and F-02 regressions).
    """
    from adaptive_loop.pipeline import AdaptiveResearchPipeline
    import json

    pipeline = AdaptiveResearchPipeline()

    async def mock_call_llm(role, system_prompt, user_prompt):
        if role == "planner":
            return json.dumps({"questions": ["Is there local market demand?"]})
        elif role == "market_analyst":
            return json.dumps({"summary": "Market analysis complete", "market_score": 70.0})
        elif role == "audit":
            return json.dumps({
                "readiness_status": "NEEDS_TARGETED_RESEARCH",
                "confidence_score": 0.50,
                "evidence_voids": ["Void 1"],
                "targeted_queries": ["Pricing in Trinidad"],
                "required_offline_experiments": ["Interview 10 merchants"]
            })
        return "{}"

    async def mock_search_web(query, region="caribbean", ledger=None, round_num=1):
        if ledger:
            ledger.add_source(url="https://ird.gov.tt/vat", title="Inland Revenue VAT rules", content="VAT guidelines", round_num=round_num)
        return "Authoritative VAT guidelines from IRD."

    monkeypatch.setattr(pipeline, "_call_llm", mock_call_llm)
    monkeypatch.setattr(pipeline, "_search_web", mock_search_web)

    # Test Adaptive Loop execution
    res = await pipeline.run_research(
        startup_idea="Caribbean Shopify VAT Plugin",
        region="caribbean",
        adaptive=True
    )

    assert "score" in res
    assert res["score"] > 0
    assert len(res["adaptive_loop"]["evidence_voids"]) > 0
    assert len(res["adaptive_loop"]["offline_experiments"]) > 0
    assert res["adaptive_loop"]["rounds_executed"] == 2

