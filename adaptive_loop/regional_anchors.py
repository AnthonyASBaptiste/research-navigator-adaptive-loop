"""
Regional Grounding & Query Bounding Engine
Prevents search engines from returning generic US/EU results and grounds
venture validation in target emerging market realities (Caribbean, LATAM, SEA).
"""

from typing import Dict, Any, List

REGIONAL_ANCHORS: Dict[str, Dict[str, Any]] = {
    "caribbean": {
        "name": "Caribbean & CARICOM (Flagship Specialized Launch Region)",
        "keywords": [
            "caribbean", "trinidad and tobago", "trinidad", "tobago", "jamaica",
            "barbados", "guyana", "bahamas", "caricom", "eastern caribbean",
            "oecs", "wipay", "linx", "ttd", "jmd", "bbd", "csme",
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
    },
    "latam": {
        "name": "Latin America (LATAM Expansion)",
        "keywords": [
            "latam", "latin america", "brazil", "mexico", "colombia", "argentina",
            "chile", "peru", "pix", "spei", "mercadolibre", "nubank", "rappi",
            "bacen", "sat.gob.mx", "dian.gov.co", "afip.gob.ar"
        ],
        "authoritative_domains": [
            "infobae.com", "valor.globo.com", "elfinanciero.com.mx", "portafolio.co",
            "cronista.com", "latercera.com", "semana.com", "eleconomista.com.mx",
            "bcb.gov.br", "banxico.org.mx", "banrep.gov.co", "dian.gov.co", "sat.gob.mx"
        ],
        "cc_tlds": [".br", ".mx", ".co", ".ar", ".cl", ".pe", ".uy"]
    },
    "southeast_asia": {
        "name": "Southeast Asia (SEA Expansion)",
        "keywords": [
            "southeast asia", "asean", "singapore", "indonesia", "vietnam",
            "malaysia", "philippines", "thailand", "grab", "gojek", "shopee",
            "tokopedia", "paynow", "duitnow", "promptpay", "mas", "bank indonesia"
        ],
        "authoritative_domains": [
            "straitstimes.com", "thejakartapost.com", "techinasia.com",
            "dealstreetasia.com", "thestar.com.my", "bangkokpost.com",
            "inquirer.net", "vnexpress.net", "mas.gov.sg", "bi.go.id", "bnm.gov.my"
        ],
        "cc_tlds": [".sg", ".id", ".vn", ".my", ".ph", ".th"]
    },
    "us_eu": {
        "name": "United States & European Union (Mature Venture Scale)",
        "keywords": [
            "united states", "us", "uk", "european union", "eu", "california",
            "delaware", "stripe", "plaid", "sec", "edgar", "companies house", "hmrc"
        ],
        "authoritative_domains": [
            "sec.gov", "ftc.gov", "gov.uk", "europa.eu", "statista.com",
            "crunchbase.com", "pitchbook.com", "cbinsights.com", "reuters.com"
        ],
        "cc_tlds": [".us", ".uk", ".co.uk", ".de", ".fr", ".eu", ".gov"]
    }
}

# Alias mapping for intuitive CLI inputs
REGION_ALIASES: Dict[str, str] = {
    "caribbean": "caribbean",
    "caricom": "caribbean",
    "tt": "caribbean",
    "jm": "caribbean",
    "latam": "latam",
    "latin_america": "latam",
    "latin america": "latam",
    "sea": "southeast_asia",
    "southeast_asia": "southeast_asia",
    "southeast asia": "southeast_asia",
    "asia": "southeast_asia",
    "us": "us_eu",
    "eu": "us_eu",
    "us_eu": "us_eu",
    "global": "global"
}


def normalize_region(region: str) -> str:
    """Normalizes regional input strings and aliases."""
    if not region:
        return "caribbean"
    reg_clean = region.lower().strip().replace("-", "_")
    return REGION_ALIASES.get(reg_clean, reg_clean if reg_clean in REGIONAL_ANCHORS else "global")


def enforce_regional_query_bounding(query: str, region: str = "caribbean") -> str:
    """
    Ensures that a search query has explicit regional anchoring so search results
    are grounded in the target market rather than generic global data.
    """
    if not query:
        return query

    norm_region = normalize_region(region)
    if norm_region == "global":
        return query

    anchors = REGIONAL_ANCHORS.get(norm_region, {})
    keywords = anchors.get("keywords", [norm_region])

    query_lower = query.lower()
    has_region = any(kw in query_lower for kw in keywords)

    if not has_region:
        if norm_region == "caribbean":
            return f'{query} Caribbean OR "Trinidad" OR "Jamaica" OR "Barbados"'
        elif norm_region == "latam":
            return f'{query} Latin America OR "Brazil" OR "Mexico" OR "Colombia"'
        elif norm_region == "southeast_asia":
            return f'{query} Southeast Asia OR "Singapore" OR "Indonesia" OR "Vietnam"'
        return f"{query} {norm_region}"
    return query
