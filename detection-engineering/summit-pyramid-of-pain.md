# Summit — Pyramid of Pain Challenge (TryHackMe SOC Level 1)

**Source:** TryHackMe (SOC Level 1 Path — Cyber Threat Intel module)
**Category:** Detection Engineering / Threat Hunting
**Result:** Completed on first attempt

---

## Scenario

Summit is a practical challenge room requiring the analyst to "chase" a simulated adversary progressively up the Pyramid of Pain — starting with the easiest indicators for an attacker to change, and escalating detection to the point where the adversary can no longer evade without abandoning their actual attack methodology (TTPs).

## Investigation & Approach

Worked through a full evidence-driven detection pipeline across the platform's hashes, network logs, command logs, and Sigma rule authoring interface — moving deliberately from low-value indicators to high-value behavioral detection, matching the Pyramid of Pain's ascending structure:

| Pyramid Level | Action Taken |
|---|---|
| **1. Hash Values** | Analyzed a sample file and blocked the malicious MD5 hash |
| **2. IP Address** | Identified and blocked the malicious source IP at the firewall (egress rule) |
| **3. Domain Name** | Blocked the attacker's DNS address |
| **4. Network Artifacts** | Authored a Sigma rule to detect the malicious network traffic pattern |
| **5. Host Artifacts** | Analyzed provided logs and refined the Sigma rule based on findings |
| **6. Tools / TTPs** | Identified a command injection technique in the logs and authored a rule targeting that specific attack behavior — the hardest layer for the adversary to evade |

## Key Takeaway

Each step forced the simulated adversary to expend more effort to evade detection than the last — swapping a hash costs nothing, but abandoning a TTP means changing their entire attack methodology. This is the practical proof of why the Pyramid of Pain matters: **detection built on indicators alone (hashes, IPs) is trivially bypassed, while detection built on TTPs creates lasting pressure on an attacker.**

## MITRE ATT&CK Connection

The final stage of the challenge (command injection detection) ties directly to ATT&CK's **Execution** tactic — reinforcing that TTP-level detection (top of the pyramid) is effectively detection aligned to ATT&CK techniques, not just IOCs.

## Lesson Learned

This was the first challenge where I had to *build* detection logic (Sigma rules) rather than just investigate an existing alert. It reinforced that IOC-based blocking (hash/IP/domain) is necessary but insufficient — real resilience against an adversary comes from detecting their behavior and technique, not just their current infrastructure. It also highlighted the value of methodical enumeration before diving into remediation — the room's debrief specifically noted that mapping all available evidence sources first, rather than looping back reactively, is a core SOC/threat-hunting discipline worth practicing more deliberately next time.
