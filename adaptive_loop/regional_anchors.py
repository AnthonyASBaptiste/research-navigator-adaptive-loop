"""
Regional Grounding & Query Bounding Engine
Prevents search engines from returning generic US/EU results and grounds
venture validation in target emerging market realities (Caribbean & LATAM).
"""

from typing import Dict, Any, List

REGIONAL_ANCHORS: Dict[str, Dict[str, Any]] = {
    "caribbean": {
        "keywords": [
            "caribbean", "trinidad and tobago", "trinidad", "tobago", "jamaica",
            "barbados", "guyana", "bahamas", "caricom", "eastern caribbean",
            "oecs", "latam", "wipay", "linx", "ttd", "jmd", "bbd", "csme",
            "central bank", "inland revenue"
        ],
        "authoritative_domains": [
            "trinidadexpress.com", "newsday.co.tt", "guardian.co.tt",
            "loopnews.com", "jamaica-gleaner.com", "jamaicaobserver.com",
            "barbadostoday.bb", "stabroeknews.com", "demerarawaves.com",
            "ird.gov.tt", "jamaicatax.gov.jm", "bra.gov.bb", "caricom.org",
            "caribank.org", "eclac.org", "tradeind.gov.tt", "central-bank.org.tt",
            "boj.org.jm", "centralbank.org.bb", "exportt.co.tt", "jamprocorp.com"
        ],
        "cc_tlds": [".tt", ".bb", ".jm", ".gy", ".lc", ".bs", ".ag", ".dm", ".gd", ".kn", ".vc"]
    }
}


def enforce_regional_query_bounding(query: str, region: str = "caribbean") -> str:
    """
    Ensures that a search query has explicit regional anchoring so search results
    are grounded in the target market rather than generic global data.
    """
    if not query or not region or region.lower() == "global":
        return query

    region_key = region.lower().strip()
    anchors = REGIONAL_ANCHORS.get(region_key, {})
    keywords = anchors.get("keywords", [region_key])

    query_lower = query.lower()
    has_region = any(kw in query_lower for kw in keywords)

    if not has_region:
        if region_key == "caribbean":
            return f'{query} Caribbean OR "Trinidad" OR "Jamaica" OR "Barbados"'
        return f"{query} {region}"
    return query
