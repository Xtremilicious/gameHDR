# Install required packages
python -m pip install -r requirements.txt

# Get pip show output for sv_ttk
$sv_ttk_info = & pip show sv_ttk

# Find and extract the Location line
$location_line = ($sv_ttk_info -split '\r?\n' | Where-Object { $_ -match '^Location:' }).Trim()

if ($location_line) {
    # Extract the location path
    $sv_ttk_location = $location_line -replace '^Location:\s+', ''
    
    # Append /sv_ttk to sv_ttk_location
    $sv_ttk_location += '\sv_ttk'
    
    # Print the sv_ttk location
    Write-Host "sv_ttk location: $sv_ttk_location"

    # Build the executable using PyInstaller
    pyinstaller --onedir --noconsole --add-data "hdr.ps1;." --add-data "$sv_ttk_location;sv_ttk" main.py
} else {
    Write-Host "Error: sv_ttk location not found."
}
