

# GameHDR

GameHDR is a user-friendly tool that allows you to create custom shortcuts for your favorite games with HDR (High Dynamic Range) enabled. 

This allows you to enable HDR on your monitor only while playing specific games.

**Note:** GameHDR is designed for Windows operating systems only. Tested for Windows 11 version 23H2.

## Features

- **Easy Shortcut Creation**: GameHDR simplifies the process of creating desktop shortcuts for games or any executables.
- **HDR Autostart**: Automatically enables HDR on your monitor when launching the game. HDR is disabled on your monitor once the game process ends.
- **Custom Icons**: Choose custom icons for your game shortcuts to personalize your desktop.

## How To Use
Use the GUI executable [here](https://github.com/Xtremilicious/GameHDR/releases/tag/release) to generate HDR shortcuts for any game or executable.

**OR**

Use CLI to use the `hdr.ps1` file directly.



## How It Works

GameHDR uses a PowerShell script (`hdr.ps1`) to enable HDR on your monitor when you start the game. HDR on the monitor is disabled once the game process has ended. Simply select your game executable file, and GameHDR will create a desktop shortcut that launches the game with HDR enabled.

## Why HDR?

HDR (High Dynamic Range) technology in gaming enhances the overall visual quality of games by providing a wider range of colors and greater contrast between light and dark areas. It creates more realistic and immersive gaming experiences, bringing games to life like never before.

## Technical Details

**Note:** GameHDR is designed for Windows operating systems and requires Python to be installed on your computer.

---

*For developers:* GameHDR uses Python scripts to automate tasks and provide a seamless experience for gamers interested in enhancing their gaming visuals with HDR technology.

## How It Works (Technical Details)

GameHDR leverages a combination of Python and PowerShell scripts to automate the process of creating custom game shortcuts with HDR (High Dynamic Range) enabled. Here's a breakdown of the technical workflow:

### Python Script (GUI and Shortcut Creation)

The graphical user interface (GUI) for GameHDR is built using the `tkinter` library in Python. This GUI allows users to interactively select a game executable and create a custom shortcut with HDR activation.

- **Game Selection**: Users can browse and select the game executable using the GUI.
- **Shortcut Creation**: Upon selecting the game executable, GameHDR creates a desktop shortcut that automatically enables HDR when launching the game.

### PowerShell Script (HDR Management)

The core functionality of enabling and disabling HDR is handled by a PowerShell script (`hdr.ps1`), which is invoked by the shortcut created using GameHDR.

- **Game Launch with HDR**: When the game shortcut is executed, the PowerShell script checks for the provided game executable and then uses the `WindowsDisplayManager` PowerShell module to enable HDR on the primary display.
  
  ```powershell
  EnableHDROnPrimaryDisplay
  StartGame -GameExecutable <path_to_game_executable>
  DisableHDROnPrimaryDisplay

### WindowsDisplayManager Module

The **WindowsDisplayManager** module is responsible for interacting with the Windows display settings to enable and disable HDR.

## Requirements

- **Python**: GameHDR requires Python to be installed on the system.
- **Windows**: GameHDR is designed specifically for Windows operating systems due to its reliance on PowerShell and WindowsDisplayManager.


