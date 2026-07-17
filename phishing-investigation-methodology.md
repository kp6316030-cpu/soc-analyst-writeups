# My Phishing Alert Investigation Methodology

*A personal reference checklist, built from hands-on practice across TryHackMe's Phishing module and LetsDefend live alerts. Improved after diagnosing a 47% → 85% false-positive accuracy jump on a repeated scenario.*

---

## Step 1 — Initial Triage (first glance)

Before deep investigation, quickly assess:

1. **Alert severity** — Low / Medium / High / Critical, to gauge priority
2. **Alert summary** — read what triggered it
3. **Sender email address** — is the domain known/legitimate, or unfamiliar/suspicious?
4. **Subject line** — does it use urgency/pressure language ("act now," "your account will be closed")?
5. **Attachment/URL presence** — note if there's a file or link, since this determines what tools I'll need next

## Step 2 — Header & SIEM Deep Dive

Once an alert warrants real investigation:

1. Pull the **raw email source** / SIEM logs — check the **originating IP**
2. Check the `Authentication-Results` header — three checks, each pass/fail:
   - **SPF** (Sender Policy Framework) — is the sending server authorized for this domain?
   - **DKIM** (DomainKeys Identified Mail) — cryptographic signature confirming the email wasn't altered and is really from the claimed domain
   - **DMARC** — the policy layer defining what happens if SPF/DKIM fail (reject/quarantine/allow); a DMARC fail is a strong spoofing signal
3. Check any embedded URLs — the **actual redirect destination**, not just the display text (hover/inspect, don't trust what's shown)
4. Check for **display name vs. actual domain mismatch** (e.g., "Home Depot" ← `support@teckbe.com`) — a classic phishing tell

## Step 3 — Sandbox / File-URL Analysis

1. Submit the suspicious link or attachment to a sandbox tool
2. **If the tool gives a verdict only** (e.g., LetsDefend's built-in sandbox) — trust the verdict for fast triage
3. **If the tool exposes behavioral detail** (e.g., Any.Run) — check network connections made, files dropped, processes spawned, registry changes, rather than relying on the verdict alone. Real-world malware increasingly includes sandbox-evasion logic designed to produce a false "safe" result, so behavioral evidence matters more than a single verdict when it's available.

## Step 4 — Documentation

Every closed alert gets a written note with:

1. **Time of incident**
2. **Verdict** — True Positive / False Positive
3. **Reasoning** — what specific evidence led to that verdict (header results, sandbox findings, IOCs)
4. **Escalation decision** — closed at my level, or escalated to L2?

---

## Bonus — Quick Process/Execution Alert Triage (adjacent skill)

Not every alert is phishing. For process execution alerts specifically:

- Recognize common **legitimate Windows processes/behavior** (e.g., `TrustInstaller` running is normal) to avoid over-investigating benign noise
- Basic commands (`mkdir`, file creation, etc.) are often not malicious on their own
- **Red flag:** a legitimate-sounding process running from an **unexpected file path** (e.g., not from `System32`) — this warrants deeper investigation even if the process name looks familiar

---

### Note on how this was built

This checklist wasn't copied from a template — it was reconstructed by walking through my own actual practice step by step, correcting vague answers ("I check for anything wrong," "the sandbox just tells me") into specific, named indicators. Two real gaps were caught and fixed in the process: DMARC/DKIM terminology needed tightening, and I confirmed the LetsDefend sandbox genuinely only exposes a binary verdict (not a tool limitation I was missing, but a real constraint worth knowing when comparing tools).
