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

def stop_onedrive_processes():
    """Stop all OneDrive processes."""
    print_colored(f"\n{symbols.STOP} Stopping OneDrive Processes", Colors.BOLD + Colors.CYAN)
    
    processes = [
        "OneDrive.exe",
        "OneDriveStandaloneUpdater.exe",
        "FileCoAuth.exe"
    ]
    
    for process in processes:
        run_command(f'taskkill /f /im "{process}"', f"Stopping {process}")

def disable_onedrive_services():
    """Disable OneDrive related services."""
    print_colored(f"\n{symbols.GEAR} Disabling OneDrive Services", Colors.BOLD + Colors.CYAN)
    
    services = [
        "OneSyncSvc",  # OneDrive Sync Service
        "OneSyncSvc_Session1",  # OneDrive Sync Service Session
    ]
    
    for service in services:
        run_command(f'sc stop "{service}"', f"Stopping {service}")
        run_command(f'sc config "{service}" start= disabled', f"Disabling {service}")

def modify_onedrive_registry():
    """Modify registry to disable OneDrive."""
    print_colored(f"\n{symbols.TOOLS} Modifying OneDrive Registry Settings", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"\n{symbols.TRASH} Removing OneDrive from Startup", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"\n{symbols.TRASH} Uninstalling OneDrive Application", Colors.BOLD + Colors.CYAN)
    
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
    print_colored(f"{symbols.CLOUD} ONEDRIVE COMPLETE DISABLE PROCESS", Colors.BOLD + Colors.MAGENTA)
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
    clear_screen()
    print_header("ONEDRIVE MANAGEMENT")
    print_colored(f"\n{symbols.TARGET} Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. {symbols.BLOCK} Disable OneDrive Completely", Colors.RED)
    print_colored(f"2. {symbols.RECYCLE} Restore OneDrive (Basic)", Colors.GREEN)
    print_colored(f"3. {symbols.INFO} Check OneDrive Status", Colors.BLUE)
    print_colored(f"4. {symbols.WAVE} Return to Main Menu", Colors.YELLOW)

def check_onedrive_status():
    """Check current OneDrive status."""
    print_colored(f"\n{symbols.INFO} Checking OneDrive Status", Colors.BOLD + Colors.CYAN)
    
    # Check if OneDrive process is running
    try:
        result = subprocess.run('tasklist /fi "imagename eq OneDrive.exe"', shell=True, capture_output=True, text=True)
        if "OneDrive.exe" in result.stdout:
            print_colored(f"{symbols.CHECK} OneDrive Process: RUNNING", Colors.GREEN)
        else:
            print_colored(f"{symbols.CROSS} OneDrive Process: NOT RUNNING", Colors.RED)
    except:
        print_colored(f"{symbols.WARNING} OneDrive Process: ERROR CHECKING", Colors.YELLOW)
    
    # Check registry settings
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\OneDrive")
        print_colored(f"{symbols.BLOCK} OneDrive Policies: DISABLED", Colors.RED)
        winreg.CloseKey(key)
    except FileNotFoundError:
        print_colored(f"{symbols.CHECK} OneDrive Policies: ENABLED", Colors.GREEN)
    except Exception as e:
        print_colored(f"{symbols.WARNING} OneDrive Policies: ERROR - {str(e)}", Colors.YELLOW)

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
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print_warning("Not running as Administrator. Some features may fail.")
    main()
