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
import ctypes

try:
    from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info, clear_screen
except ImportError:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info, clear_screen

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
    print_colored(f"\n{symbols.SHIELD} Disabling Telemetry Services", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"\n{symbols.TOOLS} Disabling Telemetry via Registry", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"\n{symbols.BLOCK} Disabling Advertising ID", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"\n{symbols.GLOBE} Disabling Location Tracking", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"\n{symbols.TRASH} Disabling Activity History", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"\n{symbols.BLOCK} Disabling Feedback Notifications", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"\n{symbols.GEAR} Disabling Telemetry Scheduled Tasks", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"{symbols.SHIELD} COMPREHENSIVE TELEMETRY & PRIVACY DISABLE", Colors.BOLD + Colors.MAGENTA)
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
    clear_screen()
    print_header("TELEMETRY & PRIVACY MANAGEMENT")
    print_colored(f"\n{symbols.TARGET} Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. {symbols.SHIELD} Disable All Telemetry & Enhance Privacy", Colors.RED)
    print_colored(f"2. {symbols.GEAR} Disable Telemetry Services Only", Colors.YELLOW)
    print_colored(f"3. {symbols.BLOCK} Disable Advertising ID Only", Colors.YELLOW)
    print_colored(f"4. {symbols.GLOBE} Disable Location Tracking Only", Colors.YELLOW)
    print_colored(f"5. {symbols.INFO} Check Telemetry Status", Colors.BLUE)
    print_colored(f"6. {symbols.WAVE} Return to Main Menu", Colors.CYAN)

def check_telemetry_status():
    """Check current telemetry status."""
    print_colored(f"\n{symbols.INFO} Checking Telemetry Status", Colors.BOLD + Colors.CYAN)
    
    # Check DiagTrack service
    try:
        result = subprocess.run('sc query "DiagTrack"', shell=True, capture_output=True, text=True)
        if "RUNNING" in result.stdout:
            print_colored(f"{symbols.WARNING} DiagTrack Service: RUNNING (Telemetry Active)", Colors.RED)
        elif "STOPPED" in result.stdout:
            print_colored(f"{symbols.CHECK} DiagTrack Service: STOPPED (Telemetry Disabled)", Colors.GREEN)
        else:
            print_colored(f"{symbols.INFO} DiagTrack Service: UNKNOWN", Colors.YELLOW)
    except:
        print_colored(f"{symbols.CROSS} DiagTrack Service: ERROR CHECKING", Colors.YELLOW)
    
    # Check telemetry registry
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection")
        value, _ = winreg.QueryValueEx(key, "AllowTelemetry")
        if value == 0:
            print_colored(f"{symbols.CHECK} Telemetry Registry: DISABLED", Colors.GREEN)
        else:
            print_colored(f"{symbols.WARNING} Telemetry Registry: ENABLED", Colors.RED)
        winreg.CloseKey(key)
    except FileNotFoundError:
        print_colored(f"{symbols.WARNING} Telemetry Registry: DEFAULT (Enabled)", Colors.RED)
    except Exception as e:
        print_colored(f"{symbols.CROSS} Telemetry Registry: ERROR - {str(e)}", Colors.YELLOW)

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
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print_warning("Not running as Administrator. Some features may fail.")
    main()
