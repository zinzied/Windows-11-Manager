#!/usr/bin/env python3
"""
Windows 11 Update Restore Script
This script re-enables Windows 11 automatic updates.
Run as Administrator for full functionality.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
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

def restore_services():
    """Re-enable Windows Update services."""
    print_header("Restoring Windows Update Services")

    services = [
        "wuauserv",  # Windows Update Service
        "bits",      # Background Intelligent Transfer Service
        "dosvc",     # Delivery Optimization Service
        "UsoSvc",    # Update Orchestrator Service
    ]

    for service in services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}")

def restore_registry():
    """Remove registry modifications that disable updates."""
    print_header("Restoring Registry Settings")

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

def restore_tasks():
    """Re-enable Windows Update scheduled tasks."""
    print_header("Restoring Scheduled Tasks")

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
        run_command(f'schtasks /change /tn "{task}" /enable', f"Enabling task: {task}")

def restore_hosts_file():
    """Remove Windows Update URL blocks from hosts file."""
    print_header("Restoring Hosts File")

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
            lines = f.readlines()

        # Remove blocking entries
        modified = False
        new_lines = []
        for line in lines:
            should_keep = True
            for url in update_urls:
                if f"127.0.0.1 {url}" in line:
                    should_keep = False
                    modified = True
                    print_success(f"Unblocked: {url}")
                    break
            if should_keep:
                new_lines.append(line)

        # Write back to hosts file if modified
        if modified:
            with open(hosts_file, 'w') as f:
                f.writelines(new_lines)
            print_success("Hosts file restored successfully")
        else:
            print_success("No blocked URLs found in hosts file")

    except Exception as e:
        print_error(f"Failed to restore hosts file: {str(e)}")

def show_restore_menu():
    """Display the restore menu."""
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_colored("🔄 WINDOWS 11 UPDATE RESTORE TOOL", Colors.BOLD + Colors.GREEN)
    print_colored("    Created by Zied Boughdir - 2025", Colors.CYAN)
    print_colored("    GitHub: https://github.com/zinzied", Colors.BLUE)
    print_colored("=" * 60, Colors.GREEN)
    print_colored("\n📋 Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored("\n1. 🔄 Restore All Windows Updates (Complete Restoration)", Colors.GREEN)
    print_colored("2. ⚙️  Restore Update Services Only", Colors.YELLOW)
    print_colored("3. 📝 Restore Registry Settings Only", Colors.YELLOW)
    print_colored("4. 📅 Restore Scheduled Tasks Only", Colors.YELLOW)
    print_colored("5. 🌐 Restore Hosts File Only", Colors.YELLOW)
    print_colored("6. ❌ Exit", Colors.RED)
    print_colored("\n" + "=" * 60, Colors.GREEN)

def restore_all_updates():
    """Execute all update restoration methods."""
    print_header("🔄 RESTORING ALL WINDOWS UPDATES")

    if not is_admin():
        print_warning("This script should be run as Administrator for full functionality.")
        print_warning("Some operations may fail without elevated privileges.")
        choice = input(f"\n{Colors.YELLOW}Continue anyway? (y/N): {Colors.END}").lower().strip()
        if choice != 'y':
            return

    print_info("Starting comprehensive Windows Update restoration process...")

    # Execute all restoration methods
    restore_services()
    restore_registry()
    restore_tasks()
    restore_hosts_file()

    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success("Windows Update restoration process completed!")
    print_colored("=" * 60, Colors.GREEN)
    print_warning("A system restart is recommended for all changes to take effect.")
    print_success("Windows Updates should now work normally.")

    restart = input(f"\n{Colors.CYAN}Would you like to restart now? (y/N): {Colors.END}").lower().strip()
    if restart == 'y':
        print_colored("Restarting system in 10 seconds...", Colors.RED)
        subprocess.run("shutdown /r /t 10", shell=True)

def main():
    """Main function with menu system."""
    while True:
        show_restore_menu()

        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-6): {Colors.END}").strip()

            if choice == '1':
                restore_all_updates()
            elif choice == '2':
                restore_services()
            elif choice == '3':
                restore_registry()
            elif choice == '4':
                restore_tasks()
            elif choice == '5':
                restore_hosts_file()
            elif choice == '6':
                print_colored("\n👋 Goodbye! Your updates are restored!", Colors.BOLD + Colors.GREEN)
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-6.")

            if choice in ['1', '2', '3', '4', '5']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

        except KeyboardInterrupt:
            print_colored("\n\n👋 Goodbye! Your updates are restored!", Colors.BOLD + Colors.GREEN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()