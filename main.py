import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import win32com.client as win32
import darkdetect
import sv_ttk
import ntkutils
import shutil
from PIL import Image, ImageTk

# Function to create shortcut with icon
def create_shortcut(ps1_file, game_executable, shortcut_name, icon_file=None):
    # Path to save the shortcut on the desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    shortcut_path = os.path.join(desktop_path, f'{shortcut_name}.lnk')

    # Create a shortcut to the PowerShell script
    shell = win32.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = 'powershell.exe'
    shortcut.Arguments = f'-ExecutionPolicy Bypass -File "{ps1_file}" -GameExecutable "{game_executable}"'
    shortcut.WorkingDirectory = os.path.dirname(ps1_file)
    
    # Set shortcut icon if provided
    if icon_file:
        shortcut.IconLocation = icon_file
    
    shortcut.save()

# Function to select game executable and extract icon
def select_game_file():
    file_path = filedialog.askopenfilename(title="Select Game Executable", filetypes=[("Executable files", "*.exe")])
    if file_path:
        game_entry.delete(0, tk.END)
        game_entry.insert(0, file_path)
        
        # Extract icon from the selected executable and update icon preview
        extract_icon(file_path)

# Function to extract icon and display in preview pane
def extract_icon(executable_path):
    # Create temporary directory to store extracted icon
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Path to store the extracted icon
    icon_path = os.path.join(temp_dir, 'extracted_icon.ico')
    
    # Run icoextract to extract the icon from the executable
    subprocess.run(['icoextract', executable_path, icon_path], check=True)
    
    # Load extracted icon using PIL
    icon_image = Image.open(icon_path)
    icon_image = icon_image.resize((100, 100), Image.LANCZOS)  # Resize icon for preview
    icon_photo = ImageTk.PhotoImage(icon_image)
    
    # Update icon preview pane
    icon_preview.config(image=icon_photo)
    icon_preview.image = icon_photo  # Keep reference to avoid garbage collection

    # Store the path of the extracted icon for creating the shortcut
    global extracted_icon_path
    extracted_icon_path = icon_path

# Function to select ICO file and update icon preview
def select_ico_file():
    ico_file = filedialog.askopenfilename(title="Select ICO File", filetypes=[("ICO files", "*.ico")])
    if ico_file:
        # Load the selected ICO file and update the icon preview
        icon_image = Image.open(ico_file)
        icon_image = icon_image.resize((100, 100), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        
        icon_preview.config(image=icon_photo)
        icon_preview.image = icon_photo  # Keep reference to avoid garbage collection
        
        # Update the extracted_icon_path to use the selected ICO file
        global extracted_icon_path
        extracted_icon_path = ico_file

# Function to create shortcut with icon and display success message
def create_shortcut_button_clicked():
    # Get the directory of the current Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the PowerShell script in the same directory as the Python script
    ps1_file = os.path.join(script_dir, 'hdr.ps1')
    
    game_executable = game_entry.get()
    shortcut_name = shortcut_name_entry.get() or os.path.splitext(os.path.basename(game_executable))[0]  # Default to exe filename
    
    if not os.path.exists(ps1_file):
        messagebox.showerror("Error", "PS1 file not found!")
        return
    
    if not os.path.exists(game_executable):
        messagebox.showerror("Error", "Selected game executable not found!")
        return
    
    create_shortcut(ps1_file, game_executable, shortcut_name, extracted_icon_path if 'extracted_icon_path' in globals() else None)
    messagebox.showinfo("Success", f"Shortcut '{shortcut_name}.lnk' created successfully!")
    cleanup_temp_directory()

def cleanup_temp_directory():
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"Temporary directory '{temp_dir}' successfully cleaned up.")
    else:
        print(f"Temporary directory '{temp_dir}' does not exist, nothing to clean up.")

# Create main window
window = tk.Tk()
window.title("GameHDR")

# Set window dimensions and position (optional)
window.geometry("650x420+200+200")

# Apply dark or light theme based on system theme
if darkdetect.theme() == "Dark":
    ntkutils.dark_title_bar(window)
    sv_ttk.set_theme("dark")
else:
    sv_ttk.set_theme("light")

# Create a frame for the layout
frame = ttk.Frame(window)
frame.pack(padx=20, pady=20, fill='both', expand=True)

# Create shortcut name entry and button (First column)
shortcut_name_label = ttk.Label(frame, text="Shortcut Name:")
shortcut_name_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')

shortcut_name_entry = ttk.Entry(frame, width=50)
shortcut_name_entry.grid(row=4, column=0, padx=10, pady=5)

create_button = ttk.Button(frame, text="Create Shortcut", command=create_shortcut_button_clicked)
create_button.grid(row=5, column=0, padx=10, pady=20)

# Choose Exe File section (Browse button)
game_label = ttk.Label(frame, text="Select Game Executable:")
game_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

game_entry = ttk.Entry(frame, width=50)
game_entry.grid(row=1, column=0, padx=10, pady=5)

browse_button = ttk.Button(frame, text="Browse...", command=select_game_file)
browse_button.grid(row=2, column=0, padx=10, pady=20)

# Icon Preview section (Second column)
preview_frame = ttk.Frame(frame)
preview_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky='n')

icon_label = ttk.Label(preview_frame, text="Icon Preview:")
icon_label.pack(pady=5)

# Placeholder icon preview
placeholder_image = Image.new('RGBA', (100, 100), (255, 255, 255, 0))  # Transparent placeholder image
placeholder_photo = ImageTk.PhotoImage(placeholder_image)

icon_preview = ttk.Label(preview_frame, image=placeholder_photo, padding=10, relief="sunken", cursor="crosshair")
icon_preview.pack(pady=5)

# Assign command to the label
icon_preview.bind("<Button-1>", lambda event: select_ico_file())

# Handle window closing event
def on_closing():
    cleanup_temp_directory()  # Clean up temporary directory
    window.destroy()  # Destroy the tkinter window

window.protocol("WM_DELETE_WINDOW", on_closing)  # Bind closing event to on_closing function

# Start the GUI main loop
window.mainloop()
