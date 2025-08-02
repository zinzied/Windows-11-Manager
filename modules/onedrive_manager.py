#!/usr/bin/env python3
"""
OneDrive Management Module for Windows 11 Update Manager
This module provides functionality to disable/enable OneDrive completely.

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
    print_colored(f"🔧 {title}", Colors.BOLD + Colors.CYAN)
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

def stop_onedrive_processes():
    """Stop all OneDrive processes."""
    print_header("Stopping OneDrive Processes")
    
    processes = [
        "OneDrive.exe",
        "OneDriveStandaloneUpdater.exe",
        "FileCoAuth.exe"
    ]
    
    for process in processes:
        run_command(f'taskkill /f /im "{process}"', f"Stopping {process}")

def disable_onedrive_services():
    """Disable OneDrive related services."""
    print_header("Disabling OneDrive Services")
    
    services = [
        "OneSyncSvc",  # OneDrive Sync Service
        "OneSyncSvc_Session1",  # OneDrive Sync Service Session
    ]
    
    for service in services:
        run_command(f'sc stop "{service}"', f"Stopping {service}")
        run_command(f'sc config "{service}" start= disabled', f"Disabling {service}")

def modify_onedrive_registry():
    """Modify registry to disable OneDrive."""
    print_header("Modifying OneDrive Registry Settings")
    
    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\OneDrive",
            "values": [
                ("DisableFileSyncNGSC", winreg.REG_DWORD, 1),
                ("DisableFileSync", winreg.REG_DWORD, 1),
                ("DisableMeteredNetworkFileSync", winreg.REG_DWORD, 1),
                ("DisableLibrariesDefaultSaveToOneDrive", winreg.REG_DWORD, 1),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\OneDrive",
            "values": [
                ("DisablePersonalSync", winreg.REG_DWORD, 1),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Classes\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}",
            "values": [
                ("System.IsPinnedToNameSpaceTree", winreg.REG_DWORD, 0),
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

def remove_onedrive_startup():
    """Remove OneDrive from startup."""
    print_header("Removing OneDrive from Startup")
    
    startup_locations = [
        r"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"
    ]
    
    for location in startup_locations:
        try:
            if location.startswith("HKEY_CURRENT_USER"):
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, location.split("\\", 1)[1], 0, winreg.KEY_SET_VALUE)
            else:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, location.split("\\", 1)[1], 0, winreg.KEY_SET_VALUE)
            
            try:
                winreg.DeleteValue(key, "OneDrive")
                print_success(f"Removed OneDrive from {location}")
            except FileNotFoundError:
                print_info(f"OneDrive not found in {location}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to access {location}: {str(e)}")

def uninstall_onedrive():
    """Uninstall OneDrive application."""
    print_header("Uninstalling OneDrive Application")
    
    # Try to find OneDrive setup
    onedrive_paths = [
        r"C:\Windows\System32\OneDriveSetup.exe",
        r"C:\Windows\SysWOW64\OneDriveSetup.exe",
        os.path.expanduser(r"~\AppData\Local\Microsoft\OneDrive\OneDriveSetup.exe")
    ]
    
    for path in onedrive_paths:
        if os.path.exists(path):
            run_command(f'"{path}" /uninstall', f"Uninstalling OneDrive using {path}")
            break
    else:
        print_warning("OneDrive setup not found in common locations")

def disable_onedrive_completely():
    """Disable OneDrive completely."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored("☁️  ONEDRIVE COMPLETE DISABLE PROCESS", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 70, Colors.MAGENTA)
    
    print_warning("This will completely disable OneDrive on your system!")
    print_warning("Make sure to backup any important OneDrive data first!")
    
    confirm = input(f"\n{Colors.YELLOW}Are you sure you want to continue? (y/N): {Colors.END}").lower().strip()
    if confirm != 'y':
        print_colored("Operation cancelled by user.", Colors.CYAN)
        return
    
    print_info("Starting OneDrive disable process...")
    
    stop_onedrive_processes()
    disable_onedrive_services()
    modify_onedrive_registry()
    remove_onedrive_startup()
    uninstall_onedrive()
    
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success("OneDrive disable process completed!")
    print_colored("=" * 60, Colors.GREEN)
    print_warning("A system restart is recommended for all changes to take effect.")
    print_info("OneDrive has been completely disabled on your system.")

def show_onedrive_menu():
    """Display OneDrive management menu."""
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored("☁️  ONEDRIVE MANAGEMENT", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored("\n📋 Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored("\n1. 🚫 Disable OneDrive Completely", Colors.RED)
    print_colored("2. 🔄 Restore OneDrive (Basic)", Colors.GREEN)
    print_colored("3. 📊 Check OneDrive Status", Colors.BLUE)
    print_colored("4. 🔙 Return to Main Menu", Colors.YELLOW)

def check_onedrive_status():
    """Check current OneDrive status."""
    print_header("Checking OneDrive Status")
    
    # Check if OneDrive process is running
    try:
        result = subprocess.run('tasklist /fi "imagename eq OneDrive.exe"', shell=True, capture_output=True, text=True)
        if "OneDrive.exe" in result.stdout:
            print_colored("OneDrive Process: RUNNING", Colors.GREEN)
        else:
            print_colored("OneDrive Process: NOT RUNNING", Colors.RED)
    except:
        print_colored("OneDrive Process: ERROR CHECKING", Colors.YELLOW)
    
    # Check registry settings
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\OneDrive")
        print_colored("OneDrive Policies: DISABLED", Colors.RED)
        winreg.CloseKey(key)
    except FileNotFoundError:
        print_colored("OneDrive Policies: ENABLED", Colors.GREEN)
    except Exception as e:
        print_colored(f"OneDrive Policies: ERROR - {str(e)}", Colors.YELLOW)

def main():
    """Main OneDrive management function."""
    while True:
        show_onedrive_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-4): {Colors.END}").strip()
            
            if choice == '1':
                disable_onedrive_completely()
            elif choice == '2':
                print_info("OneDrive restore functionality will be implemented in comprehensive restore module.")
            elif choice == '3':
                check_onedrive_status()
            elif choice == '4':
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-4.")
            
            if choice in ['1', '2', '3']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nReturning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
