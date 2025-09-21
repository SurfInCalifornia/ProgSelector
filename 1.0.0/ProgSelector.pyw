import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(SCRIPT_DIR, "logo2.ico")
DNSPY_PATH = r"C:\dnSpy\dnSpy.exe"

def find_best_visual_studio():
    base_path = r"C:\Program Files\Microsoft Visual Studio"
    if not os.path.exists(base_path):
        return None
    edition_priority = ["Enterprise", "Professional", "Community", "BuildTools"]
    best_path = None
    best_score = (-1, -1)
    for version in os.listdir(base_path):
        version_path = os.path.join(base_path, version)
        if not os.path.isdir(version_path) or not version.isdigit():
            continue
        version_int = int(version)
        for idx, edition in enumerate(edition_priority):
            devenv_path = os.path.join(version_path, edition, "Common7", "IDE", "devenv.exe")
            if os.path.exists(devenv_path):
                score = (version_int, len(edition_priority) - idx)
                if score > best_score:
                    best_score = score
                    best_path = devenv_path
    return best_path

VS_PATH = find_best_visual_studio()

def check_program_paths():
    vs_installed = VS_PATH is not None
    dnspy_installed = os.path.exists(DNSPY_PATH)
    return vs_installed, dnspy_installed

def open_with_vs(file_path):
    try:
        subprocess.Popen([VS_PATH, file_path])
        sys.exit()
    except Exception as e:
        show_error(f"Failed to open '{os.path.basename(file_path)}' with Visual Studio.\n\nError details:\n{e}")

def open_with_dnspy(file_path):
    try:
        subprocess.Popen([DNSPY_PATH, file_path])
        sys.exit()
    except Exception as e:
        show_error(f"Failed to open '{os.path.basename(file_path)}' with dnSpy.\n\nError details:\n{e}")

def show_error(message):
    messagebox.showerror("Error", message)

def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("DLL or EXE files", "*.dll *.exe")],
        title="Select a DLL or EXE file"
    )
    if file_path:
        handle_file(file_path)

def handle_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.dll':
        show_selection_screen(file_path, is_exe=False)
    elif ext == '.exe':
        show_selection_screen(file_path, is_exe=True)
    else:
        show_unsupported_file_type()

def show_selection_screen(file_path, is_exe):
    vs_installed, dnspy_installed = check_program_paths()
    root = tk.Tk()
    root.title("Choose Program")
    root.geometry("450x320")
    root.attributes('-topmost', True)
    root.iconbitmap(ICON_PATH)

    filename = os.path.basename(file_path)
    
    if is_exe:
        info = (f"You are opening the executable file '{filename}'.\n\n")
        if not dnspy_installed:
            info += "dnSpy is not installed at the required location: C:\\dnSpy\n\n"
        info += (
            "Note: Visual Studio does not support opening .exe files directly.\n"
            "Workaround:\n"
            "1. Rename the file extension from '.exe' to '.dll'\n"
            "2. Open the renamed file in Visual Studio\n"
            "3. Rename back to '.exe' after editing\n\n"
        )
        label = tk.Label(root, text=info, padx=20, pady=20, justify="left")
        label.pack(pady=10)
        
        if dnspy_installed:
            dnspy_button = tk.Button(
                root,
                text=f"Open '{filename}' with dnSpy",
                command=lambda: launch_and_exit(open_with_dnspy, file_path)
            )
            dnspy_button.pack(padx=10, pady=5)
        exit_button = tk.Button(root, text="Exit", command=root.quit)
        exit_button.pack(pady=10)

    else:
        info = f"You are opening the library file '{filename}'.\n\n"
        if not dnspy_installed:
            info += "dnSpy is not installed at the required location: C:\\dnSpy\n\n"
        label = tk.Label(root, text=info + "Available programs:", padx=20, pady=20, justify="left")
        label.pack(pady=10)

        if vs_installed:
            vs_button = tk.Button(
                root,
                text=f"Open '{filename}' with Visual Studio",
                command=lambda: launch_and_exit(open_with_vs, file_path)
            )
            vs_button.pack(padx=10, pady=5)

        if dnspy_installed:
            dnspy_button = tk.Button(
                root,
                text=f"Open '{filename}' with dnSpy",
                command=lambda: launch_and_exit(open_with_dnspy, file_path)
            )
            dnspy_button.pack(padx=10, pady=5)

        if not vs_installed and not dnspy_installed:
            label.config(text=(f"Cannot open '{filename}':\n- Visual Studio not installed\n- dnSpy not installed at C:\\dnSpy"))
            exit_button = tk.Button(root, text="Exit", command=root.quit)
            exit_button.pack(pady=10)
        elif not vs_installed:
            label.config(text=f"Visual Studio not installed.\nYou can only open '{filename}' with dnSpy (must be installed at C:\\dnSpy).")
            cancel_button = tk.Button(root, text="Cancel", command=root.quit)
            cancel_button.pack(pady=10)
        elif not dnspy_installed:
            label.config(text=f"dnSpy is not installed at C:\\dnSpy.\nYou can only open '{filename}' with Visual Studio.")
            cancel_button = tk.Button(root, text="Cancel", command=root.quit)
            cancel_button.pack(pady=10)
        else:
            cancel_button = tk.Button(root, text="Cancel", command=root.quit)
            cancel_button.pack(pady=10)

    root.mainloop()

def launch_and_exit(launch_func, file_path):
    launch_func(file_path)
    sys.exit()

def show_unsupported_file_type():
    root = tk.Tk()
    root.title("Unsupported File Type")
    root.geometry("400x200")
    root.attributes('-topmost', True)
    root.iconbitmap(ICON_PATH)
    label = tk.Label(root, text="This program only supports .dll and .exe files.", padx=20, pady=20)
    label.pack(pady=10)
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=5)
    root.mainloop()

def main():
    vs_installed, dnspy_installed = check_program_paths()
    if vs_installed or dnspy_installed:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            handle_file(file_path)
        else:
            select_file()
    else:
        show_error(
            "Required programs not installed:\n\n"
            "- Visual Studio (any edition)\n"
            "- dnSpy (must be installed at C:\\dnSpy)"
        )

if __name__ == "__main__":
    main()
