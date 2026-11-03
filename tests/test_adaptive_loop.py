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

from adaptive_loop.regional_anchors import enforce_regional_query_bounding
from adaptive_loop.evidence_ledger import EvidenceLedger
from adaptive_loop.pipeline import prepare_litellm_kwargs, resolve_model_with_fallback


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
