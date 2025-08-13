import subprocess
import sys

# Liste des packages pip à installer
pip_packages = [
    "pillow",        # pour PIL.Image, PIL.ImageTk
    "pywin32",       # pour win32gui, win32con
    "pynput",        # pour keyboard et mouse
    "pygame"         # pour pygame
]

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[OK] {package} installé")
    except subprocess.CalledProcessError:
        print(f"[ERREUR] Impossible d'installer {package}")

def main():
    print("=== Installation des packages requis ===")
    for pkg in pip_packages:
        install_package(pkg)
    print("=== Vérification des modules intégrés ===")
    try:
        import ctypes, os, sys, threading, time, tkinter, winreg, shutil, subprocess, random, string
        print("[OK] Modules intégrés présents")
    except ImportError as e:
        print(f"[ERREUR] Module intégré manquant : {e}")

if __name__ == "__main__":
    main()
