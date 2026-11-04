# 🧭 Research Navigator — Adaptive Epistemic Research Loop
### Meta Global AI Developer Hackathon 2026 (Startup Track)

> **The anti-sycophantic startup research coach powered by Meta open-weights models that turns false AI certainty into honest field validation.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Meta Open-Weights](https://img.shields.io/badge/Meta_AI-Muse_Spark_Open_+_Llama_3.3_70B-blueviolet)](https://www.llama.com/)
[![Baseten](https://img.shields.io/badge/Inference-Baseten-black)](https://www.baseten.co/)
[![Fireworks AI](https://img.shields.io/badge/Inference-Fireworks_AI-orange)](https://fireworks.ai/)
[![Staging Live](https://img.shields.io/badge/Demo-meta--hackathon.research--navigator.ai-green)](https://meta-hackathon.research-navigator.ai)

---

## 📜 Hackathon Provenance: What Existed Before vs. What Was Built This Week

In strict compliance with the hackathon rules and guidelines, this public repository contains **only the features, code, and functionality newly developed during the Hackathon (between kickoff on October 26 at 12:24 PM ET and November 4, 2026)**.

| Component | Pre-Existing Framework (Before Oct 26 Kickoff) | Newly Built During Hackathon (Oct 26 – Nov 4, 2026) |
| :--- | :--- | :--- |
| **Research Engine** | Single-pass linear search that summarized high-level web stats and gave uncritical, optimistic viability scores. | **Adaptive Epistemic Research Loop**: Multi-round feedback loop pairing an adversarial Epistemic Auditor with autonomous secondary retrieval. |
| **Meta AI Stack** | Not used. | • **Epistemic Auditor**: `meta-models/muse-spark-open-1026` via **Baseten**.<br>• **Fast Synthesis & Planner**: `llama-v3p3-70b-instruct` via **Fireworks AI**.<br>• **Vali Co-Pilot**: `llama-v3p3-70b-instruct` via **Fireworks AI**. |
| **Regional Reality** | Generic global search returning irrelevant US/EU tax and regulatory articles. | **`REGIONAL_ANCHORS` Engine**: Programmatically anchors queries to Caribbean territories (`.tt`, `.bb`, `.jm`, CARICOM, IRD, Linx, WiPay). |
| **Citation Health** | Basic unverified URL list. | **Evidence Ledger & Source Grounding Index (SGI)**: Deduplicates citations and quantifies grounded claim ratios. |
| **Epistemic Refusal** | Generic 85%+ confidence scores. | **"Field Discovery • Pioneer Opportunity"**: Refuses false certainty on frontier data; prescribes structured physical founder experiments. |
| **Validation Co-Pilot** | Basic rule-based assistant. | **Vali Co-Pilot Upgrade**: Powered by Fireworks Llama 3.3 70B to parse field voice notes and extract Mom Test evidence. |
| **Harness & Runner** | None. | **5-Archetype Benchmark Suite** (`eval_benchmark.py`) + **Standalone Judge Runner** (`demo.py`) with zero-key replay provenance. |

*Note: The pre-existing platform (Research Navigator) is an integrated full-stack startup validation system consisting of a Vue 3 frontend, Go API orchestrator, and PostgreSQL persistence. This standalone repository provides a clean, self-contained Python interface directly driving the event-built agent logic.*

---

## ⚡ Quickstart for Judges (< 60 Seconds)

Judges can execute and verify the entire agent architecture **with or without API keys**.

### 1. Installation
```bash
git clone https://github.com/AnthonyASBaptiste/research-navigator-adaptive-loop.git
cd research-navigator-adaptive-loop
pip install -r requirements.txt
```

### 2. Zero-Key Instant Verification (Replay Mode)
Experience the exact execution of **Case 4: Caribbean Shopify VAT Plugin** using our recorded raw provenance outputs from the live run:
```bash
python demo.py --replay
```
*Witness the Epistemic Auditor identify 6 evidentiary voids, dispatch Round 2 retrieval, down-calibrate confidence from 92% to 45%, and prescribe 2 mandatory offline customer discovery experiments.*

### 3. Run the Full 5-Case Benchmark Comparison
```bash
python eval_benchmark.py --replay
```
*Renders the complete 5-case comparative matrix in your terminal, showing -42.2% sycophancy reduction and 36 caught evidentiary voids.*

### 4. Test the Vali Co-Pilot Simulator (No WhatsApp setup required)
Simulate a founder returning from a Caribbean merchant discovery interview with a field voice note:
```bash
python vali_simulator.py --sample
```
*Vali parses the interview notes using Mom Test criteria, confirms friction, extracts willingness to pay, and updates the venture's evidence log.*

### 5. Live Execution Mode (With Your Own Meta API Keys)
Copy `.env.example` to `.env` and supply your Baseten, Fireworks, or Groq API key:
```bash
cp .env.example .env
# Add your FIREWORKS_API_KEY, BASETEN_API_KEY, or GROQ_API_KEY
python demo.py --live --idea "Cross-border remittance bypassing commercial bank FX queues in Trinidad"
```

---

## 🏗️ Architecture: The Adaptive Epistemic Research Loop

```
                        [ Founder Startup Pitch ]
                                    │
                                    ▼
                     [ 1. Planner Agent (Llama 3.3 70B) ]
                                    │
                     (Enforces REGIONAL_ANCHORS Bounding)
                                    ▼
                     [ 2. Regionally Grounded Search ]
                         (Evidence Ledger & SGI)
                                    │
                                    ▼
                     [ 3. Market & Financial Analysts ]
                                    │
                                    ▼
       ┌───────────► [ 4. Epistemic Auditor (Muse Spark Open) ]
       │                         │
       │              (Checks 4 Failure Modes)
       │                         │
       │        ┌────────────────┴────────────────┐
       │        ▼                                 ▼
[ Evidentiary Voids Detected ]          [ Sufficient Empirical Data ]
       │                                          │
       ▼                                          ▼
[ Round 2 Targeted Search ]             [ Confident Grounded Report ]
(Bounded gap-resolution queries)
       │
       ▼ (If public data remains sparse)
[ "Field Discovery • Pioneer Opportunity" Verdict ]
  • Honest Epistemic Calibration (e.g. 45% confidence)
  • Source Grounding Index (SGI) calculated
  • Mandatory Offline Discovery Experiments Prescribed
       │
       ▼
[ 5. Vali Autonomous Co-Pilot (Fireworks Llama 3.3 70B) ]
  • Coaches founder through prescribed offline experiments on WhatsApp
  • Parses voice notes & customer quotes using Mom Test criteria
  • Appends empirical evidence back to venture roadmap
```

---

## 📊 Empirical Benchmark Results

Evaluated across 5 diverse venture archetypes using `eval_benchmark.py`:

| Scenario & Archetype | Baseline (1-Pass) | Meta Adaptive Loop | Voids Caught | SGI | Calibrated Outcome |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **1. The Buzzword Hand-Wave** *(Quantum CRE leasing)* | 78.0 (85% conf) | **28.0 (42% conf)** | **8** | 56% | Caught ungrounded viral K-factor and zero CAC assumptions. Prescribed 3 pilot experiments. |
| **2. The Contradictory Market** *(US-TT Remittance)* | 82.0 (90% conf) | **32.0 (44% conf)** | **8** | **100%** | Exposed Central Bank exchange control contradictions. Prescribed Central Bank interviews. |
| **3. The Obscure Regional Niche** *(Dominica LoRaWAN)* | 74.0 (85% conf) | **48.0 (58% conf)** | **6** | **100%** | Detected zero public LoRaWAN rural data. Prescribed 3-month cooperative sensor test. |
| **4. The Grounded B2B SaaS** *(Shopify VAT plugin)* | 86.0 (92% conf) | **44.0 (45% conf)** | **6** | **100%** | Caught missing active merchant counts and Inland Revenue API specs. Prescribed 30 discovery interviews. |
| **5. The Unverifiable Consumer Habit** *(Hydration stake)* | 70.0 (94% conf) | **30.0 (46% conf)** | **8** | 50% | Refused to treat macro wellness TAM as proof of deposit staking. Prescribed 100-user default pilot. |

### 🎯 Key Benchmark Takeaways
- **Evidentiary Voids Exposed**: **36 critical voids caught** across 5 ventures (Baseline caught **0**).
- **Epistemic Calibration**: Reduced dangerous false confidence from **89.2%** down to an honest **47.0%** (**-42.2% sycophancy reduction**).
- **Score Calibration**: Shifted from uncritical vanity scores (**78.0 avg**) to risk-adjusted reality (**36.4 avg**, penalized -3.5 pts per void).
- **Regional Moat Integrity**: Achieved **up to 100% Regional Source Grounding Index (SGI)** on Caribbean ventures.
- **Honest Refusal Rate**: **100% (5/5)** refusal to hallucinate certainty on frontier startup concepts.

---

## 💡 The 4-Part Decision Signal Architecture

Generic startup validation tools provide a single sycophantic score (e.g. "85/100: Great idea!") based on high-level macro market reports. Research Navigator rejects single-number hype. Instead, our pipeline outputs a **composite 4-part Decision Signal**:

1. **Calibrated Viability Score (18–85)**: Dynamically computed as `(Base Market TAM * Epistemic Confidence) + SGI Grounding Bonus - (Voids Count * 3.5 pts)`. When an idea contains unverified claims, its score plummets.
2. **Calibrated Epistemic Confidence (0–100%)**: Measures the probability that the available empirical evidence actually supports the founder's thesis.
3. **Evidentiary Voids Checklist**: Explicit bulleted list of the exact operational, regulatory, or economic unknowns that must be verified before building code.
4. **Prescribed Physical Field Experiments**: Concrete, real-world customer discovery tasks formulated to resolve each detected void in the physical world (interviews, pilots, regulatory filings).

---

## 🌍 Multi-Regional Anchoring Engine

While Caribbean and CARICOM served as our initial proving ground (featuring `.tt`, `.jm`, `.bb`, Central Bank, IRD, and WiPay integrations), the `REGIONAL_ANCHORS` engine natively supports multiple regional jurisdictions with alias resolution:

- **Caribbean (`caribbean`, `caricom`, `tt`, `jm`)**: 21+ authoritative domains, 11 ccTLDs, CARICOM/OECS economic registries.
- **Latin America (`latam`, `latin_america`, `brazil`, `mexico`)**: Central banks (BACEN, Banxico), tax authorities (SAT, DIAN), Pix/SPEI rails, and major LatAm business media.
- **Southeast Asia (`southeast_asia`, `sea`, `singapore`, `indonesia`)**: MAS, Bank Indonesia, PayNow, DuitNow, Grab/Gojek ecosystems.
- **United States & EU (`us_eu`, `us`, `eu`, `uk`)**: SEC EDGAR, Companies House, HMRC, and pan-European regulatory bodies.
- **Global (`global`)**: Global search unconstrained by territory boundaries.

---

## 🔄 Two-Round Stopping Rationale (The Offline Pivot)

Judges may ask: *Why does the adaptive search loop cap at 2 rounds?*

- **Round 1 (Broad Regional Retrieval)**: Enforces geographic query bounding and gathers authoritative macro, regulatory, and commercial sources.
- **Round 2 (Targeted Gap-Resolution Retrieval)**: The Epistemic Auditor identifies specific missing claims and dispatches targeted queries to resolve those exact voids.
- **The Epistemic Stopping Rule**: If after two rounds of deep retrieval against authoritative regional databases the answer still cannot be found on the public internet, **further scraping only produces diminishing returns, LLM hallucinations, and sycophantic filler**. At this boundary, the only epistemically honest decision is to stop search, declare a **"Field Discovery • Pioneer Opportunity"**, and instruct the founder to gather physical evidence offline using **Vali Co-Pilot** (The Mom Test).

---

## 🧪 Automated Tests
Run the standalone unit test suite verifying query bounding, SGI calculation, and kwargs formatting:
```bash
pytest tests/ -v
```

---

## 🔗 Live Deployments & Provenance
- **Live Staging Platform**: [https://meta-hackathon.research-navigator.ai](https://meta-hackathon.research-navigator.ai)
- **Live Cloud Run Demo Backend**: [https://backend-go-412743311224.us-central1.run.app/health](https://backend-go-412743311224.us-central1.run.app/health)
- **3-Minute Loom Demo Video**: *[Link provided in Devpost Submission]*
- **Raw Provenance Log**: See [`provenance/eval_results.json`](provenance/eval_results.json) for recorded raw execution metrics.

---

## 👥 Authors & Acknowledgments
Built by **Anthony Baptiste** for the **Meta Global AI Developer Hackathon 2026** (Startup Track).  
Special thanks to **Meta AI**, **Baseten**, and **Fireworks AI** for inference credits and open-weights infrastructure.
