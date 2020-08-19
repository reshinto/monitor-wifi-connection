import subprocess
import re

IP_DEVICE = "192.168.1.164"

isConnected = False

connected_ips = []
while True:
    # Search for connected ips in network (not consistent and reliable)
    NETWORK = subprocess.Popen(["arp-scan", "-l"], stdout=subprocess.PIPE)
    discovered_network = NETWORK.stdout.read().decode("utf-8")
    ip_candidates = re.findall(
        r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", discovered_network)
    # keep history of connected_ips
    connected_ips = list(set(connected_ips + ip_candidates))
    procs = []
    for ip in connected_ips:
        # use ping to do a stable check if ip is connected to network as arp-scan is not stable
        proc = subprocess.Popen(["ping", ip], stdout=subprocess.PIPE)
        procs.append(proc)
    for i, ip in enumerate(connected_ips):
        for j in range(2):
            line = procs[i].stdout.readline()
            if not line:
                break
            connected_ip = line.decode("utf-8").split()[3][:-1]
            if ip == IP_DEVICE and connected_ip == "icmp_se" and isConnected:
                isConnected = False
                subprocess.Popen(
                    ["say", "Your mobile phone has just disconnected from your network!"])
            if connected_ip == IP_DEVICE and not isConnected:
                isConnected = True
                subprocess.Popen(
                    ["say", "Your mobile phone has just connected to your network!"])
        procs[i].terminate()
