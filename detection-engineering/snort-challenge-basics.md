# Snort Challenge - The Basics (TryHackMe SOC Level 1)

**Source:** TryHackMe (SOC Level 1 Path - Network Security & Traffic Analysis module)  
**Category:** Intrusion Detection / Network Security  
**Tool used:** Snort (open-source IDS/IPS)

---

## Scenario

This hands-on challenge focuses on applying Snort fundamentals by writing and testing actual detection rules against network traffic instead of just learning theoretically.

## What Snort Does

Snort is an open-source IDS/IPS that examines live or recorded network traffic based on a set of defined rules. It generates alerts or blocks traffic in IPS mode when traffic matches a rule's pattern.

## Rule Writing

I wrote and tested detection rules using Snort's rule syntax, which includes action, protocol, source IP and port, direction, destination IP and port, and rule options.

**Example rule written during the challenge:**
```
alert icmp 192.168.1.56 any <> any any (msg:"ICMP Packet From"; sid:100001; rev:1;)
```

**Breakdown:**
| Component | Value | Meaning |
|---|---|---|
| Action | `alert` | Log and generate an alert (does not block traffic) |
| Protocol | `icmp` | Matches ICMP traffic specifically |
| Source | `192.168.1.56 any` | Source IP, any port (ICMP has no ports) |
| Direction | `<>` | Bidirectional traffic |
| Destination | `any any` | Any destination IP and port |
| `msg` | `"ICMP Packet From"` | Message displayed when the alert triggers |
| `sid` | `100001` | Unique Snort rule identifier |
| `rev` | `1` | Rule revision number |

## Key Takeaway

Writing a Snort rule means specifying exactly what traffic to match (protocol, IP, port, direction) and what action to take when it matches (alert or block). This practical experience ties directly to the theory of IDS/IPS. Instead of just knowing that Snort can detect ICMP sweeps or suspicious traffic, this challenge required me to define the exact match criteria myself.

## Connection to Broader Concepts

This relates directly to the IDS versus IPS distinction discussed earlier in the module. The `alert` action used here is IDS behavior (detect and notify). Snort can also be set up in IPS mode using a `drop` or `reject` action, which actively blocks matching traffic rather than just logging it.

## Lesson Learned

Writing rules demands precision that simple understanding cannot provide. Getting the source/destination direction operator (`<>` versus `->`) or the protocol wrong affects what the rule catches. This serves as a reminder that in real detection work, a rule that is "close" but not exact can either miss actual threats or overwhelm analysts with false positives.
