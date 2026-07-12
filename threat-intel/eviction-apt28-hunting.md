# Eviction, Proactive Threat Hunting with ATT&CK Navigator (TryHackMe SOC Level 1)

**Source:** TryHackMe (SOC Level 1 Path, Cyber Threat Intel module)  
**Category:** Threat Intelligence, Proactive Threat Hunting  
**Tool used:** MITRE ATT&CK Navigator  

---

## Scenario

Sunny, a SOC analyst at E-corp, a manufacturer of rare earth metals for both government and private clients, receives classified intelligence that APT28 may target organizations like E-corp. Instead of waiting for an alert, the task is to use the MITRE ATT&CK Navigator to map APT28's known tactics, techniques, and procedures (TTPs) and search for signs that the group has already made entry. This anticipates their next likely move based on documented behavior instead of just reacting to any alerts that appear.

## Approach

Sunny worked through a step-by-step attacker-lifecycle exercise, using APT28's documented techniques to think through what actions the group might take at each stage:

- Identified the technique APT28 would use to gain **initial access** (phishing).
- Thought about which accounts or assets the group would target **next** if they gained initial access.
- Determined the next action APT28 would take after securing a foothold (moving towards further compromise).
- Identified which **scripting interpreters** to look for based on APT28's documented execution techniques if the initial technique worked.

## Key Takeaway

This exercise shifted threat hunting from reactive to **predictive**. Instead of only looking into what an alert flags, the goal is to use a specific adversary's known TTPs to anticipate their *next* move and search for evidence before it triggers a standard alert. APT28, like most APT groups, has established behavior patterns. They don’t use every technique available; they have preferences. Understanding these preferences allows an analyst to hunt intentionally rather than wait idly.

**Core principle:** *If you don’t understand the full attack surface and the adversary's typical progression, you can’t effectively anticipate or respond to their next move — you’re limited to reacting after it happens.*

## MITRE ATT&CK Connection

This exercise applies the ATT&CK framework practically, using **ATT&CK Navigator** to map a known threat actor's TTP chain and build an active hunting hypothesis instead of just labeling an incident after it occurs.

## Lesson Learned

Threat intelligence is not just background material — it’s something you can act upon. Mapping a known APT group's TTP sequence in Navigator transforms abstract threat intel into a concrete checklist for hunting. Given that technique X worked, what does this specific group usually do next, and where should I be focusing my attention now? This skill is significantly more advanced than alert-driven investigation, and it fosters the proactive mindset that sets threat hunting apart from basic alert triage.
