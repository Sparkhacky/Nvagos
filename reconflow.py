#!/usr/bin/env python3
"""
reconflow.py - Suite de reconocimiento de red con Nmap
Autor: Maikol (Bootcamp The Bridge)
Descripción: Herramienta modular en Python para automatizar diferentes tipos de escaneos Nmap con modos de velocidad.
"""
import subprocess
import sys
import os
from datetime import datetime

# Colores ANSI
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

# Banner más elaborado
def show_banner():
    banner = r"""
███╗   ██╗██████╗ ██╗   ██╗ █████╗ ████████╗
████╗  ██║██╔══██╗██║   ██║██╔══██╗╚══██╔══╝
██╔██╗ ██║██║  ██║██║   ██║███████║   ██║   
██║╚██╗██║██║  ██║██║   ██║██╔══██║   ██║   
██║ ╚████║██████╔╝╚██████╔╝██║  ██║   ██║   
╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   

            Nvagos - Suite de Reconocimiento Nmap
"""
    print(MAGENTA + banner + RESET)

# Ejecutar comando shell
def run_command(cmd):
    print(f"{CYAN}[+]{RESET} Ejecutando: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"{RED}[!]{RESET} Error al ejecutar: {cmd}")

# Crear directorio de salida
def make_output_dir(ip):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dir_name = f"recon_{ip.replace('/', '_')}_{timestamp}"
    os.makedirs(dir_name, exist_ok=True)
    print(f"{GREEN}[+] Directorio de resultados: {dir_name}{RESET}\n")
    return dir_name

# Selección de velocidad
def choose_speed():
    speeds = [("Normal (T4)", "-T4"), ("Agresivo (T5)", "-T5"), ("Sigiloso (T1)", "-T1")]
    print(f"{MAGENTA}--- Selecciona Modo de Escaneo ---{RESET}")
    for idx, (name, _) in enumerate(speeds, 1):
        print(f" {CYAN}{idx}{RESET}) {name}")
    choice = input(f"{GREEN}Modo:{RESET} ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(speeds):
        return speeds[int(choice)-1][1]
    print(f"{RED}Selección inválida, usando Normal (T4).{RESET}")
    return '-T4'

# Función genérica de escaneo
def run_nmap(ip, outdir, flags, label):
    print(f"{YELLOW}[#]{RESET} {label} en {ip}\n")
    cmd = f"nmap {flags} {ip} -oN {outdir}/{label.replace(' ', '_').lower()}.txt"
    run_command(cmd)
    print()

# Menú interactivo
def interactive_menu(ip):
    outdir = make_output_dir(ip)
    options = [
        ("Escaneo completo", lambda: run_nmap(ip, outdir, f"-A {choose_speed()}", "Escaneo_Completo")),
        ("Escaneo furtivo SYN", lambda: run_nmap(ip, outdir, "-sS -T2", "Escaneo_Furtivo")),
        ("Detección de versiones", lambda: run_nmap(ip, outdir, f"-sV {choose_speed()}", "Deteccion_Versiones")),
        ("Detección de SO", lambda: run_nmap(ip, outdir, f"-O {choose_speed()}", "Deteccion_SO")),
        ("Escaneo de vulnerabilidades", lambda: run_nmap(ip, outdir, f"--script vuln {choose_speed()}", "Escaneo_Vulnerabilidades")),
        ("Salir", None)
    ]
    while True:
        print(f"{MAGENTA}--- Menú Nvagos ---{RESET}")
        for idx, (desc, _) in enumerate(options, 1):
            print(f" {CYAN}{idx}{RESET}) {desc}")
        choice = input(f"{GREEN}Opción:{RESET} ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            idx = int(choice) - 1
            if options[idx][1] is None:
                print(f"{BLUE}Saliendo...{RESET}")
                break
            options[idx][1]()
        else:
            print(f"{RED}Opción inválida{RESET}")

# Ejecución principal
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <IP o rango>")
        sys.exit(1)
    target = sys.argv[1]
    show_banner()
    interactive_menu(target)
