#!/usr/bin/env python3
"""
Bloatware Removal Module for Windows 11 Update Manager
This module provides functionality to remove Windows 11 bloatware and unnecessary apps.

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
    print_colored(f"🗑️  {title}", Colors.BOLD + Colors.CYAN)
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

def run_powershell_command(command, description):
    """Run a PowerShell command and handle errors."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", command], 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print_success(f"{description}")
        else:
            print_error(f"{description} - {result.stderr.strip()}")
    except Exception as e:
        print_error(f"{description} - {str(e)}")

def remove_windows_apps():
    """Remove Windows 11 bloatware apps."""
    print_header("Removing Windows 11 Bloatware Apps")
    
    # List of apps to remove (safe to remove)
    apps_to_remove = [
        "Microsoft.3DBuilder",
        "Microsoft.BingFinance",
        "Microsoft.BingNews",
        "Microsoft.BingSports",
        "Microsoft.BingTranslator",
        "Microsoft.BingWeather",
        "Microsoft.GetHelp",
        "Microsoft.Getstarted",
        "Microsoft.Messaging",
        "Microsoft.Microsoft3DViewer",
        "Microsoft.MicrosoftOfficeHub",
        "Microsoft.MicrosoftSolitaireCollection",
        "Microsoft.MicrosoftStickyNotes",
        "Microsoft.MixedReality.Portal",
        "Microsoft.MSPaint",
        "Microsoft.Office.OneNote",
        "Microsoft.OneConnect",
        "Microsoft.People",
        "Microsoft.Print3D",
        "Microsoft.SkypeApp",
        "Microsoft.Wallet",
        "Microsoft.Windows.Photos",
        "Microsoft.WindowsAlarms",
        "Microsoft.WindowsCamera",
        "microsoft.windowscommunicationsapps",
        "Microsoft.WindowsFeedbackHub",
        "Microsoft.WindowsMaps",
        "Microsoft.WindowsSoundRecorder",
        "Microsoft.Xbox.TCUI",
        "Microsoft.XboxApp",
        "Microsoft.XboxGameOverlay",
        "Microsoft.XboxGamingOverlay",
        "Microsoft.XboxIdentityProvider",
        "Microsoft.XboxSpeechToTextOverlay",
        "Microsoft.YourPhone",
        "Microsoft.ZuneMusic",
        "Microsoft.ZuneVideo",
    ]
    
    print_info(f"Attempting to remove {len(apps_to_remove)} bloatware apps...")
    
    for app in apps_to_remove:
        command = f"Get-AppxPackage {app} | Remove-AppxPackage"
        run_powershell_command(command, f"Removing {app}")

def remove_xbox_services():
    """Remove Xbox-related services and features."""
    print_header("Disabling Xbox Services")
    
    xbox_services = [
        "XblAuthManager",  # Xbox Live Auth Manager
        "XblGameSave",     # Xbox Live Game Save
        "XboxGipSvc",      # Xbox Accessory Management Service
        "XboxNetApiSvc",   # Xbox Live Networking Service
    ]
    
    for service in xbox_services:
        try:
            subprocess.run(f'sc stop "{service}"', shell=True, capture_output=True)
            subprocess.run(f'sc config "{service}" start= disabled', shell=True, capture_output=True)
            print_success(f"Disabled Xbox service: {service}")
        except Exception as e:
            print_error(f"Failed to disable {service}: {str(e)}")

def disable_cortana():
    """Disable Cortana."""
    print_header("Disabling Cortana")
    
    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
            "values": [
                ("AllowCortana", winreg.REG_DWORD, 0),
                ("DisableWebSearch", winreg.REG_DWORD, 1),
                ("ConnectedSearchUseWeb", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search",
            "values": [
                ("SearchboxTaskbarMode", winreg.REG_DWORD, 0),
                ("CortanaConsent", winreg.REG_DWORD, 0),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Disabled Cortana: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to disable Cortana: {str(e)}")

def disable_windows_widgets():
    """Disable Windows 11 widgets."""
    print_header("Disabling Windows 11 Widgets")
    
    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Dsh",
            "values": [
                ("AllowNewsAndInterests", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Feeds",
            "values": [
                ("ShellFeedsTaskbarViewMode", winreg.REG_DWORD, 2),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Disabled widgets: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to disable widgets: {str(e)}")

def disable_edge_integration():
    """Disable Microsoft Edge integration features."""
    print_header("Disabling Microsoft Edge Integration")
    
    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Edge",
            "values": [
                ("HideFirstRunExperience", winreg.REG_DWORD, 1),
                ("DefaultBrowserSettingEnabled", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\MicrosoftEdge\Main",
            "values": [
                ("AllowPrelaunch", winreg.REG_DWORD, 0),
                ("AllowTabPreloading", winreg.REG_DWORD, 0),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Disabled Edge integration: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to disable Edge integration: {str(e)}")

def remove_start_menu_suggestions():
    """Remove Start Menu suggestions and ads."""
    print_header("Removing Start Menu Suggestions")
    
    registry_changes = [
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
            "values": [
                ("SystemPaneSuggestionsEnabled", winreg.REG_DWORD, 0),
                ("SilentInstalledAppsEnabled", winreg.REG_DWORD, 0),
                ("PreInstalledAppsEnabled", winreg.REG_DWORD, 0),
                ("OemPreInstalledAppsEnabled", winreg.REG_DWORD, 0),
                ("ContentDeliveryAllowed", winreg.REG_DWORD, 0),
                ("SubscribedContentEnabled", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\CloudContent",
            "values": [
                ("DisableWindowsConsumerFeatures", winreg.REG_DWORD, 1),
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Disabled Start Menu suggestion: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to disable Start Menu suggestions: {str(e)}")

def remove_all_bloatware():
    """Remove all bloatware and unnecessary features."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored("🗑️  COMPREHENSIVE BLOATWARE REMOVAL", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 70, Colors.MAGENTA)
    
    print_warning("This will remove Windows 11 bloatware and unnecessary features!")
    print_warning("Some apps may be useful to some users. Review the list carefully.")
    print_info("This includes: Xbox services, Cortana, Widgets, Edge integration, etc.")
    
    confirm = input(f"\n{Colors.YELLOW}Do you want to continue? (y/N): {Colors.END}").lower().strip()
    if confirm != 'y':
        print_colored("Operation cancelled by user.", Colors.CYAN)
        return
    
    print_info("Starting comprehensive bloatware removal...")
    
    remove_windows_apps()
    remove_xbox_services()
    disable_cortana()
    disable_windows_widgets()
    disable_edge_integration()
    remove_start_menu_suggestions()
    
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success("Bloatware removal completed!")
    print_colored("=" * 60, Colors.GREEN)
    print_warning("A system restart is recommended for all changes to take effect.")
    print_info("Your system is now cleaner and more focused.")

def show_bloatware_menu():
    """Display bloatware management menu."""
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored("🗑️  BLOATWARE REMOVAL MANAGEMENT", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored("\n📋 Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored("\n1. 🗑️  Remove All Bloatware", Colors.RED)
    print_colored("2. 📱 Remove Windows Apps Only", Colors.YELLOW)
    print_colored("3. 🎮 Disable Xbox Services Only", Colors.YELLOW)
    print_colored("4. 🔍 Disable Cortana Only", Colors.YELLOW)
    print_colored("5. 📰 Disable Widgets Only", Colors.YELLOW)
    print_colored("6. 🌐 Disable Edge Integration Only", Colors.YELLOW)
    print_colored("7. 📊 Check Installed Apps", Colors.BLUE)
    print_colored("8. 🔙 Return to Main Menu", Colors.CYAN)

def check_installed_apps():
    """Check currently installed Windows apps."""
    print_header("Checking Installed Windows Apps")
    
    try:
        command = "Get-AppxPackage | Select-Object Name, Version | Sort-Object Name"
        result = subprocess.run(
            ["powershell", "-Command", command], 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print_info("Currently installed Windows apps:")
            print_colored(result.stdout, Colors.WHITE)
        else:
            print_error("Failed to retrieve installed apps")
    except Exception as e:
        print_error(f"Error checking installed apps: {str(e)}")

def main():
    """Main bloatware management function."""
    while True:
        show_bloatware_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-8): {Colors.END}").strip()
            
            if choice == '1':
                remove_all_bloatware()
            elif choice == '2':
                remove_windows_apps()
            elif choice == '3':
                remove_xbox_services()
            elif choice == '4':
                disable_cortana()
            elif choice == '5':
                disable_windows_widgets()
            elif choice == '6':
                disable_edge_integration()
            elif choice == '7':
                check_installed_apps()
            elif choice == '8':
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-8.")
            
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nReturning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
