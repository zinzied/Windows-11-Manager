# Windows 11 Manager - PowerShell Admin Launcher
# This PowerShell script will automatically request administrator privileges and run the launcher

Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "  Windows 11 Manager - Admin Launcher" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""

# Check if colorama is installed for better color support
Write-Host "Checking for colorama (for better colors)..." -ForegroundColor Cyan
try {
    python -c "import colorama" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Colorama is already installed." -ForegroundColor Green
    } else {
        Write-Host "Installing colorama for better color support..." -ForegroundColor Yellow
        pip install colorama 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Colorama installed successfully." -ForegroundColor Green
        } else {
            Write-Host "Note: Could not install colorama. Colors may not display properly." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "Note: Could not check/install colorama. Colors may not display properly." -ForegroundColor Yellow
}

Write-Host ""

# Check if colorama is installed for better color support
Write-Host "Checking for colorama (for better colors)..." -ForegroundColor Cyan
try {
    python -c "import colorama" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Colorama is already installed." -ForegroundColor Green
    } else {
        Write-Host "Installing colorama for better color support..." -ForegroundColor Yellow
        pip install colorama 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Colorama installed successfully." -ForegroundColor Green
        } else {
            Write-Host "Note: Could not install colorama. Colors may not display properly." -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "Note: Could not check/install colorama. Colors may not display properly." -ForegroundColor Yellow
}

Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if ($isAdmin) {
    Write-Host "Already running as administrator." -ForegroundColor Green
    Write-Host "Starting Windows 11 Manager..." -ForegroundColor Cyan
    Write-Host ""
    
    # Run the launcher
    python launcher.py
} else {
    Write-Host "Requesting administrator privileges..." -ForegroundColor Yellow
    Write-Host "Please click 'Yes' in the UAC dialog." -ForegroundColor Yellow
    Write-Host ""
    
    # Request admin privileges and restart
    try {
        Start-Process python -ArgumentList "launcher.py" -Verb RunAs
        Write-Host "Admin request sent. The application will start with elevated privileges." -ForegroundColor Green
    } catch {
        Write-Host "Failed to request admin privileges: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "You can try running this script as administrator manually." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
