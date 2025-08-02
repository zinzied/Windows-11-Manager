#!/usr/bin/env python3
"""
Comprehensive Restore Script for Windows 11 System Manager
This script restores all system modifications made by the various modules.

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
    print_colored(f"🔄 {title}", Colors.BOLD + Colors.CYAN)
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

def restore_windows_updates():
    """Restore Windows Update functionality."""
    print_header("Restoring Windows Updates")
    
    # Re-enable services
    services = ["wuauserv", "bits", "dosvc", "UsoSvc"]
    for service in services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Remove registry modifications
    keys_to_delete = [
        r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
        r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",
    ]
    
    for subkey in keys_to_delete:
        try:
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, subkey)
            print_success(f"Deleted registry key: {subkey}")
        except FileNotFoundError:
            print_success(f"Registry key not found (already clean): {subkey}")
        except Exception as e:
            print_error(f"Failed to delete registry key {subkey}: {str(e)}")

def restore_onedrive():
    """Restore OneDrive functionality."""
    print_header("Restoring OneDrive")
    
    # Re-enable services
    services = ["OneSyncSvc", "OneSyncSvc_Session1"]
    for service in services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Remove OneDrive policy registry keys
    keys_to_delete = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\OneDrive"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}"),
    ]
    
    for root_key, subkey in keys_to_delete:
        try:
            winreg.DeleteKey(root_key, subkey)
            print_success(f"Deleted OneDrive registry key: {subkey}")
        except FileNotFoundError:
            print_success(f"OneDrive registry key not found: {subkey}")
        except Exception as e:
            print_error(f"Failed to delete OneDrive registry key: {str(e)}")

def restore_telemetry():
    """Restore telemetry and diagnostic services."""
    print_header("Restoring Telemetry Services")
    
    # Re-enable telemetry services
    services = ["DiagTrack", "dmwappushservice", "WerSvc"]
    for service in services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Remove telemetry policy registry keys
    keys_to_delete = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors"),
    ]
    
    for root_key, subkey in keys_to_delete:
        try:
            winreg.DeleteKey(root_key, subkey)
            print_success(f"Deleted telemetry registry key: {subkey}")
        except FileNotFoundError:
            print_success(f"Telemetry registry key not found: {subkey}")
        except Exception as e:
            print_error(f"Failed to delete telemetry registry key: {str(e)}")

def restore_performance():
    """Restore performance-related services and settings."""
    print_header("Restoring Performance Settings")
    
    # Re-enable services that might have been disabled
    services = ["WSearch", "SysMain", "Themes"]
    for service in services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Reset power plan to balanced
    run_command(
        'powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e',
        "Setting power plan to Balanced"
    )

def restore_xbox_services():
    """Restore Xbox services."""
    print_header("Restoring Xbox Services")
    
    xbox_services = ["XblAuthManager", "XblGameSave", "XboxGipSvc", "XboxNetApiSvc"]
    for service in xbox_services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")

def comprehensive_restore():
    """Perform comprehensive system restore."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored("🔄 COMPREHENSIVE SYSTEM RESTORE", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 70, Colors.MAGENTA)
    
    print_warning("This will restore all system modifications made by this tool!")
    print_info("This includes: Updates, OneDrive, Telemetry, Performance, Xbox services")
    
    confirm = input(f"\n{Colors.YELLOW}Do you want to continue? (y/N): {Colors.END}").lower().strip()
    if confirm != 'y':
        print_colored("Operation cancelled by user.", Colors.CYAN)
        return
    
    print_info("Starting comprehensive system restore...")
    
    restore_windows_updates()
    restore_onedrive()
    restore_telemetry()
    restore_performance()
    restore_xbox_services()
    
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success("Comprehensive system restore completed!")
    print_colored("=" * 60, Colors.GREEN)
    print_warning("A system restart is recommended for all changes to take effect.")
    print_info("Your system has been restored to default Windows 11 settings.")

def show_restore_menu():
    """Display restore menu."""
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored("🔄 COMPREHENSIVE SYSTEM RESTORE", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored("\n📋 Choose what to restore:", Colors.BOLD + Colors.CYAN)
    print_colored("\n1. 🔄 Restore Everything (Comprehensive)", Colors.RED)
    print_colored("2. 🔄 Restore Windows Updates Only", Colors.YELLOW)
    print_colored("3. ☁️  Restore OneDrive Only", Colors.YELLOW)
    print_colored("4. 🔒 Restore Telemetry Only", Colors.YELLOW)
    print_colored("5. ⚡ Restore Performance Settings Only", Colors.YELLOW)
    print_colored("6. 🎮 Restore Xbox Services Only", Colors.YELLOW)
    print_colored("7. 🔙 Exit", Colors.CYAN)

def main():
    """Main restore function."""
    while True:
        show_restore_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-7): {Colors.END}").strip()
            
            if choice == '1':
                comprehensive_restore()
            elif choice == '2':
                restore_windows_updates()
            elif choice == '3':
                restore_onedrive()
            elif choice == '4':
                restore_telemetry()
            elif choice == '5':
                restore_performance()
            elif choice == '6':
                restore_xbox_services()
            elif choice == '7':
                print_colored("\n👋 Restore operations completed!", Colors.BOLD + Colors.CYAN)
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-7.")
            
            if choice in ['1', '2', '3', '4', '5', '6']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nExiting restore tool...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
