#!/usr/bin/env python3
"""
Research Navigator — Vali Validation Co-Pilot Simulator
Meta Global AI Developer Hackathon 2026 (Startup Track)

Simulates the autonomous WhatsApp validation co-pilot (Vali) powered by Meta Llama 3.3 70B (Fireworks AI).
Enables judges to test customer discovery synthesis, evidence logging, and Mom Test coaching
WITHOUT needing any WhatsApp Cloud API credentials or Meta developer phone numbers.

Usage:
  python vali_simulator.py --sample           # Runs sample founder interview synthesis
  python vali_simulator.py --interactive      # Type your own field interview observations
"""

import os
import sys
import json
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
DIM = "\033[2m"
RESET = "\033[0m"

SAMPLE_VENTURE = "Shopify plugin for automated VAT calculation and tax authority compliant e-invoicing for regional Caribbean eCommerce merchants."
SAMPLE_EXPERIMENTS = [
    "Conduct structured discovery interviews with at least 30 Caribbean Shopify merchants to quantify compliance pain, current manual costs, and willingness to pay.",
    "Build a minimal prototype connecting to one regional tax authority's e-invoicing endpoint with a local merchant to test technical feasibility."
]

SAMPLE_INTERVIEW_TRANSCRIPT = """
Just finished interviewing Marcus, who runs 'Island Craft Goods' on Shopify Plus in Port of Spain.
He ships locally and to Barbados and Jamaica. He told me:
'Right now, my accountant spends 5 hours every Friday manually pulling Shopify CSV reports,
calculating the 12.5% VAT for Trinidad orders, and filling out the Inland Revenue e-Tax portal.
We got hit with a $4,500 penalty last year because of a reconciliation mismatch between our WiPay
gateway and Shopify. If someone had an app that pushed the invoices automatically to the IRD API,
I would gladly pay $50 a month without blinking.'
"""


async def run_simulation(transcript: str, venture: str = SAMPLE_VENTURE, experiments: list = None):
    try:
        from adaptive_loop import ValiCopilot
    except ImportError:
        sys.path.insert(0, str(Path(__file__).parent))
        from adaptive_loop import ValiCopilot

    print(f"\n{BOLD}{CYAN}================================================================================{RESET}")
    print(f"{BOLD}{CYAN}  🤖 Vali — Autonomous Startup Validation Co-Pilot Simulator{RESET}")
    print(f"{DIM}  Model: Meta Llama 3.3 70B via Fireworks AI | Framework: Google ADK / Hermes{RESET}")
    print(f"{BOLD}{CYAN}================================================================================{RESET}\n")

    print(f"{BOLD}🎯 Active Venture Context:{RESET}")
    print(f"  {venture}")
    print(f"\n{BOLD}📋 Prescribed Discovery Experiments:{RESET}")
    for i, exp in enumerate(experiments or SAMPLE_EXPERIMENTS, 1):
        print(f"  {i}. {exp}")

    print(f"\n{BOLD}{MAGENTA}💬 Inbound Founder Field Voice Note / Message:{RESET}")
    print(f"{DIM}\"\"\"{RESET}{transcript.strip()}{DIM}\"\"\"{RESET}\n")

    print(f"{CYAN}⏳ Vali analyzing interview evidence against Mom Test criteria...{RESET}")
    vali = ValiCopilot()
    result = await vali.process_founder_input(
        founder_message=transcript,
        venture_idea=venture,
        prescribed_experiments=experiments or SAMPLE_EXPERIMENTS
    )

    print(f"\n{BOLD}{GREEN}=================== VALI CO-PILOT SYNTHESIS ==================={RESET}")
    print(f"{BOLD}Coach Feedback:{RESET}\n  {result.get('coach_response')}\n")

    print(f"{BOLD}{YELLOW}Extracted Empirical Evidence (Mom Test Compliant):{RESET}")
    for ev in result.get("extracted_evidence", []):
        print(f"  • {ev}")

    print(f"\n{BOLD}{CYAN}Experiment Progress Update:{RESET}")
    print(f"  {result.get('experiment_progress')}")

    print(f"\n{BOLD}{GREEN}Next Field Action:{RESET}")
    print(f"  {result.get('suggested_next_step')}\n")
    print(f"{BOLD}{GREEN}==============================================================={RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Vali Co-Pilot Simulator")
    parser.add_argument("--sample", action="store_true", help="Run sample Caribbean merchant interview")
    parser.add_argument("--interactive", action="store_true", help="Interactive interview input")

    args = parser.parse_args()

    if args.interactive:
        print(f"{BOLD}Enter founder field observation / customer interview quote:{RESET}")
        text = input("> ")
        if text.strip():
            asyncio.run(run_simulation(text))
        else:
            print("No input provided. Running sample interview.")
            asyncio.run(run_simulation(SAMPLE_INTERVIEW_TRANSCRIPT))
    else:
        asyncio.run(run_simulation(SAMPLE_INTERVIEW_TRANSCRIPT))


if __name__ == "__main__":
    main()
