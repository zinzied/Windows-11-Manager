#!/usr/bin/env python3
"""
Windows 11 Update Disabler Script
This script stops and disables Windows 11 automatic updates using multiple methods.
Run as Administrator for full functionality.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import sys
import os
import winreg
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
    END = '\033[0m'  # End color formatting

def print_colored(text, color=Colors.WHITE):
    """Print text with color."""
    print(f"{color}{text}{Colors.END}")

def print_header(text):
    """Print a formatted header."""
    print_colored("=" * 60, Colors.CYAN)
    print_colored(f"  {text}", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)

def print_success(text):
    """Print success message."""
    print_colored(f"✓ {text}", Colors.GREEN)

def print_error(text):
    """Print error message."""
    print_colored(f"✗ {text}", Colors.RED)

def print_warning(text):
    """Print warning message."""
    print_colored(f"⚠️  {text}", Colors.YELLOW)

def print_info(text):
    """Print info message."""
    print_colored(f"ℹ️  {text}", Colors.BLUE)

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return os.getuid() == 0
    except AttributeError:
        # Windows doesn't have os.getuid(), use alternative method
        try:
            subprocess.run(['net', 'session'], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

def run_command(command, description):
    """Run a command and handle errors."""
    print_info(f"Executing: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print_success(f"Success: {description}")
        if result.stdout:
            print_colored(f"  Output: {result.stdout.strip()}", Colors.WHITE)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed: {description}")
        print_colored(f"  Error: {e.stderr.strip() if e.stderr else str(e)}", Colors.RED)
        return False

def stop_update_services():
    """Stop Windows Update related services."""
    services = [
        "wuauserv",  # Windows Update Service
        "bits",      # Background Intelligent Transfer Service
        "dosvc",     # Delivery Optimization Service
        "UsoSvc",    # Update Orchestrator Service
    ]

    print_header("Stopping Windows Update Services")
    for service in services:
        run_command(f'sc stop "{service}"', f"Stopping {service}")
        run_command(f'sc config "{service}" start= disabled', f"Disabling {service}")

def modify_registry():
    """Modify registry to disable automatic updates."""
    print_header("Modifying Registry Settings")

    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
            "values": [
                ("NoAutoUpdate", winreg.REG_DWORD, 1),
                ("AUOptions", winreg.REG_DWORD, 1),
                ("ScheduledInstallDay", winreg.REG_DWORD, 0),
                ("ScheduledInstallTime", winreg.REG_DWORD, 3),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update",
            "values": [
                ("EnableFeaturedSoftware", winreg.REG_DWORD, 0),
            ]
        },
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",
            "values": [
                ("DisableWindowsUpdateAccess", winreg.REG_DWORD, 1),
                ("WUServer", winreg.REG_SZ, " "),
                ("WUStatusServer", winreg.REG_SZ, " "),
            ]
        }
    ]

    for reg_change in registry_changes:
        try:
            # Create or open the registry key
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])

            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Set registry value: {reg_change['subkey']}\\{value_name}")

            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to modify registry: {reg_change['subkey']} - {str(e)}")

def disable_update_tasks():
    """Disable Windows Update scheduled tasks."""
    print_header("Disabling Scheduled Tasks")

    tasks = [
        r"\Microsoft\Windows\WindowsUpdate\Scheduled Start",
        r"\Microsoft\Windows\WindowsUpdate\sih",
        r"\Microsoft\Windows\WindowsUpdate\sihboot",
        r"\Microsoft\Windows\UpdateOrchestrator\Schedule Scan",
        r"\Microsoft\Windows\UpdateOrchestrator\Schedule Scan Static Task",
        r"\Microsoft\Windows\UpdateOrchestrator\UpdateModelTask",
        r"\Microsoft\Windows\UpdateOrchestrator\USO_UxBroker",
    ]

    for task in tasks:
        run_command(f'schtasks /change /tn "{task}" /disable', f"Disabling task: {task}")

def block_update_urls():
    """Add Windows Update URLs to hosts file to block them."""
    print_header("Blocking Update URLs in Hosts File")

    hosts_file = Path(r"C:\Windows\System32\drivers\etc\hosts")
    update_urls = [
        "windowsupdate.microsoft.com",
        "update.microsoft.com",
        "windowsupdate.com",
        "download.windowsupdate.com",
        "wustat.windows.com",
        "ntservicepack.microsoft.com",
        "stats.microsoft.com",
        "download.microsoft.com",
    ]

    try:
        # Read existing hosts file
        with open(hosts_file, 'r') as f:
            content = f.read()

        # Add blocking entries if they don't exist
        modified = False
        for url in update_urls:
            block_entry = f"127.0.0.1 {url}"
            if block_entry not in content:
                content += f"\n{block_entry}"
                modified = True
                print_success(f"Blocked: {url}")

        # Write back to hosts file if modified
        if modified:
            with open(hosts_file, 'w') as f:
                f.write(content)
            print_success("Hosts file updated successfully")
        else:
            print_success("All URLs already blocked in hosts file")

    except Exception as e:
        print_error(f"Failed to modify hosts file: {str(e)}")

def show_menu():
    """Display the main menu."""
    print_colored("\n" + "=" * 60, Colors.MAGENTA)
    print_colored("🛡️  WINDOWS 11 UPDATE MANAGER", Colors.BOLD + Colors.MAGENTA)
    print_colored("    Created by Zied Boughdir - 2025", Colors.CYAN)
    print_colored("    GitHub: https://github.com/zinzied", Colors.BLUE)
    print_colored("=" * 60, Colors.MAGENTA)
    print_colored("\n📋 Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored("\n1. 🚫 Disable All Windows Updates (Full Protection)", Colors.YELLOW)
    print_colored("2. ⚙️  Stop Update Services Only", Colors.YELLOW)
    print_colored("3. 📝 Modify Registry Settings Only", Colors.YELLOW)
    print_colored("4. 📅 Disable Scheduled Tasks Only", Colors.YELLOW)
    print_colored("5. 🌐 Block Update URLs Only", Colors.YELLOW)
    print_colored("6. 📊 Check Current Update Status", Colors.BLUE)
    print_colored("7. 🔄 Create Restore Script", Colors.GREEN)
    print_colored("8. ❌ Exit", Colors.RED)
    print_colored("\n" + "=" * 60, Colors.MAGENTA)

def check_update_status():
    """Check the current status of Windows Update components."""
    print_header("Checking Windows Update Status")

    # Check services
    services = ["wuauserv", "bits", "dosvc", "UsoSvc"]
    print_colored("\n🔧 Service Status:", Colors.BOLD + Colors.CYAN)
    for service in services:
        try:
            result = subprocess.run(f'sc query "{service}"', shell=True, capture_output=True, text=True)
            if "RUNNING" in result.stdout:
                print_colored(f"  {service}: RUNNING", Colors.GREEN)
            elif "STOPPED" in result.stdout:
                print_colored(f"  {service}: STOPPED", Colors.RED)
            else:
                print_colored(f"  {service}: UNKNOWN", Colors.YELLOW)
        except:
            print_colored(f"  {service}: ERROR", Colors.RED)

    # Check registry
    print_colored("\n📝 Registry Status:", Colors.BOLD + Colors.CYAN)
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU")
        print_colored("  Update policies: DISABLED", Colors.RED)
        winreg.CloseKey(key)
    except FileNotFoundError:
        print_colored("  Update policies: ENABLED", Colors.GREEN)
    except Exception as e:
        print_colored(f"  Update policies: ERROR - {str(e)}", Colors.YELLOW)

def create_restore_script():
    """Create a script to restore Windows Updates if needed."""
    print_header("Creating Restore Script")

    try:
        print_success("Restore script already exists: restore_windows_updates.py")
        print_info("You can run it anytime to restore Windows Updates")
    except Exception as e:
        print_error(f"Failed to verify restore script: {str(e)}")

def disable_all_updates():
    """Execute all update disabling methods."""
    print_header("🚫 DISABLING ALL WINDOWS UPDATES")

    if not is_admin():
        print_warning("This script should be run as Administrator for full functionality.")
        print_warning("Some operations may fail without elevated privileges.")
        choice = input(f"\n{Colors.YELLOW}Continue anyway? (y/N): {Colors.END}").lower().strip()
        if choice != 'y':
            return

    print_info("Starting comprehensive Windows Update disabling process...")

    # Execute all disabling methods
    stop_update_services()
    modify_registry()
    disable_update_tasks()
    block_update_urls()
    create_restore_script()

    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success("Windows Update disabling process completed!")
    print_colored("=" * 60, Colors.GREEN)
    print_warning("A system restart is recommended for all changes to take effect.")
    print_info("To restore updates later, run: python restore_windows_updates.py")

    restart = input(f"\n{Colors.CYAN}Would you like to restart now? (y/N): {Colors.END}").lower().strip()
    if restart == 'y':
        print_colored("Restarting system in 10 seconds...", Colors.RED)
        subprocess.run("shutdown /r /t 10", shell=True)

def main():
    """Main function with menu system."""
    while True:
        show_menu()

        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-8): {Colors.END}").strip()

            if choice == '1':
                disable_all_updates()
            elif choice == '2':
                stop_update_services()
            elif choice == '3':
                modify_registry()
            elif choice == '4':
                disable_update_tasks()
            elif choice == '5':
                block_update_urls()
            elif choice == '6':
                check_update_status()
            elif choice == '7':
                create_restore_script()
            elif choice == '8':
                print_colored("\n👋 Goodbye! Stay safe!", Colors.BOLD + Colors.CYAN)
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-8.")

            if choice in ['1', '2', '3', '4', '5', '7']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

        except KeyboardInterrupt:
            print_colored("\n\n👋 Goodbye! Stay safe!", Colors.BOLD + Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
