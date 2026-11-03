"""
Evidence Ledger & Source Grounding Index (SGI)
Tracks citations, deduplicates URLs, and calculates regional grounding ratios
to ensure research findings are empirically verifiable and regionally anchored.
"""

from typing import Dict, Any, List
from urllib.parse import urlparse
from .regional_anchors import REGIONAL_ANCHORS


class EvidenceLedger:
    """
    Tracks external citations and evidence sources across multi-round research executions.
    Calculates the Source Grounding Index (SGI) and regional grounding ratio.
    """
    def __init__(self, target_region: str = "caribbean"):
        self.target_region = target_region
        self.sources: List[Dict[str, Any]] = []
        self._seen_urls = set()

    def add_source(
        self,
        url: str,
        content: str = "",
        query: str = "",
        round_num: int = 1,
        title: str = ""
    ) -> None:
        if not url or url in self._seen_urls:
            return
        self._seen_urls.add(url)
        domain = ""
        try:
            domain = urlparse(url).netloc.lower()
        except Exception:
            pass

        is_regional = False
        anchors = REGIONAL_ANCHORS.get(self.target_region.lower(), {})
        keywords = anchors.get("keywords", [self.target_region.lower()])
        cc_tlds = anchors.get("cc_tlds", [])
        authoritative = anchors.get("authoritative_domains", [])

        if any(domain.endswith(tld) for tld in cc_tlds):
            is_regional = True
        elif any(auth_d in domain for auth_d in authoritative):
            is_regional = True
        elif any(kw in (content + " " + query).lower() for kw in keywords):
            is_regional = True

        self.sources.append({
            "url": url,
            "domain": domain,
            "title": title or domain,
            "snippet": content[:300],
            "round": round_num,
            "query": query,
            "is_regional": is_regional
        })

    def calculate_metrics(self) -> Dict[str, Any]:
        total = len(self.sources)
        if total == 0:
            return {
                "total_sources": 0,
                "regional_sources": 0,
                "regional_grounding_ratio": 0.0,
                "source_grounding_index": 0.0
            }

        regional_count = sum(1 for s in self.sources if s.get("is_regional", False))
        regional_ratio = round(regional_count / total, 2)
        base_sgi = min(total / 5.0, 1.0) * 0.5 + (regional_ratio * 0.5)

        return {
            "total_sources": total,
            "regional_sources": regional_count,
            "regional_grounding_ratio": regional_ratio,
            "source_grounding_index": round(base_sgi, 2)
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metrics": self.calculate_metrics(),
            "sources": self.sources
        }
