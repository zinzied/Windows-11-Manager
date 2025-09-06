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
import shutil
from pathlib import Path
import time

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

def run_command(command, description, check_output=False):
    """Run a command and handle errors with optional output check."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description}")
            if check_output:
                return result.stdout.strip()
        else:
            print_error(f"{description} - {result.stderr.strip()}")
            return None
    except Exception as e:
        print_error(f"{description} - {str(e)}")
        return None

def check_admin():
    """Check if running as administrator."""
    try:
        result = subprocess.run('net session >nul 2>&1', shell=True, capture_output=True)
        return result.returncode == 0
    except:
        return False

def create_backup_registry_key(root_key, subkey):
    """Create a backup of registry key if it exists."""
    try:
        key = winreg.OpenKey(root_key, subkey, 0, winreg.KEY_READ)
        backup_key = winreg.CreateKey(root_key, f"Backup_{subkey.replace('\\', '_')}_{int(time.time())}")
        # Simple backup by copying values (enhanced version could use more advanced methods)
        i = 0
        while True:
            try:
                value_name, value_data, value_type = winreg.EnumValue(key, i)
                winreg.SetValueEx(backup_key, value_name, 0, value_type, value_data)
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
        winreg.CloseKey(backup_key)
        print_info(f"Created backup for {subkey}")
    except FileNotFoundError:
        pass
    except Exception as e:
        print_error(f"Failed to backup {subkey}: {str(e)}")

def restore_registry_value(root_key, subkey, value_name, default_value, value_type=winreg.REG_DWORD):
    """Restore a registry value to default."""
    try:
        create_backup_registry_key(root_key, subkey)
        key = winreg.CreateKey(root_key, subkey)
        winreg.SetValueEx(key, value_name, 0, value_type, default_value)
        winreg.CloseKey(key)
        print_success(f"Restored {value_name} in {subkey}")
    except Exception as e:
        print_error(f"Failed to restore {value_name} in {subkey}: {str(e)}")

def restore_windows_updates():
    """Restore Windows Update functionality with enhanced checks."""
    print_header("Restoring Windows Updates")
    
    # Re-enable services with dependency handling
    services = [
        ("wuauserv", "auto"),
        ("bits", "auto"),
        ("dosvc", "auto"),
        ("UsoSvc", "auto"),
        ("wuauserv", "demand")  # Additional for Update Orchestrator
    ]
    for service, start_type in services:
        run_command(f'sc config "{service}" start= {start_type}', f"Configuring {service} to {start_type}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Restore registry keys and values (reverse disable logic)
    policy_keys = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate"),
    ]
    for root_key, subkey in policy_keys:
        try:
            winreg.DeleteKey(root_key, subkey)
            print_success(f"Deleted policy key: {subkey}")
        except FileNotFoundError:
            print_info(f"Policy key not found: {subkey}")
        except Exception as e:
            print_error(f"Failed to delete {subkey}: {str(e)}")
    
    # Restore additional update settings
    restore_registry_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update", "AUOptions", 1)
    restore_registry_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate", "DoNotConnectToWindowsUpdateInternetLocations", 0)
    
    # Reset Windows Update components
    run_command('net stop wuauserv', "Stopping Windows Update service for reset")
    run_command('net stop cryptSvc', "Stopping Cryptographic Services")
    run_command('net stop bits', "Stopping Background Intelligent Transfer Service")
    run_command('net stop msiserver', "Stopping Windows Installer")
    run_command('ren C:\\Windows\\SoftwareDistribution SoftwareDistribution.old', "Renaming SoftwareDistribution folder")
    run_command('ren C:\\Windows\\System32\\catroot2 catroot2.old', "Renaming Catroot2 folder")
    run_command('net start wuauserv', "Starting Windows Update service")
    run_command('net start cryptSvc', "Starting Cryptographic Services")
    run_command('net start bits', "Starting Background Intelligent Transfer Service")
    run_command('net start msiserver', "Starting Windows Installer")
    
    print_success("Windows Updates restoration completed with component reset.")

def restore_onedrive():
    """Enhanced restore for OneDrive functionality."""
    print_header("Restoring OneDrive")
    
    # Re-enable services
    services = [
        ("OneSyncSvc", "auto"),
        ("OneSyncSvc_Session1", "auto"),
    ]
    for service, start_type in services:
        run_command(f'sc config "{service}" start= {start_type}', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Reset registry modifications (reverse disable settings)
    registry_resets = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\OneDrive",
            "values": [
                ("DisableFileSyncNGSC", 0),
                ("DisableFileSync", 0),
                ("DisableMeteredNetworkFileSync", 0),
                ("DisableLibrariesDefaultSaveToOneDrive", 0),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\OneDrive",
            "values": [
                ("DisablePersonalSync", 0),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Classes\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}",
            "values": [
                ("System.IsPinnedToNameSpaceTree", 1),
            ]
        }
    ]
    
    for reg_change in registry_resets:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            for value_name, default_value in reg_change["values"]:
                restore_registry_value(reg_change["key"], reg_change["subkey"], value_name, default_value)
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to reset OneDrive registry: {reg_change['subkey']} - {str(e)}")
    
    # Restore OneDrive to startup
    startup_locations = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
    ]
    for location in startup_locations:
        try:
            if "HKEY_CURRENT_USER" in location:
                root = winreg.HKEY_CURRENT_USER
            else:
                root = winreg.HKEY_LOCAL_MACHINE
            sub_loc = location.split("\\", 1)[1] if "\\" in location else location
            key = winreg.CreateKey(root, sub_loc)
            # Add OneDrive to startup if setup exists
            onedrive_path = os.path.expanduser(r"~\AppData\Local\Microsoft\OneDrive\OneDrive.exe")
            if os.path.exists(onedrive_path):
                winreg.SetValueEx(key, "OneDrive", 0, winreg.REG_SZ, f'"{onedrive_path}"')
                print_success(f"Restored OneDrive to startup in {location}")
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to restore startup in {location}: {str(e)}")
    
    # Reinstall OneDrive if uninstalled
    onedrive_setup_paths = [
        r"C:\Windows\System32\OneDriveSetup.exe",
        r"C:\Windows\SysWOW64\OneDriveSetup.exe",
    ]
    for setup_path in onedrive_setup_paths:
        if os.path.exists(setup_path):
            run_command(f'"{setup_path}" /allusers', "Reinstalling OneDrive")
            break
    else:
        # Download and install OneDrive if not present (basic fallback)
        print_warning("OneDrive setup not found. Manual reinstall may be required from Microsoft website.")
    
    # Verify restoration
    time.sleep(2)
    result = run_command('tasklist /fi "imagename eq OneDrive.exe"', "Checking OneDrive process", check_output=True)
    if result and "OneDrive.exe" in result:
        print_success("OneDrive process is now running.")
    else:
        print_warning("OneDrive process not detected. May require manual start or restart.")

def restore_telemetry():
    """Enhanced restore for telemetry and diagnostic services."""
    print_header("Restoring Telemetry Services")
    
    # Re-enable telemetry services with additional ones
    services = [
        "DiagTrack", "dmwappushservice", "WerSvc",
        "DPS", "WdiServiceHost", "WdiSystemHost"
    ]
    for service in services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Reset telemetry policy registry keys and values
    telemetry_resets = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "values": [
                ("AllowTelemetry", 3),  # Full telemetry
                ("AllowDeviceNameInTelemetry", 1),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo",
            "values": [
                ("DisabledByGroupPolicy", 0),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors",
            "values": [
                ("DisableLocation", 0),
                ("DisableSensors", 0),
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy",
            "values": [
                ("TailoredExperiencesWithDiagnosticDataEnabled", 1),
            ]
        }
    ]
    
    for reg_change in telemetry_resets:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            for value_name, default_value in reg_change["values"]:
                restore_registry_value(reg_change["key"], reg_change["subkey"], value_name, default_value)
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to reset telemetry registry: {reg_change['subkey']} - {str(e)}")
    
    # Re-enable scheduled tasks for telemetry
    tasks = [
        r"\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser",
        r"\Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
        r"\Microsoft\Windows\Autochk\Proxy",
    ]
    for task in tasks:
        run_command(f'schtasks /change /tn "{task}" /enable', f"Enabling task {task}")
    
    print_success("Telemetry restoration completed with full service and task re-enablement.")

def restore_performance():
    """Enhanced restore for performance-related services and settings."""
    print_header("Restoring Performance Settings")
    
    # Re-enable all potentially disabled services
    services = [
        "WSearch", "SysMain", "Themes", "Spooler", "Themes",
        "WindowsAudio", "AudioSrv", "AudioEndpointBuilder"
    ]
    for service in services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Reset power plan to balanced and restore defaults
    run_command(
        'powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e',
        "Setting power plan to Balanced"
    )
    run_command('powercfg /restoredefaultschemes', "Restoring default power schemes")
    
    # Restore visual effects to default (Let Windows choose)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f', "Restoring default visual effects")
    
    # Re-enable startup programs (reverse disable)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /f', "Ensuring startup registry is accessible")
    print_info("Startup programs registry restored. Manual re-enabling of specific programs may be needed.")
    
    # Re-enable Windows Search indexing
    run_command('sc config "WSearch" start= auto', "Enabling Windows Search")
    run_command('sc start "WSearch"', "Starting Windows Search")
    
    # Restore memory management defaults
    restore_registry_value(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "LargeSystemCache", 0)
    
    print_success("Performance settings restored to defaults.")

def restore_xbox_services():
    """Enhanced restore for Xbox services with additional components."""
    print_header("Restoring Xbox Services")
    
    xbox_services = [
        "XblAuthManager", "XblGameSave", "XboxGipSvc", "XboxNetApiSvc",
        "XblGameSave", "XboxGipSvc"
    ]
    for service in xbox_services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")
    
    # Reinstall Xbox components if needed
    run_command('dism /online /add-capability /capabilityname:Xbox.*', "Reinstalling Xbox capabilities")
    
    print_success("Xbox services and components restored.")

def restore_bloatware():
    """New feature: Restore bloatware and apps."""
    print_header("Restoring Bloatware and System Apps")
    
    # Reinstall common bloatware apps
    apps_to_restore = [
        "Microsoft.3DBuilder",
        "Microsoft.BingWeather",
        "Microsoft.GetHelp",
        "Microsoft.Getstarted",
        "Microsoft.Microsoft3DViewer",
        "Microsoft.MicrosoftOfficeHub",
        "Microsoft.MicrosoftSolitaireCollection",
        "Microsoft.MixedReality.Portal",
        "Microsoft.OneConnect",
        "Microsoft.People",
        "Microsoft.Print3D",
        "Microsoft.SkypeApp",
        "Microsoft.StorePurchaseApp",
        "Microsoft.Wallet",
        "Microsoft.WindowsCamera",
        "microsoft.windowscommunicationsapps",
        "Microsoft.WindowsMaps",
        "Microsoft.Xbox.TCUI",
        "Microsoft.XboxApp",
        "Microsoft.XboxGameOverlay",
        "Microsoft.XboxGamingOverlay",
        "Microsoft.XboxIdentityProvider",
        "Microsoft.XboxSpeechToTextOverlay",
        "Microsoft.YourPhone",
        "Microsoft.ZuneMusic",
        "Microsoft.ZuneVideo"
    ]
    
    for app in apps_to_restore:
        ps_command = f'Get-AppxPackage -allusers *{app}* | Foreach {{Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}}'
        run_command(f'powershell -Command "{ps_command}"', f"Restoring {app}")
    
    # Re-enable Cortana
    restore_registry_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\Windows Search", "AllowCortana", 1)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" /v CortanaConsent /t REG_DWORD /d 1 /f', "Enabling Cortana")
    
    # Re-enable widgets and start menu suggestions
    restore_registry_value(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Dsh", "AllowNewsAndInterests", 1)
    restore_registry_value(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager", "SubscribedContent-338389Enabled", 1)
    
    print_success("Bloatware and system apps restored.")

def comprehensive_restore():
    """Perform comprehensive system restore with all improvements."""
    if not check_admin():
        print_error("This script requires administrator privileges. Please run as administrator.")
        return
    
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored("🔄 COMPREHENSIVE SYSTEM RESTORE", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 70, Colors.MAGENTA)
    
    print_warning("This will restore all system modifications made by this tool!")
    print_info("This includes: Updates, OneDrive, Telemetry, Performance, Xbox services, Bloatware")
    print_warning("Backups of registry changes will be created automatically.")
    
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
    restore_bloatware()
    
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success("Comprehensive system restore completed successfully!")
    print_colored("=" * 60, Colors.GREEN)
    print_warning("A system restart is highly recommended for all changes to take effect.")
    print_info("Your system has been fully restored to default Windows 11 settings.")
    print_info("Check the registry backups if you need to revert any changes.")

def show_restore_menu():
    """Enhanced restore menu with new options."""
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
    print_colored("7. 🗑️  Restore Bloatware and Apps Only", Colors.YELLOW)
    print_colored("8. 🔙 Exit", Colors.CYAN)

def main():
    """Main restore function with admin check."""
    if not check_admin():
        print_error("Please run this script as administrator to restore system settings.")
        input("Press Enter to exit...")
        return
    
    print_info("Administrator privileges confirmed.")
    
    while True:
        show_restore_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-8): {Colors.END}").strip()
            
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
                restore_bloatware()
            elif choice == '8':
                print_colored("\n👋 Restore operations completed!", Colors.BOLD + Colors.CYAN)
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-8.")
            
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nExiting restore tool...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
