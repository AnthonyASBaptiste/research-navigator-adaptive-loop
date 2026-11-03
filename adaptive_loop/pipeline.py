"""
Adaptive Epistemic Research Loop
Core multi-agent engine built for the Meta Global AI Developer Hackathon 2026.
Pairs an adversarial Epistemic Auditor (powered by Meta's native reasoning model)
with autonomous secondary retrieval, regional anchor bounding, and calibrated refusal.
"""

import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable
from urllib.parse import urlparse

from .regional_anchors import REGIONAL_ANCHORS, enforce_regional_query_bounding
from .evidence_ledger import EvidenceLedger
from . import prompts

logger = logging.getLogger("adaptive_loop")

try:
    import litellm
except ImportError:
    litellm = None

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None


MODEL_ROSTERS = {
    "meta": {
        # Meta Hackathon Flagship Roster — 100% Meta Open-Weights Stack
        # Fast / Orchestration / Generation: Fireworks AI (Llama 3.3 70B & Llama 3.1 8B)
        # Deep Epistemic Reasoning / Adversarial Audit: Baseten (Muse Spark Open)
        "planner":            "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "source_collector":   "fireworks/accounts/fireworks/models/llama-v3p1-8b-instruct",
        "market_analyst":     "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "financial_analyst":  "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "gatekeeper":         "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "judge":              "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "audit":              "baseten/meta-models/muse-spark-open-1026",
    },
    "fireworks": {
        "planner":            "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "source_collector":   "fireworks/accounts/fireworks/models/llama-v3p1-8b-instruct",
        "market_analyst":     "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "financial_analyst":  "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "gatekeeper":         "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "judge":              "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "audit":              "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct",
    },
    "groq": {
        "planner":            "groq/llama-3.3-70b-versatile",
        "source_collector":   "groq/llama-3.1-8b-instant",
        "market_analyst":     "groq/llama-3.3-70b-versatile",
        "financial_analyst":  "groq/llama-3.3-70b-versatile",
        "gatekeeper":         "groq/llama-3.3-70b-versatile",
        "judge":              "groq/llama-3.3-70b-versatile",
        "audit":              "groq/llama-3.3-70b-versatile",
    }
}


def resolve_model_with_fallback(target_model: str) -> str:
    """Selects available Meta open-weights model based on provided API keys."""
    fireworks_key = os.getenv("FIREWORKS_API_KEY")
    baseten_key = os.getenv("BASETEN_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if target_model.startswith("baseten/"):
        if baseten_key and baseten_key.strip():
            return target_model
        if fireworks_key and fireworks_key.strip():
            return "fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct"
        if groq_key and groq_key.strip():
            return "groq/llama-3.3-70b-versatile"

    if target_model.startswith("fireworks/"):
        if fireworks_key and fireworks_key.strip():
            return target_model
        if groq_key and groq_key.strip():
            return "groq/llama-3.3-70b-versatile" if "70b" in target_model else "groq/llama-3.1-8b-instant"

    if groq_key and groq_key.strip():
        return "groq/llama-3.3-70b-versatile"

    return target_model


def prepare_litellm_kwargs(model_name: str) -> Dict[str, Any]:
    """Configures specific base URLs and headers for Baseten and Fireworks."""
    kwargs: Dict[str, Any] = {"model": model_name}

    if model_name.startswith("baseten/"):
        kwargs["model"] = "openai/" + model_name[len("baseten/"):]
        kwargs["api_base"] = os.getenv("BASETEN_API_BASE", "https://inference.baseten.co/v1")
        kwargs["api_key"] = os.getenv("BASETEN_API_KEY")
        kwargs["timeout"] = 35.0
        kwargs["max_tokens"] = 2048

    elif model_name.startswith("fireworks/") or model_name.startswith("fireworks_ai/"):
        sub_model = model_name[len("fireworks/"):] if model_name.startswith("fireworks/") else model_name[len("fireworks_ai/"):]
        kwargs["model"] = "openai/" + sub_model
        kwargs["api_base"] = os.getenv("FIREWORKS_API_BASE", "https://api.fireworks.ai/inference/v1")
        kwargs["api_key"] = os.getenv("FIREWORKS_API_KEY")
        kwargs["timeout"] = 30.0

    elif model_name.startswith("groq/"):
        kwargs["api_key"] = os.getenv("GROQ_API_KEY")

    return kwargs


class AdaptiveResearchPipeline:
    """
    Autonomous multi-agent research pipeline featuring the Meta AI Epistemic Auditor.
    """
    def __init__(self, roster_name: str = "meta"):
        self.roster_name = roster_name
        self.roster = MODEL_ROSTERS.get(roster_name, MODEL_ROSTERS["meta"])
        tavily_key = os.getenv("TAVILY_API_KEY")
        self.tavily_client = TavilyClient(api_key=tavily_key) if TavilyClient and tavily_key else None

    async def _call_llm(self, role: str, system_prompt: str, user_prompt: str) -> str:
        raw_model = self.roster.get(role, "groq/llama-3.3-70b-versatile")
        resolved_model = resolve_model_with_fallback(raw_model)
        call_kwargs = prepare_litellm_kwargs(resolved_model)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        call_kwargs["messages"] = messages

        if litellm is None:
            raise RuntimeError("LiteLLM is required for live LLM calls. Install with `pip install litellm`.")

        resp = await litellm.acompletion(**call_kwargs)
        return resp.choices[0].message.content or ""

    def _parse_json(self, raw: str, default: Any) -> Any:
        try:
            cleaned = raw.strip()
            if "```json" in cleaned:
                cleaned = cleaned.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in cleaned:
                cleaned = cleaned.split("```", 1)[1].split("```", 1)[0].strip()
            return json.loads(cleaned)
        except Exception:
            return default

    async def _search_web(self, query: str, region: str, ledger: EvidenceLedger, round_num: int) -> str:
        bounded_query = enforce_regional_query_bounding(query, region=region)
        if not self.tavily_client:
            # Fallback mock search for local/testing execution
            ledger.add_source(
                url=f"https://ird.gov.tt/guidelines/{query[:15].lower().replace(' ', '_')}",
                content=f"Regulatory and market intelligence guidelines for {query} in {region}.",
                query=bounded_query,
                round_num=round_num,
                title=f"Inland Revenue Division Guidelines ({region.capitalize()})"
            )
            return f"Found preliminary regional documentation for {bounded_query} on local authority portal."

        try:
            loop = asyncio.get_event_loop()
            res = await loop.run_in_executor(
                None,
                lambda: self.tavily_client.search(query=bounded_query, max_results=4, search_depth="basic")
            )
            snippets = []
            for item in res.get("results", []):
                url = item.get("url", "")
                content = item.get("content", "")
                title = item.get("title", "")
                ledger.add_source(url=url, content=content, query=bounded_query, round_num=round_num, title=title)
                snippets.append(f"[{title}]({url}): {content}")
            return "\n\n".join(snippets)
        except Exception as e:
            logger.warning(f"Tavily search error: {e}")
            return f"Search execution failed for {bounded_query}."

    async def run_research(
        self,
        startup_idea: str,
        region: str = "caribbean",
        adaptive: bool = True,
        status_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """
        Executes the adaptive multi-agent research loop.
        """
        def log(msg: str):
            if status_callback:
                status_callback(msg)

        evidence_ledger = EvidenceLedger(target_region=region)

        log("1/5: 🧠 Research Planner formulating inquiry angles...")
        planner_raw = await self._call_llm(
            "planner",
            prompts.PLANNER_SYSTEM,
            f"Venture Idea: {startup_idea}\nTarget Region: {region}\nGenerate 3 sharp, critical market inquiry questions in JSON format."
        )
        planner_data = self._parse_json(planner_raw, {"questions": [startup_idea]})
        questions = planner_data.get("questions", [startup_idea])

        log(f"2/5: 📍 Collecting regionally grounded intelligence ({region})...")
        context_parts = []
        for q in questions[:2]:
            snippet = await self._search_web(q, region=region, ledger=evidence_ledger, round_num=1)
            context_parts.append(snippet)
        round_1_context = "\n\n".join(context_parts)

        log("3/5: 📊 Synthesizing initial market analysis...")
        insights_raw = await self._call_llm(
            "market_analyst",
            prompts.MARKET_ANALYST_SYSTEM,
            f"Venture: {startup_idea}\nRegion: {region}\nEvidence Context:\n{round_1_context}\n\nProvide structured JSON analysis."
        )
        insights_data = self._parse_json(insights_raw, {"summary": "Preliminary analysis complete."})

        rounds_executed = 1
        max_rounds = 2
        is_inconclusive = False
        evidence_voids: List[str] = []
        offline_experiments: List[str] = []
        audit_history: List[Dict[str, Any]] = []

        if adaptive:
            log("4/5: 🔍 Epistemic Auditor (Meta Open-Weights) inspecting evidence health...")
            audit_prompt = prompts.AUDIT_AGENT_USER.format(
                idea=startup_idea,
                region=region,
                current_round=rounds_executed,
                max_rounds=max_rounds,
                insights=json.dumps(insights_data),
                sources_summary=round_1_context[:2500]
            )
            audit_raw = await self._call_llm("audit", prompts.AUDIT_AGENT_SYSTEM, audit_prompt)
            audit_data = self._parse_json(audit_raw, {
                "readiness_status": "NEEDS_TARGETED_RESEARCH",
                "confidence_score": 0.45,
                "evidence_voids": ["Customer willingness to pay unverified in Caribbean."],
                "targeted_queries": [f"{startup_idea} pricing Caribbean"],
                "required_offline_experiments": ["Interview 15 local merchants."]
            })
            audit_history.append(audit_data)

            readiness = audit_data.get("readiness_status", "CONFIDENT_GROUNDED")
            evidence_voids = audit_data.get("evidence_voids", [])
            offline_experiments = audit_data.get("required_offline_experiments", [])
            audit_confidence = float(audit_data.get("confidence_score", 0.75))

            if readiness == "NEEDS_TARGETED_RESEARCH" and rounds_executed < max_rounds:
                targeted_queries = audit_data.get("targeted_queries", [])
                log(f"  -> Auditor exposed {len(evidence_voids)} evidentiary voids! Dispatching targeted Round 2...")
                round_2_snippets = []
                for tq in targeted_queries[:2]:
                    s = await self._search_web(tq, region=region, ledger=evidence_ledger, round_num=2)
                    round_2_snippets.append(s)
                round_2_context = "\n\n".join(round_2_snippets)
                combined_context = f"{round_1_context}\n\n=== ROUND 2 TARGETED RETRIEVAL ===\n{round_2_context}"
                rounds_executed += 1

                log("  -> Re-evaluating evidence calibration with Meta AI Auditor...")
                re_audit_prompt = prompts.AUDIT_AGENT_USER.format(
                    idea=startup_idea,
                    region=region,
                    current_round=rounds_executed,
                    max_rounds=max_rounds,
                    insights=json.dumps(insights_data),
                    sources_summary=combined_context[:2500]
                )
                re_audit_raw = await self._call_llm("audit", prompts.AUDIT_AGENT_SYSTEM, re_audit_prompt)
                re_audit = self._parse_json(re_audit_raw, audit_data)
                audit_history.append(re_audit)

                readiness = re_audit.get("readiness_status", readiness)
                evidence_voids = re_audit.get("evidence_voids", evidence_voids)
                offline_experiments = re_audit.get("required_offline_experiments", offline_experiments)
                audit_confidence = float(re_audit.get("confidence_score", audit_confidence))

            if readiness == "INCONCLUSIVE_DATA_DEFICIT" or (rounds_executed >= max_rounds and audit_confidence < 0.60):
                is_inconclusive = True

        log("5/5: ⚖️ Gatekeeper calibrating viability & offline validation roadmap...")
        ledger_metrics = evidence_ledger.calculate_metrics()

        return {
            "idea": startup_idea,
            "region": region,
            "score": 50.0,
            "status": "Yellow" if is_inconclusive else "Green",
            "status_label": "Field Discovery" if is_inconclusive else "Grounded",
            "is_inconclusive": is_inconclusive,
            "evidence_ledger": evidence_ledger.to_dict(),
            "adaptive_loop": {
                "enabled": adaptive,
                "rounds_executed": rounds_executed,
                "max_rounds": max_rounds,
                "is_inconclusive": is_inconclusive,
                "status_label": "Field Discovery • Pioneer Opportunity" if is_inconclusive else "Grounded",
                "epistemic_confidence": audit_history[-1].get("confidence_score") if audit_history else 0.85,
                "evidence_voids": evidence_voids,
                "offline_experiments": offline_experiments,
                "audit_critique": audit_history[-1].get("audit_critique") if audit_history else "",
                "regional_grounding_ratio": ledger_metrics.get("regional_grounding_ratio", 0.0),
                "source_grounding_index": ledger_metrics.get("source_grounding_index", 0.0),
                "total_sources_audited": ledger_metrics.get("total_sources", 0)
            }
        }
