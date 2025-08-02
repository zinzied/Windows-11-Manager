#!/usr/bin/env python3
"""
Telemetry & Privacy Management Module for Windows 11 Update Manager
This module provides functionality to disable Windows telemetry and enhance privacy.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import winreg
import os
import sys
from pathlib import Path

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(text, color=Colors.WHITE):
    """Print text with color."""
    print(f"{color}{text}{Colors.END}")

def print_header(title):
    """Print a section header."""
    print_colored(f"\n{'=' * 60}", Colors.CYAN)
    print_colored(f"🔒 {title}", Colors.BOLD + Colors.CYAN)
    print_colored(f"{'=' * 60}", Colors.CYAN)

def print_success(message):
    """Print success message."""
    print_colored(f"✅ {message}", Colors.GREEN)

def print_error(message):
    """Print error message."""
    print_colored(f"❌ {message}", Colors.RED)

def print_warning(message):
    """Print warning message."""
    print_colored(f"⚠️  {message}", Colors.YELLOW)

def print_info(message):
    """Print info message."""
    print_colored(f"ℹ️  {message}", Colors.BLUE)

def run_command(command, description):
    """Run a command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description}")
        else:
            print_error(f"{description} - {result.stderr.strip()}")
    except Exception as e:
        print_error(f"{description} - {str(e)}")

def disable_telemetry_services():
    """Disable telemetry and diagnostic services."""
    print_header("Disabling Telemetry Services")
    
    services = [
        "DiagTrack",  # Connected User Experiences and Telemetry
        "dmwappushservice",  # Device Management Wireless Application Protocol
        "WerSvc",  # Windows Error Reporting Service
        "WSearch",  # Windows Search (optional)
        "RetailDemo",  # Retail Demo Service
        "Fax",  # Fax Service
    ]
    
    for service in services:
        run_command(f'sc stop "{service}"', f"Stopping {service}")
        run_command(f'sc config "{service}" start= disabled', f"Disabling {service}")

def disable_telemetry_registry():
    """Modify registry to disable telemetry."""
    print_header("Disabling Telemetry via Registry")
    
    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "values": [
                ("AllowTelemetry", winreg.REG_DWORD, 0),
                ("DoNotShowFeedbackNotifications", winreg.REG_DWORD, 1),
                ("DisableOneSettingsDownloads", winreg.REG_DWORD, 1),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection",
            "values": [
                ("AllowTelemetry", winreg.REG_DWORD, 0),
                ("MaxTelemetryAllowed", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy",
            "values": [
                ("TailoredExperiencesWithDiagnosticDataEnabled", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Diagnostics\DiagTrack",
            "values": [
                ("ShowedToastAtLevel", winreg.REG_DWORD, 1),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Set registry value: {reg_change['subkey']}\\{value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to modify registry: {reg_change['subkey']} - {str(e)}")

def disable_advertising_id():
    """Disable Windows advertising ID."""
    print_header("Disabling Advertising ID")
    
    registry_changes = [
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo",
            "values": [
                ("Enabled", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo",
            "values": [
                ("DisabledByGroupPolicy", winreg.REG_DWORD, 1),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Disabled advertising ID: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to disable advertising ID: {str(e)}")

def disable_location_tracking():
    """Disable location tracking."""
    print_header("Disabling Location Tracking")
    
    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors",
            "values": [
                ("DisableLocation", winreg.REG_DWORD, 1),
                ("DisableLocationScripting", winreg.REG_DWORD, 1),
                ("DisableSensors", winreg.REG_DWORD, 1),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\DeviceAccess\Global\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}",
            "values": [
                ("Value", winreg.REG_SZ, "Deny"),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Disabled location tracking: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to disable location tracking: {str(e)}")

def disable_activity_history():
    """Disable activity history and timeline."""
    print_header("Disabling Activity History")
    
    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\System",
            "values": [
                ("EnableActivityFeed", winreg.REG_DWORD, 0),
                ("PublishUserActivities", winreg.REG_DWORD, 0),
                ("UploadUserActivities", winreg.REG_DWORD, 0),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Disabled activity history: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to disable activity history: {str(e)}")

def disable_feedback_notifications():
    """Disable Windows feedback notifications."""
    print_header("Disabling Feedback Notifications")
    
    registry_changes = [
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Siuf\Rules",
            "values": [
                ("NumberOfSIUFInPeriod", winreg.REG_DWORD, 0),
                ("PeriodInNanoSeconds", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "values": [
                ("DoNotShowFeedbackNotifications", winreg.REG_DWORD, 1),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Disabled feedback notifications: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to disable feedback notifications: {str(e)}")

def disable_telemetry_tasks():
    """Disable telemetry scheduled tasks."""
    print_header("Disabling Telemetry Scheduled Tasks")
    
    tasks = [
        r"\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser",
        r"\Microsoft\Windows\Application Experience\ProgramDataUpdater",
        r"\Microsoft\Windows\Autochk\Proxy",
        r"\Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
        r"\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip",
        r"\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector",
        r"\Microsoft\Windows\Feedback\Siuf\DmClient",
        r"\Microsoft\Windows\Feedback\Siuf\DmClientOnScenarioDownload",
        r"\Microsoft\Windows\Windows Error Reporting\QueueReporting",
    ]
    
    for task in tasks:
        run_command(f'schtasks /change /tn "{task}" /disable', f"Disabling task: {task}")

def disable_all_telemetry():
    """Disable all telemetry and privacy invasive features."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored("🔒 COMPREHENSIVE TELEMETRY & PRIVACY DISABLE", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 70, Colors.MAGENTA)
    
    print_warning("This will disable Windows telemetry and enhance privacy!")
    print_info("This may affect some Windows features and error reporting.")
    
    confirm = input(f"\n{Colors.YELLOW}Do you want to continue? (y/N): {Colors.END}").lower().strip()
    if confirm != 'y':
        print_colored("Operation cancelled by user.", Colors.CYAN)
        return
    
    print_info("Starting telemetry and privacy enhancement process...")
    
    disable_telemetry_services()
    disable_telemetry_registry()
    disable_advertising_id()
    disable_location_tracking()
    disable_activity_history()
    disable_feedback_notifications()
    disable_telemetry_tasks()
    
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success("Telemetry and privacy enhancement completed!")
    print_colored("=" * 60, Colors.GREEN)
    print_warning("A system restart is recommended for all changes to take effect.")
    print_info("Your privacy has been significantly enhanced.")

def show_telemetry_menu():
    """Display telemetry management menu."""
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored("🔒 TELEMETRY & PRIVACY MANAGEMENT", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored("\n📋 Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored("\n1. 🚫 Disable All Telemetry & Enhance Privacy", Colors.RED)
    print_colored("2. 📊 Disable Telemetry Services Only", Colors.YELLOW)
    print_colored("3. 📝 Disable Advertising ID Only", Colors.YELLOW)
    print_colored("4. 📍 Disable Location Tracking Only", Colors.YELLOW)
    print_colored("5. 📈 Check Telemetry Status", Colors.BLUE)
    print_colored("6. 🔙 Return to Main Menu", Colors.CYAN)

def check_telemetry_status():
    """Check current telemetry status."""
    print_header("Checking Telemetry Status")
    
    # Check DiagTrack service
    try:
        result = subprocess.run('sc query "DiagTrack"', shell=True, capture_output=True, text=True)
        if "RUNNING" in result.stdout:
            print_colored("DiagTrack Service: RUNNING (Telemetry Active)", Colors.RED)
        elif "STOPPED" in result.stdout:
            print_colored("DiagTrack Service: STOPPED (Telemetry Disabled)", Colors.GREEN)
        else:
            print_colored("DiagTrack Service: UNKNOWN", Colors.YELLOW)
    except:
        print_colored("DiagTrack Service: ERROR CHECKING", Colors.YELLOW)
    
    # Check telemetry registry
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection")
        value, _ = winreg.QueryValueEx(key, "AllowTelemetry")
        if value == 0:
            print_colored("Telemetry Registry: DISABLED", Colors.GREEN)
        else:
            print_colored("Telemetry Registry: ENABLED", Colors.RED)
        winreg.CloseKey(key)
    except FileNotFoundError:
        print_colored("Telemetry Registry: DEFAULT (Enabled)", Colors.RED)
    except Exception as e:
        print_colored(f"Telemetry Registry: ERROR - {str(e)}", Colors.YELLOW)

def main():
    """Main telemetry management function."""
    while True:
        show_telemetry_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-6): {Colors.END}").strip()
            
            if choice == '1':
                disable_all_telemetry()
            elif choice == '2':
                disable_telemetry_services()
            elif choice == '3':
                disable_advertising_id()
            elif choice == '4':
                disable_location_tracking()
            elif choice == '5':
                check_telemetry_status()
            elif choice == '6':
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-6.")
            
            if choice in ['1', '2', '3', '4', '5']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nReturning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
