# ARP Poisoning & Man-in-the-Middle Attack — Self-Directed Home Lab

**Type:** Original, self-scoped lab (not a guided platform exercise)
**Environment:** Kali Linux VM (attacker) + physical Windows PC (victim), both connected via a shared mobile hotspot
**Tools used:** `arpspoof`, `arp-scan`, `nmap`, Wireshark

---

## Objective

Gain practical understanding of ARP poisoning by performing an actual man-in-the-middle attack on a device that I own, over a network I control — and verifying the attack's impact with packet capture on both ends.

## Why ARP Poisoning Works

No authentication exists for ARP (Address Resolution Protocol) traffic: any device on a local network can send a reply to an ARP request saying "I am the device owning X address," and all other devices will believe it without question. By exploiting this, an attacker can poison ARP tables of two participants (a victim and a network gateway) with fake ARP replies: "I am the other participant."

## Setup

**Network:** Attacker and victim connected to the same mobile hotspot, creating a shared local subnet.

**Initial obstacle:** My Kali VM was set to **NAT mode** (by VirtualBox default), which gave it an isolated virtual IP and effectively prevented interaction with the real world victim device on the hotspot. Setting the VM's network adapter to **Bridged Mode** fixed this problem, providing Kali a legitimate IP address within the same subnet as the hotspot.

**Host discovery**, done properly:
```bash
sudo arp-scan --localnet
```
This showed three machines within the subnet: the gateway (`192.168.84.5`), the attacker (`192.168.84.71`, i.e., Kali), and the victim machine (`192.168.84.74`).

## Performing the Attack

```bash
sudo sysctl -w net.ipv4.ip_forward=1

sudo arpspoof -i eth0 -t 192.168.84.74 192.168.84.5
sudo arpspoof -i eth0 -t 192.168.84.5 192.168.84.74
```

The first line sends an ARP reply poison message to the victim machine that makes it believe Kali is its default gateway; the second line poisons the gateway with similar information about the victim. The first line is absolutely necessary – otherwise the attack will disconnect the victim machine from the internet rather than just intercept its communication.

## Validating the Attack

**On the victim, filtering Wireshark by `arp`:** saw a large number of unsolicited ARP replies saying that `192.168.84.5 is at [Kali's MAC address]`. The confirmation that this was real came by comparing Kali's actual MAC address (`ip link show eth0`) against the one in those replies.

**On the attacker (Kali), clearing the ARP filter:** saw victim's traffic — TLS, DHCP, TCP — directly captured in Kali's own packet capture window. Filtering for plaintext HTTP traffic found a legitimate OCSP request (`o.pki.goog`), in full plaintext form — including the headers, User-Agent, and content type — confirming that even browsers using HTTPS make requests in plaintext.

## Main Discovery: HTTPS Defeats Content Reading, Not Position

TLS traffic was clearly visible as flowing through the intercepted connection (confirming the MITM position was real), but its contents could not be read. This is a useful, practical distinction: **successful positioning as a man-in-the-middle does not guarantee the ability to read data** — HTTPS specifically prevents the "reading the content" step of an attack, regardless of whether or not the "interception" step succeeds.

## Limitations and Honest Gaps

The lab was thorough in covering the **attack and detection** phases, but the **defense phase** — adding a static ARP entry for the gateway's MAC address and then trying the attack again to see that it no longer works — was not done. This is clearly the next logical step: static ARP entries will not allow an ARP table to be over-written, which is the counter measure to all of the above demonstrations.

## Lesson Learned

Performing this attack, rather than just reading about it, brought home in a practical way how the attack really worked in ways that theory had not. Seeing the wrong MAC address in the packet in Wireshark, and seeing packets that were actually part of live traffic (even down to a specific HTTP request) going through a network under my control, turned the abstraction of "man-in-the-middle" into an observable event, rather than an assumption. It also provided a very practical lesson learned that has nothing at all to do with the attack itself: the mode of the virtual machine's network adapter (NAT or Bridged) is critical when doing any lab that requires the VM to communicate with devices on the local network.
