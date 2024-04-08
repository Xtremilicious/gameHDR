param (
    [Parameter(Mandatory = $true)]
    [string]$GameExecutable
)

# Check if the GameExecutable parameter is provided
if (-not $GameExecutable) {
    Write-Error "Please provide the path to the game executable using -GameExecutable parameter."
    exit 1
}

# Function to check if module is installed
function IsModuleInstalled($moduleName) {
    return (Get-Module -Name $moduleName -ListAvailable) -ne $null
}

# Function to install WindowsDisplayManager module with elevated privileges
function InstallWindowsDisplayManager {
    # Check if the module is already installed
    if (-not (IsModuleInstalled "WindowsDisplayManager")) {
        try {
            # Install the module using elevated privileges
            Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `"Install-Module WindowsDisplayManager -Force -Scope AllUsers`"" -Verb RunAs -Wait
            Write-Output "WindowsDisplayManager module installed successfully."
        } catch {
            Write-Error "Failed to install WindowsDisplayManager module: $_"
            exit 1
        }
    } else {
        Write-Output "WindowsDisplayManager module is already installed."
    }
}

# Install the module if not already installed
InstallWindowsDisplayManager

# Import WindowsDisplayManager module
Import-Module WindowsDisplayManager

# Function to enable HDR on the primary display
function EnableHDROnPrimaryDisplay {
    $primaryDisplay = WindowsDisplayManager\GetPrimaryDisplay
    if ($primaryDisplay) {
        $result = $primaryDisplay.EnableHdr()
        if ($result) {
            Write-Output "Enabled HDR on Primary Display"
            return $true
        } else {
            Write-Error "Failed to enable HDR on Primary Display"
            return $false
        }
    } else {
        Write-Error "Primary Display not found"
        return $false
    }
}

# Function to disable HDR on the primary display
function DisableHDROnPrimaryDisplay {
    $primaryDisplay = WindowsDisplayManager\GetPrimaryDisplay
    if ($primaryDisplay) {
        $result = $primaryDisplay.DisableHdr()
        if ($result) {
            Write-Output "Disabled HDR on Primary Display"
            return $true
        } else {
            Write-Error "Failed to disable HDR on Primary Display"
            return $false
        }
    } else {
        Write-Error "Primary Display not found"
        return $false
    }
}

# Function to start a game executable
function StartGame {
    param (
        [string]$GameExecutable
    )
    try {
        Write-Output "Starting the game: $GameExecutable"
        Start-Process -FilePath $GameExecutable -Wait
    } catch {
        Write-Error "Failed to start the game: $_"
    }
}

# Main script logic
try {
    # Enable HDR on the primary display
    if (EnableHDROnPrimaryDisplay) {
        # Start the game executable provided as an argument
        if ($GameExecutable -and (Test-Path $GameExecutable -PathType Leaf)) {
            StartGame -GameExecutable $GameExecutable
        } else {
            Write-Error "Invalid or missing game executable path: $GameExecutable"
        }

        # Disable HDR on the primary display after the game ends
        DisableHDROnPrimaryDisplay
    } else {
        Write-Error "Failed to enable HDR on the primary display"
    }
} catch {
    Write-Error "An error occurred: $_"
}
