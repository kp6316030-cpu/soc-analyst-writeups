# TryHackMe SOC Level 1 — Path Completion Reflection

**Path:** TryHackMe SOC Level 1 (100% complete)
**Duration:** ~1 month
The modules included are: SOC Fundamentals, Cyber Threat Intelligence (covering the Kill Chain, Unified Kill Chain, MITRE ATT&CK, and the Pyramid of Pain), Phishing Analysis, Network Security and Traffic Analysis (using Snort, Wireshark, NetworkMiner, and IDS/IPS), Web Attack Detection (including SQLi, XSS, Web Shells, and Web DDoS), Windows Logging and Threat Detection, Linux Logging and Threat Detection, SIEM Log Analysis (with Splunk and Elastic), and the complete set of incident investigation challenge rooms (Summit, Eviction, ItsyBitsy, and Benign).

---

## What This Path Actually Covered

This wasn't a single skill — it was the full SOC analyst investigation lifecycle, built module by module:

- **Frameworks first** (Kill Chain, MITRE ATT&CK, Pyramid of Pain) — the vocabulary and mental models used to describe *any* attack, regardless of platform
- **Attack surface knowledge** (phishing, web attacks, network-level attacks) — recognizing what an attack actually looks like at the technical level
- **OS-level detection** (Windows and Linux logging/threat detection, run in parallel) — understanding how the same attack lifecycle (initial access → first actions → persistence) manifests differently depending on the operating system
- **Tooling** (Snort, Wireshark, NetworkMiner, Splunk, Elastic) — the actual instruments used to see and confirm what frameworks predict
- **Synthesis** (Summit, Eviction, ItsyBitsy, Benign) — full investigations requiring all of the above at once, under a realistic incident scenario

What actually stuck and what required repetition

Being honest about this matters more than just listing completed rooms:

- **Cyber Kill Chain order** needed correcting three separate times before it held reliably — it kept getting confused with MITRE ATT&CK's tactic names, since both frameworks describe attack progression but use different terminology
- It took me four attempts to explain the difference between Web-layer (L7) DDoS and network-layer DDoS in my own words rather than just restating the definition
- At first, Sysmon was mistaken for the native Windows Event Logs (it was assumed that event IDs 4624 and 4625 were Sysmon IDs when in fact they are native Windows Security Log IDs).
- In contrast, **Linux logging, Snort rule syntax, and MITM/TLS fingerprint detection** landed cleanly on the first real attempt — these built more naturally on concepts (Bash scripting, general networking) I already had some foundation in

The rule was that concepts which overlapped with the frameworks I had not yet fully internalised required a lot of repetition, while those that related to hands-on skills I had already come across were understood more quickly.

## Practical Work That Came Out of This Path

- **7+ GitHub writeups** spanning malware analysis, live SOC alert investigation (real CVEs: CVE-2024-3400, CVE-2024-49138), detection engineering (Snort rule writing), and threat hunting (MITRE ATT&CK Navigator against a named APT group)
- **A self-built phishing investigation methodology** — a personal, reusable 4-step checklist (Initial Triage → Header/SIEM Deep Dive → Sandbox Analysis → Documentation), built by explaining my own actual process rather than copying a template
- **An independently-scoped home lab** — ARP poisoning/MITM attack, executed and detected via Wireshark on my own local network, going beyond the guided path content

## Biggest Takeaway

Initially I thought that the work involved in SOC meant being able to quickly identify obviously malicious activity. The true lesson—most clearly demonstrated by the Benign and ItsyBitsy challenge rooms—is that the majority of the work consists of careful, detailed searching: linking together small log entries which, on their own, are not noteworthy when looked at individually in order to form a full picture. Nothing about it is immediately apparent; it is necessary to deliberately examine each entry rather than expecting patterns to become obvious.

## What's Next

- Continue building on this foundation with the Google Cybersecurity Professional Certificate (in progress) and CompTIA Security+ (in progress)
- Apply this framework knowledge (Kill Chain, ATT&CK) and hands-on tooling (SIEM, Snort, Wireshark) directly in further live alert investigation on LetsDefend
- Build a Python-based phishing triage tool that operationalizes the investigation methodology developed during this path
