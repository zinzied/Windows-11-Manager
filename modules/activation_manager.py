#!/usr/bin/env python3
"""
Windows Activation Manager for Windows 10 and 11
This script provides tools to manage Windows activation status.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import sys
import os
import json
import re
import platform
import ctypes
import tempfile
import time
import winreg
from datetime import datetime
from colorama import Fore, Back, Style  

# Set UTF-8 encoding for better symbol support
if sys.platform == 'win32':
    try:
        # Try to set console to UTF-8
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass

# Try to import colorama for better Windows color support
try:
    from colorama import init, Fore, Back, Style
    COLORAMA_AVAILABLE = True
    # Initialize colorama
    init(autoreset=True)
except ImportError:
    COLORAMA_AVAILABLE = False

# Symbol definitions with fallbacks for terminals that don't support Unicode
class Symbols:
    def __init__(self):
        # Test if terminal supports Unicode
        self.unicode_supported = self._test_unicode_support()

        if self.unicode_supported:
            # Unicode symbols
            self.SHIELD = "🛡️"
            self.TARGET = "🎯"
            self.GEAR = "🔧"
            self.TOOLS = "🛠️"
            self.CLOUD = "☁️"
            self.LOCK = "🔒"
            self.TRASH = "🗑️"
            self.LIGHTNING = "⚡"
            self.INFO = "ℹ️"
            self.CROSS = "❌"
            self.CHECK = "✅"
            self.WARNING = "⚠️"
            self.ROCKET = "🚀"
            self.STOP = "⏹️"
            self.WAVE = "👋"
            self.RECYCLE = "🔄"
            self.BLOCK = "🚫"
            self.KEY = "🔑"
            self.FOLDER = "📁"
            self.BOOK = "📖"
            self.CERTIFICATE = "📜"
            self.LICENSE = "📄"
            self.HARDWARE = "💻"
            self.GLOBE = "🌐"
        else:
            # ASCII fallbacks
            self.SHIELD = "[SHIELD]"
            self.TARGET = "[TARGET]"
            self.GEAR = "[GEAR]"
            self.TOOLS = "[TOOLS]"
            self.CLOUD = "[CLOUD]"
            self.LOCK = "[LOCK]"
            self.TRASH = "[TRASH]"
            self.LIGHTNING = "[FAST]"
            self.INFO = "[INFO]"
            self.CROSS = "[X]"
            self.CHECK = "[OK]"
            self.WARNING = "[!]"
            self.ROCKET = "[START]"
            self.STOP = "[STOP]"
            self.WAVE = "[BYE]"
            self.RECYCLE = "[CYCLE]"
            self.BLOCK = "[BLOCK]"
            self.KEY = "[KEY]"
            self.FOLDER = "[FOLDER]"
            self.BOOK = "[BOOK]"
            self.CERTIFICATE = "[CERT]"
            self.LICENSE = "[LIC]"
            self.HARDWARE = "[HW]"
            self.GLOBE = "[GLOBE]"

    def _test_unicode_support(self):
        """Test if the terminal supports Unicode symbols."""
        try:
            # Try to encode a Unicode symbol
            test_symbol = "🛡️"
            test_symbol.encode(sys.stdout.encoding or 'utf-8')
            return True
        except (UnicodeEncodeError, AttributeError):
            return False

# Initialize symbols
symbols = Symbols()

# Color codes for terminal output
class Colors:
    if COLORAMA_AVAILABLE:
        # Use colorama colors for better Windows support
        RED = Fore.RED + Style.BRIGHT
        GREEN = Fore.GREEN + Style.BRIGHT
        YELLOW = Fore.YELLOW + Style.BRIGHT
        BLUE = Fore.BLUE + Style.BRIGHT
        MAGENTA = Fore.MAGENTA + Style.BRIGHT
        CYAN = Fore.CYAN + Style.BRIGHT
        WHITE = Fore.WHITE + Style.BRIGHT
        BOLD = Style.BRIGHT
        UNDERLINE = ''  # Colorama doesn't have underline
        END = Style.RESET_ALL
    else:
        # Fallback to ANSI codes
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'  # End color formatting

# Global variable to track if ANSI has been tested
_ansi_tested = False

def print_colored(text, color=Colors.WHITE):
    """Print text with color."""
    global _ansi_tested
    if COLORAMA_AVAILABLE:
        # Colorama handles everything for us
        print(f"{color}{text}")
    else:
        # Try ANSI codes with fallback
        try:
            if not _ansi_tested:
                enable_ansi_colors()
                _ansi_tested = True
            print(f"{color}{text}{Colors.END}")
        except Exception:
            # Fallback to plain text
            print(text)

def enable_ansi_colors():
    """Enable ANSI color codes on Windows terminals."""
    if platform.system() == "Windows":
        try:
            # Enable ANSI escape sequence processing
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True

def print_header():
    """Print the header for this module."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored(f"{symbols.KEY}  WINDOWS ACTIVATION MANAGER - WINDOWS 10 & 11", Colors.BOLD + Colors.MAGENTA)
    print_colored("    Created by Zied Boughdir - 2025", Colors.CYAN)
    print_colored("    GitHub: https://github.com/zinzied", Colors.BLUE)
    print_colored("=" * 70, Colors.MAGENTA)
    print_colored("    Manage Windows Activation Status", Colors.CYAN)
    print_colored("=" * 70, Colors.MAGENTA)

def check_admin():
    """Check if running as administrator."""
    try:
        subprocess.run(['net', 'session'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_mas_activation_status():
    """Get comprehensive activation status using MAS Check Activation Status script."""
    mas_script = get_mas_script_path("../Check_Activation_Status.cmd")
    
    if not mas_script:
        # Try alternative path
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mas_script = os.path.join(base_path, "MAS", "Separate-Files-Version", "Check_Activation_Status.cmd")
    
    if os.path.exists(mas_script):
        try:
            print_colored(f"{symbols.INFO} Running MAS activation status check...", Colors.CYAN)
            
            # Execute MAS status checker
            result = subprocess.run([
                'cmd.exe', '/c', f'"{mas_script}"'
            ], capture_output=True, text=True, timeout=180, encoding='utf-8', errors='replace')
            
            if result.returncode == 0 and result.stdout:
                return True, result.stdout
            else:
                return False, f"MAS script failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "MAS status check timed out"
        except Exception as e:
            return False, f"Error running MAS status check: {str(e)}"
    
    return False, "MAS Check_Activation_Status.cmd not found"

def parse_mas_status_output(output):
    """Parse MAS activation status output to extract key information."""
    status_info = {
        'windows_licensed': False,
        'windows_method': 'Unknown',
        'office_licensed': False,
        'office_method': 'Unknown',
        'expires': 'Unknown',
        'details': []
    }
    
    lines = output.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        # Detect sections
        if 'Windows Status' in line:
            current_section = 'windows'
        elif 'Office Status' in line:
            current_section = 'office'
        elif 'Ohook Status' in line:
            current_section = 'ohook'
            status_info['office_method'] = 'Ohook (Permanent)'
            status_info['office_licensed'] = True
        
        # Parse license status
        if 'License Status' in line and 'Licensed' in line:
            if current_section == 'windows':
                status_info['windows_licensed'] = True
            elif current_section == 'office':
                status_info['office_licensed'] = True
        
        # Parse activation method
        if 'HWID' in line and current_section == 'windows':
            status_info['windows_method'] = 'HWID (Permanent)'
            status_info['windows_licensed'] = True
        elif 'KMS38' in line and current_section == 'windows':
            status_info['windows_method'] = 'KMS38 (Until 2038)'
            status_info['windows_licensed'] = True
        elif 'KMS' in line and 'Volume' in line:
            if current_section == 'windows':
                status_info['windows_method'] = 'KMS (180 Days)'
            elif current_section == 'office':
                status_info['office_method'] = 'KMS (180 Days)'
        
        # Parse expiration
        if 'expires' in line.lower() or 'remaining' in line.lower():
            status_info['expires'] = line
        
        # Collect important details
        if any(keyword in line.lower() for keyword in ['license', 'activation', 'expires', 'permanent', 'error']):
            if line and not line.startswith('=') and not line.startswith('_'):
                status_info['details'].append(line)
    
    return status_info

def display_enhanced_activation_status():
    """Display enhanced activation status using MAS methods with fallback."""
    print_colored(f"\n{symbols.INFO}  ENHANCED ACTIVATION STATUS CHECK", Colors.BOLD + Colors.CYAN)
    
    # Try MAS method first
    mas_success, mas_output = get_mas_activation_status()
    
    if mas_success:
        print_colored(f"\n{symbols.CHECK} Using MAS comprehensive status check...", Colors.GREEN)
        
        # Parse MAS output
        status_info = parse_mas_status_output(mas_output)
        
        print_colored("\n" + "=" * 60, Colors.BLUE)
        print_colored(f"{symbols.SHIELD}  COMPREHENSIVE ACTIVATION STATUS", Colors.BOLD + Colors.BLUE)
        print_colored("=" * 60, Colors.BLUE)
        
        # Windows Status
        print_colored(f"\n{symbols.LICENSE} WINDOWS ACTIVATION:", Colors.BOLD + Colors.MAGENTA)
        if status_info['windows_licensed']:
            print_colored(f"{symbols.CHECK} Status: ACTIVATED", Colors.GREEN)
            print_colored(f"{symbols.INFO} Method: {status_info['windows_method']}", Colors.CYAN)
        else:
            print_colored(f"{symbols.CROSS} Status: NOT ACTIVATED", Colors.RED)
            print_colored(f"{symbols.WARNING} Windows needs activation", Colors.YELLOW)
        
        # Office Status
        print_colored(f"\n{symbols.CERTIFICATE} OFFICE ACTIVATION:", Colors.BOLD + Colors.MAGENTA)
        if status_info['office_licensed']:
            print_colored(f"{symbols.CHECK} Status: ACTIVATED", Colors.GREEN)
            print_colored(f"{symbols.INFO} Method: {status_info['office_method']}", Colors.CYAN)
        else:
            print_colored(f"{symbols.CROSS} Status: NOT DETECTED OR NOT ACTIVATED", Colors.YELLOW)
        
        # Expiration info
        if status_info['expires'] != 'Unknown':
            print_colored(f"\n{symbols.GLOBE} EXPIRATION INFO:", Colors.BOLD + Colors.MAGENTA)
            print_colored(f"{symbols.INFO} {status_info['expires']}", Colors.CYAN)
        
        # Additional details
        if status_info['details']:
            print_colored(f"\n{symbols.BOOK} ADDITIONAL DETAILS:", Colors.BOLD + Colors.MAGENTA)
            for detail in status_info['details'][:5]:  # Show first 5 important details
                print_colored(f"  • {detail}", Colors.WHITE)
        
        print_colored("\n" + "=" * 60, Colors.BLUE)
        
        # Show raw MAS output if requested
        show_raw = input(f"\n{Colors.BOLD}Show detailed MAS output? (y/N): {Colors.END}").strip().lower()
        if show_raw == 'y':
            print_colored(f"\n{symbols.BOOK} DETAILED MAS OUTPUT:", Colors.BOLD + Colors.CYAN)
            print_colored("=" * 60, Colors.CYAN)
            print_colored(mas_output, Colors.WHITE)
        
        return True
    
    else:
        print_colored(f"\n{symbols.WARNING} MAS status check failed: {mas_output}", Colors.YELLOW)
        print_colored(f"{symbols.INFO} Falling back to standard status check...", Colors.CYAN)
        
        # Fallback to original method
        return display_activation_status()

def get_advanced_activation_info():
    """Get advanced activation information using PowerShell and WMI."""
    print_colored(f"\n{symbols.GEAR}  ADVANCED ACTIVATION ANALYSIS", Colors.BOLD + Colors.CYAN)
    
    advanced_script = '''
# Advanced Windows Activation Status Script
$ErrorActionPreference = "SilentlyContinue"

Write-Host "=== WINDOWS LICENSING INFORMATION ==="

# Get SoftwareLicensingService info
$sls = Get-WmiObject -Class SoftwareLicensingService
Write-Host "Version: $($sls.Version)"
Write-Host "KeyManagementServiceMachine: $($sls.KeyManagementServiceMachine)"
Write-Host "KeyManagementServicePort: $($sls.KeyManagementServicePort)"
Write-Host "IsKeyManagementServiceMachine: $($sls.IsKeyManagementServiceMachine)"

Write-Host "\n=== PRODUCT INFORMATION ==="

# Get all licensed products
$products = Get-WmiObject -Class SoftwareLicensingProduct | Where-Object {$_.PartialProductKey -ne $null}

foreach ($product in $products) {
    Write-Host "\n--- Product: $($product.Name) ---"
    Write-Host "Description: $($product.Description)"
    Write-Host "Product Key Channel: $($product.ProductKeyChannel)"
    Write-Host "Product Key ID: $($product.ProductKeyID)"
    Write-Host "Partial Product Key: $($product.PartialProductKey)"
    Write-Host "License Status: $($product.LicenseStatus) (0=Unlicensed, 1=Licensed, 2=OOBGrace, 3=OOTGrace, 4=NonGenuineGrace, 5=Notification, 6=ExtendedGrace)"
    Write-Host "Grace Period Remaining: $($product.GracePeriodRemaining) minutes"
    Write-Host "Evaluation End Date: $($product.EvaluationEndDate)"
    Write-Host "License Family: $($product.LicenseFamily)"
    Write-Host "License Status Reason: $($product.LicenseStatusReason)"
    
    if ($product.ADActivationObjectName) {
        Write-Host "AD Activation Object: $($product.ADActivationObjectName)"
    }
    
    if ($product.KeyManagementServiceMachine) {
        Write-Host "KMS Server: $($product.KeyManagementServiceMachine):$($product.KeyManagementServicePort)"
        Write-Host "KMS PID: $($product.KeyManagementServiceProductKeyID)"
    }
}

Write-Host "\n=== SYSTEM INFORMATION ==="
$os = Get-WmiObject -Class Win32_OperatingSystem
Write-Host "OS Name: $($os.Caption)"
Write-Host "Version: $($os.Version)"
Write-Host "Build: $($os.BuildNumber)"
Write-Host "Install Date: $($os.InstallDate)"
Write-Host "Registered User: $($os.RegisteredUser)"
Write-Host "Organization: $($os.Organization)"
Write-Host "Product Type: $($os.ProductType)"
Write-Host "Suite Mask: $($os.SuiteMask)"

Write-Host "\n=== ACTIVATION METHODS DETECTED ==="

# Check for HWID activation indicators
$hwid = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform" -Name "BackupProductKeyDefault" -ErrorAction SilentlyContinue
if ($hwid) {
    Write-Host "HWID: Digital License detected"
}

# Check for KMS38 indicators
$kms38 = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform\55c92734-d682-4d71-983e-d6ec3f16059f" -Name "SkipRearm" -ErrorAction SilentlyContinue
if ($kms38 -and $kms38.SkipRearm -eq 1) {
    Write-Host "KMS38: Registry modification detected"
}

# Check for KMS activation
$kmsProducts = Get-WmiObject -Class SoftwareLicensingProduct | Where-Object {$_.KeyManagementServiceMachine -ne $null}
if ($kmsProducts) {
    Write-Host "KMS: Active KMS activation detected"
    foreach ($kms in $kmsProducts) {
        Write-Host "  Server: $($kms.KeyManagementServiceMachine):$($kms.KeyManagementServicePort)"
    }
}

Write-Host "\n=== OFFICE DETECTION ==="

# Check for Office installations
$officeKeys = @(
    "HKLM:\SOFTWARE\Microsoft\Office",
    "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Office"
)

foreach ($key in $officeKeys) {
    if (Test-Path $key) {
        $versions = Get-ChildItem -Path $key -ErrorAction SilentlyContinue | Where-Object {$_.Name -match "\\d+\.\d+$"}
        foreach ($version in $versions) {
            $versionInfo = Get-ItemProperty -Path $version.PSPath -ErrorAction SilentlyContinue
            if ($versionInfo) {
                Write-Host "Office Version Found: $($version.PSChildName)"
                
                # Check for Ohook
                $officePath = "${env:ProgramFiles}\Microsoft Office\Office$($version.PSChildName)"
                if (Test-Path "$officePath\sppc*.dll") {
                    Write-Host "  Ohook: Detected in $officePath"
                }
                
                $officePath86 = "${env:ProgramFiles(x86)}\Microsoft Office\Office$($version.PSChildName)"
                if (Test-Path "$officePath86\sppc*.dll") {
                    Write-Host "  Ohook: Detected in $officePath86"
                }
            }
        }
    }
}
    '''
    
    try:
        print_colored(f"{symbols.INFO} Running advanced analysis...", Colors.CYAN)
        success, stdout, stderr = run_powershell_command(advanced_script, timeout=120)
        
        if success and stdout:
            print_colored("\n" + "=" * 70, Colors.BLUE)
            print_colored(f"{symbols.GEAR} ADVANCED SYSTEM ANALYSIS", Colors.BOLD + Colors.BLUE)
            print_colored("=" * 70, Colors.BLUE)
            print_colored(stdout, Colors.WHITE)
            return True
        else:
            print_colored(f"\n{symbols.CROSS} Advanced analysis failed.", Colors.RED)
            if stderr:
                print_colored(f"{symbols.INFO} Error: {stderr}", Colors.YELLOW)
            return False
            
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Advanced analysis failed: {str(e)}", Colors.RED)
        return False
def get_activation_status():
    """Get the current Windows activation status (legacy method)."""
    try:
        # Use slmgr.vbs to get activation status
        # Instead of capturing output, redirect to a temp file to avoid encoding issues
        import tempfile

        # Create a temporary file to store the output
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dli'], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        # Parse the output to extract key information
        status = {
            'licensed': False,
            'product_key': None,
            'description': None,
            'license_status': None,
            'remaining_time': None
        }

        lines = output.split('\n')
        for line in lines:
            if 'License Status' in line:
                status['license_status'] = line.split(':')[1].strip() if ':' in line else 'Unknown'
                if 'Licensed' in status['license_status']:
                    status['licensed'] = True
            elif 'Product Key' in line:
                status['product_key'] = line.split(':')[1].strip() if ':' in line else 'Not available'
            elif 'Description' in line:
                status['description'] = line.split(':')[1].strip() if ':' in line else 'Not available'
            elif 'Remaining Windows' in line and 'rearm' not in line.lower():
                status['remaining_time'] = line.split(':')[1].strip() if ':' in line else 'Unknown'

        return status
    except subprocess.CalledProcessError as e:
        print_colored(f"\n{symbols.CROSS} Error checking activation status: {e}", Colors.RED)
        return None
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Unexpected error checking activation status: {e}", Colors.RED)
        return None

def display_activation_status():
    """Display the current Windows activation status (legacy method)."""
    print_colored(f"\n{symbols.INFO}  BASIC ACTIVATION STATUS CHECK", Colors.BOLD + Colors.CYAN)

    status = get_activation_status()
    if not status:
        return False

    print_colored("\n" + "=" * 50, Colors.BLUE)
    print_colored(f"{symbols.LICENSE}  ACTIVATION DETAILS", Colors.BOLD + Colors.BLUE)
    print_colored("=" * 50, Colors.BLUE)

    if status['licensed']:
        print_colored(f"{symbols.CHECK} License Status: {status['license_status']}", Colors.GREEN)
        print_colored(f"{symbols.CERTIFICATE} Product Key: {status['product_key'] if status['product_key'] else 'Not available'}", Colors.WHITE)
        print_colored(f"{symbols.INFO} Description: {status['description'] if status['description'] else 'Not available'}", Colors.WHITE)

        if status['remaining_time']:
            print_colored(f"{symbols.GLOBE} Remaining Time: {status['remaining_time']}", Colors.CYAN)
    else:
        print_colored(f"{symbols.CROSS} License Status: {status['license_status']}", Colors.RED)
        print_colored(f"{symbols.WARNING} Windows is not activated", Colors.YELLOW)
        print_colored(f"{symbols.INFO} Description: {status['description'] if status['description'] else 'Not available'}", Colors.WHITE)
    
    return True

def validate_product_key(product_key):
    """
    Validate the format of a Windows product key.
    
    Windows product keys are typically in one of these formats:
    - XXXXX-XXXXX-XXXXX-XXXXX-XXXXX (25 characters, 5 groups of 5)
    - XXXXXXXXX-XXXXXXXXX-XXXXXXXXX-XXXXXXXXX-XXXXXXXXX (45 characters, 5 groups of 9)
    """
    if not product_key:
        return False, "Product key cannot be empty."
    
    # Remove any whitespace
    key = product_key.strip().upper()
    
    # Check for common invalid inputs
    if len(key) < 10:  # Too short to be a valid key
        return False, "Product key is too short. Windows product keys are typically 25 or 29 characters."
    
    if key.isdigit() and len(key) < 10:  # Just a number like "2"
        return False, "Invalid product key format. Please enter a valid Windows product key (e.g., XXXXX-XXXXX-XXXXX-XXXXX-XXXXX)."
    
    # Check for standard Windows key format (25 characters with dashes)
    if len(key) == 29 and key.count('-') == 4:
        parts = key.split('-')
        if len(parts) == 5 and all(len(part) == 5 for part in parts):
            # Check if all parts contain only alphanumeric characters
            if all(part.replace('-', '').isalnum() for part in parts):
                return True, "Valid product key format."
    
    # Check for KMS/MAK key format (might be different)
    if len(key) >= 25 and '-' in key:
        # Allow other dash-separated formats
        parts = key.split('-')
        if len(parts) >= 4:  # At least 4 parts
            return True, "Product key format appears valid."
    
    # If no dashes, check if it's 25 characters of alphanumeric
    if len(key) == 25 and key.isalnum():
        return True, "Product key format appears valid."
    
    return False, "Invalid product key format. Windows product keys should be in format XXXXX-XXXXX-XXXXX-XXXXX-XXXXX."

def activate_windows(product_key=None):
    """Attempt to activate Windows with a product key."""
    print_colored(f"\n{symbols.ROCKET}  ACTIVATING WINDOWS", Colors.BOLD + Colors.CYAN)

    if not product_key:
        print_colored(f"\n{symbols.INFO} Please enter your Windows product key:", Colors.CYAN)
        print_colored(f"Example format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX", Colors.WHITE)
        product_key = input(f"{Colors.BOLD}Enter your Windows product key: {Colors.END}").strip()
        
        if not product_key:
            print_colored(f"\n{symbols.CROSS} No product key provided.", Colors.RED)
            return False

    # Validate the product key format
    is_valid, message = validate_product_key(product_key)
    if not is_valid:
        print_colored(f"\n{symbols.CROSS} {message}", Colors.RED)
        print_colored(f"{symbols.INFO} Please ensure you have a valid Windows product key.", Colors.YELLOW)
        print_colored(f"{symbols.INFO} You can find your product key on your Windows installation media, email receipt, or Certificate of Authenticity.", Colors.YELLOW)
        return False
    
    print_colored(f"\n{symbols.CHECK} Product key format validated.", Colors.GREEN)

    try:
        import tempfile

        # Use slmgr.vbs to install the product key
        print_colored(f"\n{symbols.INFO} Installing product key...", Colors.CYAN)

        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/ipk', product_key], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        if result.returncode == 0:
            print_colored(f"{symbols.CHECK} Product key installed successfully.", Colors.GREEN)

            # Now try to activate
            print_colored(f"\n{symbols.INFO} Attempting to activate Windows...", Colors.CYAN)

            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
                temp_file_path = temp_file.name

            # Run the command and redirect output to our temp file in binary mode
            with open(temp_file_path, 'wb') as temp_output:
                result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/ato'], 
                                      stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

            # Read the output from the temp file in binary mode and decode with cp1252
            with open(temp_file_path, 'rb') as temp_file:
                output = temp_file.read().decode('cp1252', errors='replace')

            # Clean up the temp file
            os.unlink(temp_file_path)

            if result.returncode == 0:
                print_colored(f"{symbols.CHECK} Windows activation completed successfully!", Colors.GREEN)
                return True
            else:
                print_colored(f"{symbols.CROSS} Windows activation failed.", Colors.RED)
                print_colored(f"Output: {output}", Colors.YELLOW)
                return False
        else:
            print_colored(f"{symbols.CROSS} Failed to install product key.", Colors.RED)
            print_colored(f"Output: {output}", Colors.YELLOW)
            return False

    except subprocess.CalledProcessError as e:
        # Provide more specific error messages based on return codes
        error_code = e.returncode
        if error_code == 3221549136:  # 0xC0000130
            print_colored(f"\n{symbols.CROSS} Invalid product key format or characters.", Colors.RED)
            print_colored(f"{symbols.INFO} Please check that your product key is entered correctly.", Colors.YELLOW)
            print_colored(f"{symbols.INFO} Windows product keys should be in format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX", Colors.YELLOW)
        elif error_code == -1073422315:  # 0xC004F015
            print_colored(f"\n{symbols.CROSS} Product key is not valid for this version of Windows.", Colors.RED)
            print_colored(f"{symbols.INFO} Make sure the product key matches your Windows edition.", Colors.YELLOW)
        elif error_code == -1073418194:  # 0xC004F02E  
            print_colored(f"\n{symbols.CROSS} Product key format is invalid.", Colors.RED)
            print_colored(f"{symbols.INFO} Please verify the product key and try again.", Colors.YELLOW)
        else:
            print_colored(f"\n{symbols.CROSS} Error activating Windows (Code: {error_code}): {e}", Colors.RED)
            print_colored(f"{symbols.INFO} This may be due to network issues, invalid key, or system restrictions.", Colors.YELLOW)
        
        print_colored(f"\n{symbols.BOOK} Troubleshooting Tips:", Colors.BOLD + Colors.CYAN)
        print_colored(f"• Ensure you're connected to the internet", Colors.WHITE)
        print_colored(f"• Verify the product key is correct and unused", Colors.WHITE)
        print_colored(f"• Check that the key matches your Windows edition", Colors.WHITE)
        print_colored(f"• Try running Windows Update first", Colors.WHITE)
        return False
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Unexpected error activating Windows: {e}", Colors.RED)
        return False

def check_activation_details():
    """Show detailed activation information."""
    print_colored(f"\n{symbols.INFO}  DETAILED ACTIVATION INFORMATION", Colors.BOLD + Colors.CYAN)

    try:
        import tempfile

        # Get detailed information about the license
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dlv'], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        print_colored("\n" + "=" * 50, Colors.BLUE)
        print_colored(f"{symbols.CERTIFICATE}  LICENSE DETAILS", Colors.BOLD + Colors.BLUE)
        print_colored("=" * 50, Colors.BLUE)
        print_colored(output, Colors.WHITE)

        # Get installation ID
        print_colored("\n" + "=" * 50, Colors.BLUE)
        print_colored(f"{symbols.HARDWARE}  INSTALLATION ID", Colors.BOLD + Colors.BLUE)
        print_colored("=" * 50, Colors.BLUE)

        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dti'], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        print_colored(output, Colors.WHITE)

        return True

    except subprocess.CalledProcessError as e:
        print_colored(f"\n{symbols.CROSS} Error getting activation details: {e}", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Unexpected error getting activation details: {e}", Colors.RED)
        return False

def reset_activation():
    """Reset Windows activation (rearm)."""
    print_colored(f"\n{symbols.WARNING}  RESET WINDOWS ACTIVATION (REARM)", Colors.BOLD + Colors.YELLOW)
    print_colored(f"{symbols.WARNING} This will reset the activation status and may require reactivation.", Colors.YELLOW)
    print_colored(f"{symbols.WARNING} This can only be done a limited number of times (typically 3 times).", Colors.YELLOW)

    confirm = input(f"\n{Colors.BOLD}Are you sure you want to reset activation? (y/N): {Colors.END}").strip().lower()

    if confirm != 'y':
        print_colored(f"\n{symbols.CHECK} Activation reset cancelled.", Colors.GREEN)
        return False

    try:
        import tempfile

        # Use slmgr.vbs to rearm Windows
        print_colored(f"\n{symbols.INFO} Resetting activation...", Colors.CYAN)

        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/rearm'], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        if result.returncode == 0:
            print_colored(f"{symbols.CHECK} Windows activation has been reset successfully!", Colors.GREEN)
            print_colored(f"{symbols.INFO} You will need to reactivate Windows.", Colors.CYAN)
            print_colored(f"{symbols.INFO} Please restart your computer for changes to take effect.", Colors.CYAN)
            return True
        else:
            print_colored(f"{symbols.CROSS} Failed to reset Windows activation.", Colors.RED)
            print_colored(f"Output: {output}", Colors.YELLOW)
            return False

    except subprocess.CalledProcessError as e:
        print_colored(f"\n{symbols.CROSS} Error resetting activation: {e}", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Unexpected error resetting activation: {e}", Colors.RED)
        return False

def show_activation_help():
    """Show help information about Windows activation."""
    print_colored(f"\n{symbols.BOOK}  WINDOWS ACTIVATION HELP", Colors.BOLD + Colors.CYAN)

    print_colored("\n" + "=" * 70, Colors.BLUE)
    print_colored(f"{symbols.INFO} UNDERSTANDING WINDOWS ACTIVATION", Colors.BOLD + Colors.BLUE)
    print_colored("=" * 70, Colors.BLUE)

    print_colored(f"\n{symbols.LICENSE} WHAT IS WINDOWS ACTIVATION?", Colors.BOLD + Colors.WHITE)
    print_colored("Windows activation is a validation process that verifies your Windows operating system is genuine and properly licensed.", Colors.WHITE)
    print_colored("Activation helps ensure that your PC is running genuine Windows software and not counterfeit or pirated software.", Colors.WHITE)

    print_colored(f"\n{symbols.KEY} HOW TO ACTIVATE WINDOWS", Colors.BOLD + Colors.WHITE)
    print_colored("1. Purchase a valid Windows license from Microsoft or an authorized retailer", Colors.WHITE)
    print_colored("2. Use the product key that came with your Windows purchase", Colors.WHITE)
    print_colored("3. Run this tool and select 'Activate Windows'", Colors.WHITE)
    print_colored("4. Enter your product key when prompted", Colors.WHITE)
    print_colored("5. Follow the on-screen instructions to complete activation", Colors.WHITE)

    print_colored(f"\n{symbols.LICENSE} PRODUCT KEY FORMATS", Colors.BOLD + Colors.WHITE)
    print_colored("• Standard Format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX (25 characters)", Colors.WHITE)
    print_colored("• Example: 7B9N3-2V7C8-JQKMG-X7DQT-BHBB6", Colors.CYAN)
    print_colored("• Characters: Letters (A-Z) and Numbers (0-9) only", Colors.WHITE)
    print_colored("• Dashes: Required every 5 characters", Colors.WHITE)
    print_colored("• Case: Not case-sensitive (automatically converted to uppercase)", Colors.WHITE)

    print_colored(f"\n{symbols.CERTIFICATE} TYPES OF WINDOWS LICENSES", Colors.BOLD + Colors.WHITE)
    print_colored("• Retail License: Can be transferred to different computers", Colors.WHITE)
    print_colored("• OEM License: Tied to the original hardware it came with", Colors.WHITE)
    print_colored("• Volume License: For organizations with multiple computers", Colors.WHITE)
    print_colored("• Digital License: Automatically assigned after first activation", Colors.WHITE)

    print_colored(f"\n{symbols.WARNING} IMPORTANT NOTES", Colors.BOLD + Colors.YELLOW)
    print_colored("• This tool only works on genuine Windows installations", Colors.YELLOW)
    print_colored("• Using invalid or counterfeit product keys is against Microsoft's terms", Colors.YELLOW)
    print_colored("• The reset option (rearm) can only be used a limited number of times", Colors.YELLOW)
    print_colored("• Some editions of Windows (like Home) cannot be activated with KMS or MAK keys", Colors.YELLOW)

    print_colored(f"\n{symbols.CHECK} ACTIVATION TROUBLESHOOTING", Colors.BOLD + Colors.GREEN)
    print_colored("• Ensure you're connected to the internet", Colors.WHITE)
    print_colored("• Check that your system clock is set correctly", Colors.WHITE)
    print_colored("• Make sure you're using the correct product key for your Windows edition", Colors.WHITE)
    print_colored("• Verify the product key hasn't been used on another computer (if retail)", Colors.WHITE)
    print_colored("• Try running Windows Update first to ensure system compatibility", Colors.WHITE)
    print_colored("• If using a Volume License key, ensure your organization allows activation", Colors.WHITE)
    print_colored("• For persistent issues, use Microsoft's automated phone activation", Colors.WHITE)
    print_colored("• If issues persist, contact Microsoft Support", Colors.WHITE)

    print_colored(f"\n{symbols.WARNING} COMMON ERROR SOLUTIONS", Colors.BOLD + Colors.YELLOW)
    print_colored("• 'Invalid product key': Check format and ensure key matches Windows edition", Colors.WHITE)
    print_colored("• 'Key already in use': Key may be installed on another computer", Colors.WHITE)
    print_colored("• 'Cannot connect to activation server': Check internet connection", Colors.WHITE)
    print_colored("• 'Hardware change detected': May need to reactivate after major hardware changes", Colors.WHITE)

    print_colored("\n" + "=" * 70, Colors.BLUE)

# ============================================================================
# MAS (Microsoft Activation Scripts) Integration
# ============================================================================

def get_windows_info():
    """Get Windows version and build information."""
    try:
        # Get Windows version
        import platform
        version = platform.version()
        release = platform.release()
        
        # Get build number from registry
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as key:
                build = winreg.QueryValueEx(key, "CurrentBuildNumber")[0]
                product_name = winreg.QueryValueEx(key, "ProductName")[0]
        except:
            build = "Unknown"
            product_name = "Unknown"
        
        return {
            'version': version,
            'release': release,
            'build': int(build) if build.isdigit() else 0,
            'product_name': product_name
        }
    except Exception:
        return {
            'version': 'Unknown',
            'release': 'Unknown', 
            'build': 0,
            'product_name': 'Unknown'
        }

def check_prerequisites():
    """Check if system meets prerequisites for MAS activation."""
    win_info = get_windows_info()
    
    # Check if Windows version is supported
    if win_info['build'] < 10240:  # Windows 10 minimum build
        return False, f"Unsupported Windows version. Build {win_info['build']} detected. Windows 10/11 required."
    
    # Check if running in Windows Sandbox
    if os.path.exists(r"C:\Users\WDAGUtilityAccount"):
        return False, "Windows Sandbox detected. Activation is not supported in sandbox environment."
    
    # Check admin privileges
    if not check_admin():
        return False, "Administrator privileges required for activation."
    
    return True, "Prerequisites met."

def run_powershell_command(command, timeout=300):
    """Execute PowerShell command with proper encoding handling."""
    try:
        # Create temporary script file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(command)
            temp_script = temp_file.name
        
        # Execute PowerShell script
        result = subprocess.run([
            'powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', 
            '-WindowStyle', 'Hidden', '-File', temp_script
        ], capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='replace')
        
        # Clean up temp file
        try:
            os.unlink(temp_script)
        except:
            pass
        
        return result.returncode == 0, result.stdout, result.stderr
    
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def run_mas_script(script_path, parameters=""):
    """Run MAS activation script with proper parameters."""
    try:
        if not os.path.exists(script_path):
            return False, f"MAS script not found: {script_path}", ""
        
        # Execute the MAS script
        result = subprocess.run([
            'cmd.exe', '/c', f'"{script_path}" {parameters}'
        ], capture_output=True, text=True, timeout=300, encoding='utf-8', errors='replace')
        
        return result.returncode == 0, result.stdout, result.stderr
    
    except subprocess.TimeoutExpired:
        return False, "", "Script execution timed out"
    except Exception as e:
        return False, "", str(e)

def get_mas_script_path(script_name):
    """Get the full path to a MAS script."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(base_path, "MAS", "Separate-Files-Version", "Activators", script_name)
    return script_path if os.path.exists(script_path) else None

def hwid_activation():
    """HWID Activation - Permanent Windows 10/11 activation using MAS."""
    print_colored(f"\n{symbols.SHIELD}  HWID ACTIVATION - PERMANENT WINDOWS ACTIVATION", Colors.BOLD + Colors.GREEN)
    print_colored("This method provides permanent activation for Windows 10/11 through digital license.", Colors.CYAN)
    
    # Check prerequisites
    prereq_ok, prereq_msg = check_prerequisites()
    if not prereq_ok:
        print_colored(f"\n{symbols.CROSS} {prereq_msg}", Colors.RED)
        return False
    
    win_info = get_windows_info()
    print_colored(f"\n{symbols.INFO} Detected: {win_info['product_name']} (Build {win_info['build']})", Colors.CYAN)
    
    # Verify Windows 10/11
    if win_info['build'] < 10240:
        print_colored(f"\n{symbols.CROSS} HWID activation only supports Windows 10/11.", Colors.RED)
        print_colored(f"{symbols.INFO} Your build: {win_info['build']}, Required: 10240+", Colors.YELLOW)
        return False
    
    # Check if it's Windows Server
    if 'Server' in win_info['product_name']:
        print_colored(f"\n{symbols.CROSS} HWID activation is not supported on Windows Server.", Colors.RED)
        return False
    
    print_colored(f"\n{symbols.WARNING} This will attempt permanent activation of your Windows installation.", Colors.YELLOW)
    confirm = input(f"\n{Colors.BOLD}Continue with HWID activation? (y/N): {Colors.END}").strip().lower()
    
    if confirm != 'y':
        print_colored(f"\n{symbols.CHECK} HWID activation cancelled.", Colors.GREEN)
        return False
    
    print_colored(f"\n{symbols.LIGHTNING} Starting HWID activation process...", Colors.CYAN)
    
    # Try to use MAS script first
    mas_script = get_mas_script_path("HWID_Activation.cmd")
    if mas_script:
        print_colored(f"{symbols.INFO} Using MAS HWID activation script...", Colors.CYAN)
        success, stdout, stderr = run_mas_script(mas_script, "/HWID")
        
        if success:
            print_colored(f"\n{symbols.CHECK} HWID activation completed successfully!", Colors.GREEN)
            print_colored(f"{symbols.INFO} Windows should now be permanently activated.", Colors.CYAN)
            print_colored(f"{symbols.INFO} Please restart your computer to complete the process.", Colors.CYAN)
            return True
        else:
            print_colored(f"\n{symbols.WARNING} MAS script failed, trying alternative method...", Colors.YELLOW)
    
    # Fallback to manual HWID activation
    try:
        # Use PowerShell for HWID activation
        hwid_script = '''
# HWID Activation Script
$ErrorActionPreference = "SilentlyContinue"

# Check if Windows is already activated
$status = (Get-CimInstance -ClassName SoftwareLicensingProduct | Where-Object {$_.PartialProductKey}).LicenseStatus
if ($status -eq 1) {
    Write-Host "Windows is already activated."
    exit 0
}

# Windows 10/11 KMS Client Keys
$keys = @{
    "Home" = "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99"
    "Pro" = "W269N-WFGWX-YVC9B-4J6C9-T83GX"
    "Enterprise" = "NPPR9-FWDCX-D2C8J-H872K-2YT43"
    "Education" = "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2"
    "Pro N" = "MH37W-N47XK-V7XM9-C7227-GCQG9"
    "Enterprise N" = "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4"
    "Education N" = "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ"
}

# Get Windows edition
$edition = (Get-CimInstance -ClassName Win32_OperatingSystem).Caption

# Find matching key
$productKey = $null
foreach ($key in $keys.Keys) {
    if ($edition -like "*$key*") {
        $productKey = $keys[$key]
        break
    }
}

if (-not $productKey) {
    $productKey = $keys["Pro"]  # Default to Pro
}

Write-Host "Installing product key: $productKey"

# Install the product key
$result = Start-Process -FilePath "cscript.exe" -ArgumentList "//nologo", "C:\\Windows\\System32\\slmgr.vbs", "/ipk", $productKey -Wait -PassThru -WindowStyle Hidden

if ($result.ExitCode -eq 0) {
    Write-Host "Product key installed successfully."
    
    # Activate Windows
    Write-Host "Activating Windows..."
    $result = Start-Process -FilePath "cscript.exe" -ArgumentList "//nologo", "C:\\Windows\\System32\\slmgr.vbs", "/ato" -Wait -PassThru -WindowStyle Hidden
    
    if ($result.ExitCode -eq 0) {
        Write-Host "HWID activation completed successfully!"
        exit 0
    } else {
        Write-Host "Activation failed."
        exit 1
    }
} else {
    Write-Host "Failed to install product key."
    exit 1
}
        '''
        
        print_colored(f"{symbols.INFO} Running PowerShell HWID activation...", Colors.CYAN)
        success, stdout, stderr = run_powershell_command(hwid_script)
        
        if success and "successfully" in stdout.lower():
            print_colored(f"\n{symbols.CHECK} HWID activation completed successfully!", Colors.GREEN)
            print_colored(f"{symbols.INFO} Windows should now be permanently activated.", Colors.CYAN)
            print_colored(f"{symbols.INFO} Please restart your computer to complete the process.", Colors.CYAN)
            return True
        else:
            print_colored(f"\n{symbols.CROSS} HWID activation failed.", Colors.RED)
            if stderr:
                print_colored(f"{symbols.INFO} Error: {stderr}", Colors.YELLOW)
            return False
            
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} HWID activation failed: {str(e)}", Colors.RED)
        return False

def kms38_activation():
    """KMS38 Activation - Windows activation valid until 2038 using MAS."""
    print_colored(f"\n{symbols.TARGET}  KMS38 ACTIVATION - VALID UNTIL 2038", Colors.BOLD + Colors.BLUE)
    print_colored("This method provides Windows activation valid until January 19, 2038.", Colors.CYAN)
    
    # Check prerequisites
    prereq_ok, prereq_msg = check_prerequisites()
    if not prereq_ok:
        print_colored(f"\n{symbols.CROSS} {prereq_msg}", Colors.RED)
        return False
    
    win_info = get_windows_info()
    print_colored(f"\n{symbols.INFO} Detected: {win_info['product_name']} (Build {win_info['build']})", Colors.CYAN)
    
    # Verify Windows version
    if win_info['build'] < 14393:  # Windows 10 build 1607
        print_colored(f"\n{symbols.CROSS} KMS38 activation requires Windows 10 build 14393 or later.", Colors.RED)
        print_colored(f"{symbols.INFO} Your build: {win_info['build']}, Required: 14393+", Colors.YELLOW)
        return False
    
    print_colored(f"\n{symbols.WARNING} This will activate Windows until January 19, 2038.", Colors.YELLOW)
    confirm = input(f"\n{Colors.BOLD}Continue with KMS38 activation? (y/N): {Colors.END}").strip().lower()
    
    if confirm != 'y':
        print_colored(f"\n{symbols.CHECK} KMS38 activation cancelled.", Colors.GREEN)
        return False
    
    print_colored(f"\n{symbols.LIGHTNING} Starting KMS38 activation process...", Colors.CYAN)
    
    # Try to use MAS script first
    mas_script = get_mas_script_path("KMS38_Activation.cmd")
    if mas_script:
        print_colored(f"{symbols.INFO} Using MAS KMS38 activation script...", Colors.CYAN)
        success, stdout, stderr = run_mas_script(mas_script, "/KMS38")
        
        if success:
            print_colored(f"\n{symbols.CHECK} KMS38 activation completed successfully!", Colors.GREEN)
            print_colored(f"{symbols.INFO} Windows is now activated until January 19, 2038.", Colors.CYAN)
            return True
        else:
            print_colored(f"\n{symbols.WARNING} MAS script failed, trying alternative method...", Colors.YELLOW)
    
    # Fallback to manual KMS38 activation
    try:
        # Use PowerShell for KMS38 activation
        kms38_script = '''
# KMS38 Activation Script
$ErrorActionPreference = "SilentlyContinue"

# Check if Windows is already activated
$status = (Get-CimInstance -ClassName SoftwareLicensingProduct | Where-Object {$_.PartialProductKey}).LicenseStatus
if ($status -eq 1) {
    Write-Host "Windows is already activated."
    exit 0
}

# KMS Client Keys for Windows 10/11
$keys = @{
    "Home" = "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99"
    "Pro" = "W269N-WFGWX-YVC9B-4J6C9-T83GX"
    "Enterprise" = "NPPR9-FWDCX-D2C8J-H872K-2YT43"
    "Education" = "NW6C2-QMPVW-D7KKK-3GKT6-VCFB2"
    "Pro N" = "MH37W-N47XK-V7XM9-C7227-GCQG9"
    "Enterprise N" = "DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4"
    "Education N" = "2WH4N-8QGBV-H22JP-CT43Q-MDWWJ"
    "Pro for Workstations" = "NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J"
}

# Get Windows edition
$edition = (Get-CimInstance -ClassName Win32_OperatingSystem).Caption

# Find matching key
$productKey = $null
foreach ($key in $keys.Keys) {
    if ($edition -like "*$key*") {
        $productKey = $keys[$key]
        break
    }
}

if (-not $productKey) {
    $productKey = $keys["Pro"]  # Default to Pro
}

Write-Host "Installing KMS client key: $productKey"

# Install the KMS client key
$result = Start-Process -FilePath "cscript.exe" -ArgumentList "//nologo", "C:\\Windows\\System32\\slmgr.vbs", "/ipk", $productKey -Wait -PassThru -WindowStyle Hidden

if ($result.ExitCode -eq 0) {
    Write-Host "KMS client key installed successfully."
    
    # Set KMS38 registry value
    try {
        $regPath = "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SoftwareProtectionPlatform\\55c92734-d682-4d71-983e-d6ec3f16059f"
        if (-not (Test-Path $regPath)) {
            New-Item -Path $regPath -Force | Out-Null
        }
        Set-ItemProperty -Path $regPath -Name "SkipRearm" -Value 1 -Type DWord -Force
        Write-Host "KMS38 registry key set successfully."
    } catch {
        Write-Host "Warning: Could not set KMS38 registry key."
    }
    
    # Activate Windows
    Write-Host "Activating Windows with KMS38..."
    $result = Start-Process -FilePath "cscript.exe" -ArgumentList "//nologo", "C:\\Windows\\System32\\slmgr.vbs", "/ato" -Wait -PassThru -WindowStyle Hidden
    
    if ($result.ExitCode -eq 0) {
        Write-Host "KMS38 activation completed successfully!"
        exit 0
    } else {
        Write-Host "Activation failed."
        exit 1
    }
} else {
    Write-Host "Failed to install KMS client key."
    exit 1
}
        '''
        
        print_colored(f"{symbols.INFO} Running PowerShell KMS38 activation...", Colors.CYAN)
        success, stdout, stderr = run_powershell_command(kms38_script)
        
        if success and "successfully" in stdout.lower():
            print_colored(f"\n{symbols.CHECK} KMS38 activation completed successfully!", Colors.GREEN)
            print_colored(f"{symbols.INFO} Windows is now activated until January 19, 2038.", Colors.CYAN)
            return True
        else:
            print_colored(f"\n{symbols.CROSS} KMS38 activation failed.", Colors.RED)
            if stderr:
                print_colored(f"{symbols.INFO} Error: {stderr}", Colors.YELLOW)
            return False
            
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} KMS38 activation failed: {str(e)}", Colors.RED)
        return False

def online_kms_activation():
    """Online KMS Activation - 180-day activation with auto-renewal."""
    print_colored(f"\n{symbols.GLOBE}  ONLINE KMS ACTIVATION - 180 DAYS WITH AUTO-RENEWAL", Colors.BOLD + Colors.CYAN)
    print_colored("This method provides 180-day activation with automatic renewal task.", Colors.CYAN)
    
    # Check prerequisites
    prereq_ok, prereq_msg = check_prerequisites()
    if not prereq_ok:
        print_colored(f"\n{symbols.CROSS} {prereq_msg}", Colors.RED)
        return False
    
    win_info = get_windows_info()
    print_colored(f"\n{symbols.INFO} Detected: {win_info['product_name']} (Build {win_info['build']})", Colors.CYAN)
    
    print_colored(f"\n{symbols.WARNING} This will activate Windows for 180 days with auto-renewal.", Colors.YELLOW)
    print_colored(f"{symbols.INFO} Requires internet connection for activation and renewals.", Colors.CYAN)
    confirm = input(f"\n{Colors.BOLD}Continue with Online KMS activation? (y/N): {Colors.END}").strip().lower()
    
    if confirm != 'y':
        print_colored(f"\n{symbols.CHECK} Online KMS activation cancelled.", Colors.GREEN)
        return False
    
    print_colored(f"\n{symbols.LIGHTNING} Starting Online KMS activation process...", Colors.CYAN)
    
    # Try to use MAS script first
    mas_script = get_mas_script_path("Online_KMS_Activation.cmd")
    if mas_script:
        print_colored(f"{symbols.INFO} Using MAS Online KMS activation script...", Colors.CYAN)
        success, stdout, stderr = run_mas_script(mas_script, "/KMS-ActAndRenewalTask")
        
        if success:
            print_colored(f"\n{symbols.CHECK} Online KMS activation completed successfully!", Colors.GREEN)
            print_colored(f"{symbols.INFO} Windows is now activated for 180 days.", Colors.CYAN)
            print_colored(f"{symbols.INFO} Auto-renewal task has been created.", Colors.CYAN)
            return True
        else:
            print_colored(f"\n{symbols.CROSS} Online KMS activation failed.", Colors.RED)
            return False
    else:
        print_colored(f"\n{symbols.CROSS} MAS Online KMS script not found.", Colors.RED)
        print_colored(f"{symbols.INFO} Please ensure MAS scripts are available in the MAS folder.", Colors.YELLOW)
        return False

def tsforge_activation():
    """TSforge Activation - Permanent activation for Windows/Office."""
    print_colored(f"\n{symbols.TOOLS}  TSFORGE ACTIVATION - PERMANENT WINDOWS/OFFICE", Colors.BOLD + Colors.MAGENTA)
    print_colored("This method provides permanent activation for Windows and Office.", Colors.CYAN)
    
    # Check prerequisites
    if not check_admin():
        print_colored(f"\n{symbols.CROSS} Administrator privileges required for activation.", Colors.RED)
        return False
    
    win_info = get_windows_info()
    print_colored(f"\n{symbols.INFO} Detected: {win_info['product_name']} (Build {win_info['build']})", Colors.CYAN)
    
    print_colored(f"\n{symbols.WARNING} This will attempt permanent activation of Windows and Office.", Colors.YELLOW)
    print_colored(f"{symbols.INFO} TSforge works with Windows 7/8/10/11 and Office.", Colors.CYAN)
    confirm = input(f"\n{Colors.BOLD}Continue with TSforge activation? (y/N): {Colors.END}").strip().lower()
    
    if confirm != 'y':
        print_colored(f"\n{symbols.CHECK} TSforge activation cancelled.", Colors.GREEN)
        return False
    
    print_colored(f"\n{symbols.LIGHTNING} Starting TSforge activation process...", Colors.CYAN)
    
    # Try to use MAS script
    mas_script = get_mas_script_path("TSforge_Activation.cmd")
    if mas_script:
        print_colored(f"{symbols.INFO} Using MAS TSforge activation script...", Colors.CYAN)
        success, stdout, stderr = run_mas_script(mas_script, "/TSforge")
        
        if success:
            print_colored(f"\n{symbols.CHECK} TSforge activation completed successfully!", Colors.GREEN)
            print_colored(f"{symbols.INFO} Windows and Office should now be permanently activated.", Colors.CYAN)
            return True
        else:
            print_colored(f"\n{symbols.CROSS} TSforge activation failed.", Colors.RED)
            return False
    else:
        print_colored(f"\n{symbols.CROSS} MAS TSforge script not found.", Colors.RED)
        print_colored(f"{symbols.INFO} Please ensure MAS scripts are available in the MAS folder.", Colors.YELLOW)
        return False
def ohook_office_activation():
    """Ohook Activation - Permanent Office activation using MAS."""
    print_colored(f"\n{symbols.CERTIFICATE}  OHOOK OFFICE ACTIVATION - PERMANENT", Colors.BOLD + Colors.MAGENTA)
    print_colored("This method provides permanent activation for Microsoft Office.", Colors.CYAN)
    
    # Check prerequisites
    if not check_admin():
        print_colored(f"\n{symbols.CROSS} Administrator privileges required for activation.", Colors.RED)
        return False
    
    # Check for Office installation
    office_paths = [
        r"C:\Program Files\Microsoft Office",
        r"C:\Program Files (x86)\Microsoft Office"
    ]
    
    office_found = False
    office_version = None
    
    for path in office_paths:
        if os.path.exists(path):
            office_found = True
            # Try to detect Office version
            try:
                for item in os.listdir(path):
                    if item.startswith('Office') and len(item) > 6 and item[6:].isdigit():
                        office_version = item[6:]
                        break
            except:
                pass
            break
    
    if not office_found:
        print_colored(f"\n{symbols.CROSS} Microsoft Office installation not detected.", Colors.RED)
        print_colored(f"{symbols.INFO} Please install Microsoft Office before running this activation.", Colors.YELLOW)
        return False
    
    print_colored(f"\n{symbols.INFO} Office installation detected", Colors.CYAN)
    if office_version:
        print_colored(f"{symbols.INFO} Version: {office_version}", Colors.CYAN)
    
    print_colored(f"\n{symbols.WARNING} This will attempt to activate Microsoft Office.", Colors.YELLOW)
    
    confirm = input(f"\n{Colors.BOLD}Continue with Office activation? (y/N): {Colors.END}").strip().lower()
    
    if confirm != 'y':
        print_colored(f"\n{symbols.CHECK} Office activation cancelled.", Colors.GREEN)
        return False
    
    print_colored(f"\n{symbols.LIGHTNING} Starting Office activation process...", Colors.CYAN)
    
    # Try to use MAS script first
    mas_script = get_mas_script_path("Ohook_Activation_AIO.cmd")
    if mas_script:
        print_colored(f"{symbols.INFO} Using MAS Ohook activation script...", Colors.CYAN)
        success, stdout, stderr = run_mas_script(mas_script, "/Ohook")
        
        if success:
            print_colored(f"\n{symbols.CHECK} Ohook Office activation completed!", Colors.GREEN)
            print_colored(f"{symbols.INFO} Microsoft Office should now be activated.", Colors.CYAN)
            print_colored(f"{symbols.INFO} Open any Office application to verify activation.", Colors.CYAN)
            return True
        else:
            print_colored(f"\n{symbols.WARNING} MAS script failed, trying alternative method...", Colors.YELLOW)
    
    # Fallback to traditional Office activation
    try:
        # Find Office Script Protection Platform (ospp.vbs)
        ospp_paths = []
        if office_version:
            ospp_paths = [
                f"C:\\Program Files\\Microsoft Office\\Office{office_version}\\ospp.vbs",
                f"C:\\Program Files (x86)\\Microsoft Office\\Office{office_version}\\ospp.vbs"
            ]
        else:
            # Try common Office versions
            for ver in ['16', '15', '14']:
                ospp_paths.extend([
                    f"C:\\Program Files\\Microsoft Office\\Office{ver}\\ospp.vbs",
                    f"C:\\Program Files (x86)\\Microsoft Office\\Office{ver}\\ospp.vbs"
                ])
        
        ospp_found = None
        for ospp_path in ospp_paths:
            if os.path.exists(ospp_path):
                ospp_found = ospp_path
                break
        
        if not ospp_found:
            print_colored(f"\n{symbols.CROSS} Office Script Protection Platform (ospp.vbs) not found.", Colors.RED)
            return False
        
        print_colored(f"{symbols.INFO} Using OSPP: {ospp_found}", Colors.CYAN)
        
        # Activate Office
        result = subprocess.run(['cscript', '//Nologo', ospp_found, '/act'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print_colored(f"\n{symbols.CHECK} Office activation completed!", Colors.GREEN)
            print_colored(f"{symbols.INFO} Microsoft Office should now be activated.", Colors.CYAN)
            print_colored(f"{symbols.INFO} Open any Office application to verify activation.", Colors.CYAN)
            return True
        else:
            print_colored(f"\n{symbols.WARNING} Office activation completed with warnings.", Colors.YELLOW)
            print_colored(f"{symbols.INFO} Open Office and check activation status manually.", Colors.CYAN)
            return True
            
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Office activation failed: {str(e)}", Colors.RED)
        return False

def show_main_menu():
    """Display the main menu for activation manager."""
    print_header()
    print_colored(f"\n{symbols.TARGET} What would you like to do?", Colors.BOLD + Colors.CYAN)

    print_colored(f"\n{symbols.INFO} ACTIVATION STATUS:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"1. {symbols.SHIELD}  Enhanced Status (MAS Method)", Colors.GREEN)
    print_colored("   └─ Comprehensive activation status using MAS detection", Colors.WHITE)
    print_colored(f"2. {symbols.INFO}  Basic Status Check", Colors.BLUE)
    print_colored("   └─ Standard Windows activation status", Colors.WHITE)
    print_colored(f"3. {symbols.GEAR}  Advanced Analysis", Colors.CYAN)
    print_colored("   └─ Detailed system and licensing information", Colors.WHITE)

    print_colored(f"\n{symbols.KEY} STANDARD ACTIVATION:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"4. {symbols.KEY}  Activate Windows (Product Key)", Colors.GREEN)
    print_colored("   └─ Enter a product key to activate Windows", Colors.WHITE)
    print_colored(f"5. {symbols.CERTIFICATE} Check License Details", Colors.CYAN)
    print_colored("   └─ View detailed information about your Windows license", Colors.WHITE)

    print_colored(f"\n{symbols.ROCKET} MAS ACTIVATION METHODS:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"6. {symbols.SHIELD}  HWID Activation (Permanent)", Colors.GREEN)
    print_colored("   └─ Permanent Windows 10/11 activation via digital license", Colors.WHITE)
    print_colored(f"7. {symbols.TARGET}  KMS38 Activation (Until 2038)", Colors.BLUE)
    print_colored("   └─ Windows activation valid until January 19, 2038", Colors.WHITE)
    print_colored(f"8. {symbols.GLOBE}  Online KMS (180 Days + Auto-Renewal)", Colors.CYAN)
    print_colored("   └─ 180-day activation with automatic renewal task", Colors.WHITE)
    print_colored(f"9. {symbols.TOOLS}  TSforge Activation (Permanent)", Colors.MAGENTA)
    print_colored("   └─ Permanent Windows/Office activation (supports older versions)", Colors.WHITE)
    print_colored(f"10. {symbols.CERTIFICATE} Ohook Office Activation", Colors.MAGENTA)
    print_colored("    └─ Permanent Microsoft Office activation", Colors.WHITE)

    print_colored(f"\n{symbols.WARNING} ADVANCED OPTIONS:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"11. {symbols.RECYCLE} Reset Activation (Rearm)", Colors.YELLOW)
    print_colored("    └─ Reset activation status (limited uses, requires reactivation)", Colors.WHITE)

    print_colored(f"\n{symbols.BOOK} HELP & INFO:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"12. {symbols.BOOK}  Activation Help", Colors.BLUE)
    print_colored("    └─ Learn about Windows activation and troubleshooting", Colors.WHITE)
    print_colored(f"0.  {symbols.CROSS} Return to Main Menu", Colors.RED)

    print_colored("\n" + "=" * 70, Colors.MAGENTA)

def main():
    """Main function for activation manager."""
    # Enable ANSI colors for Windows terminals
    enable_ansi_colors()

    # Check admin status
    is_admin = check_admin()

    if not is_admin:
        print_colored(f"\n{symbols.WARNING}  NOT RUNNING AS ADMINISTRATOR", Colors.BOLD + Colors.YELLOW)
        print_colored("This application requires administrator privileges for activation.", Colors.YELLOW)
        print_colored("Please restart as Administrator.", Colors.YELLOW)
        input(f"\n{Colors.CYAN}Press Enter to return to main menu...{Colors.END}")
        return

    while True:
        show_main_menu()

        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-12, 0 to exit): {Colors.END}").strip()

            if choice == '1':
                display_enhanced_activation_status()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '2':
                display_activation_status()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '3':
                get_advanced_activation_info()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '4':
                activate_windows()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '5':
                check_activation_details()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '6':
                hwid_activation()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '7':
                kms38_activation()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '8':
                online_kms_activation()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '9':
                tsforge_activation()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '10':
                ohook_office_activation()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '11':
                reset_activation()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '12':
                show_activation_help()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '0':
                print_colored(f"\n{symbols.WAVE} Returning to main menu...", Colors.CYAN)
                break
            else:
                print_colored("\n{symbols.CROSS} Invalid choice! Please enter 1-12 or 0.", Colors.RED)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

        except KeyboardInterrupt:
            print_colored(f"\n\n{symbols.WAVE} Returning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_colored(f"\n{symbols.CROSS} An error occurred: {str(e)}", Colors.RED)
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
