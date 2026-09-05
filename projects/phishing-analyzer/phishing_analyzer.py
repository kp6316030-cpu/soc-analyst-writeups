import email
import re
import os
import requests

VT_API_KEY = os.environ.get("VT_API_KEY")

# Step 1: Load the email
with open("sample_phishing.eml", "r") as f:
    msg = email.message_from_file(f)

print("=== Basic Email Info ===")
print("From:", msg["From"])
print("Subject:", msg["Subject"])

print("\n=== Security Headers ===")
print("Originating IP:", msg["X-Originating-Ip"])
print("Authentication Results:", msg["Authentication-Results"])

# Step 2: Parse SPF/DKIM/DMARC
auth_results = msg["Authentication-Results"] or ""
spf_match = re.search(r"spf=(\w+)", auth_results)
dkim_match = re.search(r"dkim=(\w+)", auth_results)
dmarc_match = re.search(r"dmarc=(\w+)", auth_results)

print("\n=== Parsed Authentication Results ===")
print("SPF:", spf_match.group(1) if spf_match else "Not found")
print("DKIM:", dkim_match.group(1) if dkim_match else "Not found")
print("DMARC:", dmarc_match.group(1) if dmarc_match else "Not found")

# Step 3: Get body and extract URLs
body = ""
if msg.is_multipart():
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            body = part.get_payload(decode=True).decode(errors="ignore")
else:
    body = msg.get_payload(decode=True).decode(errors="ignore")

urls = re.findall(r'href="(http[^"]+)"', body)

print("\n=== URLs Found in Body ===")
for url in urls:
    print(url)

# Step 4: Sender legitimacy check
from_header = msg["From"] or ""
display_name_match = re.search(r'"([^"]+)"', from_header)
email_domain_match = re.search(r'@([\w.-]+)', from_header)

print("\n=== Sender Legitimacy Check ===")
mismatch_detected = False
if email_domain_match:
    actual_domain = email_domain_match.group(1)
    if display_name_match:
        display_name = display_name_match.group(1)
    else:
        display_name = from_header.split("<")[0].strip()

    print(f"Display Name: {display_name}")
    print(f"Actual Sending Domain: {actual_domain}")
    if actual_domain.lower() not in display_name.lower():
        print("WARNING: Display name does not match sending domain - possible spoofing")
        mismatch_detected = True
    else:
        print("Display name and domain appear consistent")
else:
    print("Could not extract sender domain")

# Step 5: Defang IOCs
def defang(indicator):
    return indicator.replace(".", "[.]")

print("\n=== Defanged IOCs ===")
ip_clean = msg["X-Originating-Ip"].strip("[]") if msg["X-Originating-Ip"] else None
if ip_clean:
    print("IP:", defang(ip_clean))
else:
    print("IP: N/A")
for url in urls:
    print("URL:", defang(url))

# Step 6: VirusTotal check (only if we have a real IP)
def check_ip_virustotal(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": VT_API_KEY}
    response = requests.get(url, headers=headers)

    print(f"DEBUG: Status Code: {response.status_code}")
    print(f"DEBUG: Response: {response.text[:300]}")

    if response.status_code == 200:
        data = response.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]
        malicious_count = stats["malicious"]
        total_engines = sum(stats.values())
        return malicious_count, total_engines
    else:
        return None, None

print("\n=== VirusTotal IP Reputation ===")
vt_malicious = None
if ip_clean:
    malicious_count, total_engines = check_ip_virustotal(ip_clean)
    if malicious_count is not None:
        print(f"Flagged malicious by {malicious_count}/{total_engines} security vendors")
        vt_malicious = malicious_count > 0
    else:
        print("Could not retrieve VirusTotal data (check API key or rate limit)")
else:
    print("No IP address available to check")

print("\n=== FINAL VERDICT ===")
if vt_malicious:
    print("Verdict: MALICIOUS")
    print("Reason: IP flagged by VirusTotal as malicious by one or more security vendors.")
elif mismatch_detected:
    print("Verdict: SUSPICIOUS / LIKELY PHISHING")
    print("Reason: Sender display name does not match actual domain.")
    print("Note: VirusTotal did not flag the IP, but IP reputation checks only catch")
    print("      previously-reported infrastructure — a clean IP does NOT mean the")
    print("      email is safe. The domain/display-name mismatch remains the stronger")
    print("      signal here and should not be dismissed based on IP reputation alone.")
else:
    print("Verdict: Likely legitimate")
    print("Reason: Sender domain matches display name, authentication checks passed,")
    print("        and no malicious indicators found via VirusTotal.")
