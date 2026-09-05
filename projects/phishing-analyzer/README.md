# Phishing Email Analyzer — Python Automation Tool

**Type:** Self-built (original project, not guided lab)
**Language:** Python 3
**Libraries:** `email`, `re`, `os`, `requests`
**External API:** VirusTotal v3 (IP reputation)

---

## Motivation

Having analyzed dozens of phishing emails manually across TryHackMe's Phishing module and developing my personal methodology for it (please refer to [phishing-investigation-methodology.md](../phishing-investigation-methodology.md)), I decided to automate the first three steps of this methodology: **initial triage -> header/siem analysis -> basic threat intel enrichment**. The intention was not to automate the part that needs analyst's judgment, but to make the process less manual and allow concentrating on the truly analytical parts.

## What the Script Does

For a given `.eml` file, the script:

1. Gets sender, subject, and headers (`X-Originating-IP`, `Authentication-Results`) 
2. Parses SPF/DKIM/DMARC results individually out of the raw header string using regex  
3. Extracts URLs from HTML body
4. Detects **mismatch between display name and actual sending domain** ("Home Depot" sent from `teckbe.com`)
5. Defangs all found IOCs (IPs, URLs) automatically
6. Checks **VirusTotal API** to get reputation of the sending IP across 90 security vendors  
7. Gives a final verdict taking into account several factors at once, instead of relying on just one check 

## Sample Output (Phishing Email)

```
From: "Thank you! Home Depot" <support@teckbe.com>
Subject: Order Placed: Your Order ID OD2321657089291 Placed Successfully

=== Sender Legitimacy Check ===
Display Name: Thank you! Home Depot
Actual Sending Domain: teckbe.com
WARNING: Display name does not match sending domain - possible spoofing

=== VirusTotal IP Reputation ===
Flagged malicious by 0/90 security vendors

=== FINAL VERDICT ===
Verdict: SUSPICIOUS / LIKELY PHISHING
Reason: Sender display name does not match actual domain.
Note: VirusTotal did not flag the IP, but IP reputation checks only catch
      previously-reported infrastructure — a clean IP does NOT mean the
      email is safe. The domain/display-name mismatch remains the stronger
      signal here and should not be dismissed based on IP reputation alone.
```

## Key Findings While Building This

**1. A blunt spoofing rule generates false positives for legitimate third-party senders.**
Feeding the script a real, non-spoofed email ("IPO allotment notice" from "DEEPA JEWELLERS LIMITED" sent via `bigshareonline.com`, a known Indian share registrar) resulted in the same "display name mismatch" warning as the actual phishing sample. This is an expected pattern for legitimate business emails, where the company uses third party registrars/payroll providers/etc whose domain genuinely does not match. Instead of removing the check , I changed the verdict logic from an absolute claim to a flagged item that requires context because a single signal of an unmatched domain cannot confirm the spoofing.

**2. Checking the reputation of IPs may fail to catch compromised or freshly created infrastructure for attacks.**
The confirmed phishing message's sending IP returned **0/90 malicious** according to VirusTotal checks. That is not a flaw of the tool but a logical feature: IP becomes flagged after being previously submitted to vendors as suspicious. Therefore, a newly created infrastructure for conducting a phishing attack will not flag as malicious by reputation alone, hence **VirusTotal check is not a guarantee of security**.

**3. Header formats in emails vary more widely than I have expected.**
At first, I supposed display names always use quotation marks (`"Home Depot" <email>`). It is quite common but does not happen always — an email sent by an Indian company had unquoted display name format (`DEEPA JEWELLERS LIMITED <email>`), which caused a runtime error. In order to fix it, both display names formats should be processed separately.

## Design Decision: Correlated Verdict Instead of Simple Rule

Final verdict decision starts with VirusTotal checks (confirmed malicious IP address is definitive evidence), then uses display name check (suspicious flag but clearly caveated, not definitive on its own), and reports "likely legitimate" verdict if neither check fires. This reflects an important takeaway from the SOC training this month: true detection depends on correlating **multiple signals**, not single indicators.

## Setup

Free VirusTotal API key needed (`virustotal.com` → Profile → API Key).

```bash
export VT_API_KEY="your_key_here"
python3 phishing_analyzer.py
```

## Next Steps

- URL reputation checks in addition to IP (using VirusTotal URL endpoint)
- Domain age WHOIS lookup (brand new domains are clear phishing signs)
- Command line arguments for analyzing any `.eml` file without modifying the script
