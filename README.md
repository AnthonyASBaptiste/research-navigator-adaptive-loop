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
| **1. The Buzzword Hand-Wave** *(Quantum CRE leasing)* | Yellow (85% conf) | **Field Discovery (42% conf)** | **8** | 56% | Caught ungrounded viral K-factor and zero CAC assumptions. Prescribed 3 pilot experiments. |
| **2. The Contradictory Market** *(US-TT Remittance)* | Yellow (90% conf) | **Field Discovery (44% conf)** | **8** | **100%** | Exposed Central Bank exchange control contradictions. Prescribed Central Bank interviews. |
| **3. The Obscure Regional Niche** *(Dominica LoRaWAN)* | Yellow (85% conf) | **Field Discovery (58% conf)** | **6** | **100%** | Detected zero public LoRaWAN rural data. Prescribed 3-month cooperative sensor test. |
| **4. The Grounded B2B SaaS** *(Shopify VAT plugin)* | Yellow (92% conf) | **Field Discovery (45% conf)** | **6** | **100%** | Caught missing active merchant counts and Inland Revenue API specs. Prescribed 30 discovery interviews. |
| **5. The Unverifiable Consumer Habit** *(Hydration stake)* | Red (94% conf) | **Field Discovery (46% conf)** | **8** | 50% | Refused to treat macro wellness TAM as proof of deposit staking. Prescribed 100-user default pilot. |

### 🎯 Key Benchmark Takeaways
- **Evidentiary Voids Exposed**: **36 critical voids caught** across 5 ventures (Baseline caught **0**).
- **Epistemic Calibration**: Reduced dangerous false confidence from **89.2%** down to an honest **47.0%** (**-42.2% sycophancy reduction**).
- **Regional Moat Integrity**: Achieved **up to 100% Regional Source Grounding Index (SGI)** on Caribbean ventures.
- **Honest Refusal Rate**: **100% (5/5)** refusal to hallucinate certainty on frontier startup concepts.

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
