#!/usr/bin/env python3
"""
CyberSim Mission Completeness Audit
Scans all missions across all data files and reports any missing fields.
Run: python3 audit_missions.py
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.mission_data import MISSIONS, get_mission
from core.mission_data_p2 import MISSIONS_P2
from core.mission_data_p3 import MISSIONS_P3
from core.mission_data_stage34 import STAGE3_MISSIONS, STAGE4_MISSIONS
from core.mission_types import TYPE_LAB, TYPE_THEORY, TYPE_PROJECT, TYPE_CAREER, TYPE_EXTERNAL

# ─── ANSI Colors ──────────────────────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ─── Required fields per difficulty ───────────────────────────────────────────
REQUIRED_FIELDS = {
    "all": ["briefing", "objective", "xp_reward"],
    "lab": ["methods", "tools", "step_by_step_guide", "security_level", "flag"],
}

DIFFICULTIES = ["easy", "normal", "hard"]

def audit_missions():
    """Run the full mission audit."""
    # Collect all missions
    all_missions = {}
    all_missions.update(MISSIONS)
    all_missions.update(MISSIONS_P2)
    all_missions.update(MISSIONS_P3)
    all_missions.update(STAGE3_MISSIONS)
    all_missions.update(STAGE4_MISSIONS)

    print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}║          🔍 CYBERSIM MISSION COMPLETENESS AUDIT             ║{RESET}")
    print(f"{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}")
    print(f"\n  {DIM}Total missions: {len(all_missions)}{RESET}")
    print(f"  {DIM}Checking: briefing, objective, methods, tools, guide, security, XP, flag{RESET}\n")

    total_issues = 0
    total_ok = 0
    mission_issues = {}

    for mid in sorted(all_missions.keys()):
        m = all_missions[mid]
        name = m.get("name", f"Mission {mid}")
        mtype = m.get("type", TYPE_THEORY)
        is_lab = mtype == TYPE_LAB
        issues = []

        for diff in DIFFICULTIES:
            diff_data = m.get(diff)
            if not diff_data:
                issues.append(f"  {RED}✗{RESET} Missing entire '{diff}' difficulty block")
                continue

            # Check required fields for ALL missions
            for field in REQUIRED_FIELDS["all"]:
                if not diff_data.get(field):
                    issues.append(f"  {YELLOW}⚠{RESET} [{diff.upper()}] Missing: {field}")

            # Check additional fields for LAB missions
            if is_lab:
                for field in REQUIRED_FIELDS["lab"]:
                    if not diff_data.get(field):
                        issues.append(f"  {RED}✗{RESET} [{diff.upper()}] Missing: {field}")

            # Check tool detail (should have name, cmd, desc)
            tools = diff_data.get("tools", [])
            for i, tool in enumerate(tools):
                if isinstance(tool, dict):
                    if not tool.get("name"):
                        issues.append(f"  {YELLOW}⚠{RESET} [{diff.upper()}] Tool {i+1} missing 'name'")
                    if not tool.get("cmd"):
                        issues.append(f"  {YELLOW}⚠{RESET} [{diff.upper()}] Tool '{tool.get('name', '?')}' missing 'cmd'")
                    if not tool.get("desc"):
                        issues.append(f"  {YELLOW}⚠{RESET} [{diff.upper()}] Tool '{tool.get('name', '?')}' missing 'desc' (why we use this)")

        if issues:
            total_issues += len(issues)
            mission_issues[mid] = {"name": name, "type": mtype, "issues": issues}
        else:
            total_ok += 1

    # ─── Report ───────────────────────────────────────────────
    if mission_issues:
        print(f"  {RED}{BOLD}ISSUES FOUND:{RESET}\n")
        for mid, info in sorted(mission_issues.items()):
            lab_tag = f" {GREEN}[LAB]{RESET}" if info["type"] == TYPE_LAB else f" {DIM}[THEORY]{RESET}"
            print(f"  {BOLD}Mission {mid}: {info['name']}{RESET}{lab_tag}")
            for issue in info["issues"]:
                print(f"    {issue}")
            print()
    else:
        print(f"  {GREEN}No issues found!{RESET}")

    # Summary
    print(f"\n{BOLD}{'═' * 62}{RESET}")
    print(f"  {GREEN}✅ Missions OK:       {total_ok}{RESET}")
    print(f"  {YELLOW}⚠  Missions with gaps: {len(mission_issues)}{RESET}")
    print(f"  {RED}Total issues:         {total_issues}{RESET}")
    print(f"  {DIM}Theory missions (no tools/methods) are expected.{RESET}")
    print(f"{BOLD}{'═' * 62}{RESET}\n")

    return total_issues


if __name__ == "__main__":
    issues = audit_missions()
    sys.exit(0 if issues == 0 else 1)
