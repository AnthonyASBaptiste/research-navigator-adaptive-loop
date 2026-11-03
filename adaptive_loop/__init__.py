"""
Adaptive Epistemic Research Loop & Vali Co-Pilot
Built for Meta Global AI Developer Hackathon 2026.
"""

from .pipeline import AdaptiveResearchPipeline, MODEL_ROSTERS
from .evidence_ledger import EvidenceLedger
from .regional_anchors import REGIONAL_ANCHORS, enforce_regional_query_bounding
from .vali_copilot import ValiCopilot

__all__ = [
    "AdaptiveResearchPipeline",
    "EvidenceLedger",
    "REGIONAL_ANCHORS",
    "enforce_regional_query_bounding",
    "ValiCopilot",
    "MODEL_ROSTERS",
]
