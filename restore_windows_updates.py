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
import sys
import winreg
from pathlib import Path

# Ensure we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info, clear_screen
except ImportError:
    # Fallback if run directly from root without modules package context
    try:
        from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info, clear_screen
    except ImportError:
        # Define fallback if module is missing
        class Colors:
            RED = '\033[91m'
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            BLUE = '\033[94m'
            MAGENTA = '\033[95m'
            CYAN = '\033[96m'
            WHITE = '\033[97m'
            BOLD = '\033[1m'
            END = '\033[0m'
        
        def print_colored(text, color=Colors.WHITE): print(f"{color}{text}{Colors.END}")
        def print_header(text): print(f"\n=== {text} ===")
        def print_success(text): print(f"OK: {text}")
        def print_error(text): print(f"ERROR: {text}")
        def print_warning(text): print(f"WARNING: {text}")
        def print_info(text): print(f"INFO: {text}")
        symbols = type('obj', (object,), {'CROSS': 'x', 'CHECK': 'v', 'WARNING': '!', 'INFO': 'i', 'BLOCK': '#', 'RECYCLE': '@'})

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return os.getuid() == 0
    except AttributeError:
        try:
            subprocess.run(['net', 'session'], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

def run_command(command, description, ignore_errors=False):
    """Run a command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print_success(f"{description}")
        return True
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.strip() if e.stderr else str(e)
        if "does not exist" in err_msg:
             print_info(f"{description} - Task/Service not found (already clean?)")
             return True
             
        if not ignore_errors:
            print_error(f"{description}")
            print_colored(f"  - Error: {err_msg}", Colors.RED)
        return False

def restore_services():
    """Re-enable Windows Update services."""
    print_colored(f"\n{symbols.RECYCLE} Restoring Windows Update Services", Colors.BOLD + Colors.CYAN)

    services = [
        "wuauserv",  # Windows Update Service
        "bits",      # Background Intelligent Transfer Service
        "dosvc",     # Delivery Optimization Service
        "UsoSvc",    # Update Orchestrator Service
    ]

    for service in services:
        run_command(f'sc config "{service}" start= auto', f"Enabling {service}")
        run_command(f'sc start "{service}"', f"Starting {service}", ignore_errors=True)

def restore_registry():
    """Remove registry modifications that disable updates."""
    print_colored(f"\n{symbols.TOOLS} Restoring Registry Settings", Colors.BOLD + Colors.CYAN)

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
            # Often fails if subkeys exist, we might need recursive delete or just ignore
            print_warning(f"Could not delete key {subkey}: {str(e)}")

def restore_tasks():
    """Re-enable Windows Update scheduled tasks."""
    print_colored(f"\n{symbols.GEAR} Restoring Scheduled Tasks", Colors.BOLD + Colors.CYAN)

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
        run_command(f'schtasks /change /tn "{task}" /enable', f"Enabling task: {task}", ignore_errors=True)

def restore_hosts_file():
    """Remove Windows Update URL blocks from hosts file."""
    print_colored(f"\n{symbols.GLOBE} Restoring Hosts File", Colors.BOLD + Colors.CYAN)

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
    clear_screen()
    print_header("WINDOWS 11 UPDATE RESTORE TOOL")
    print_colored(f"\n{symbols.TARGET} Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. {symbols.RECYCLE} Restore All Windows Updates (Complete Restoration)", Colors.GREEN)
    print_colored(f"2. {symbols.GEAR} Restore Update Services Only", Colors.YELLOW)
    print_colored(f"3. {symbols.TOOLS} Restore Registry Settings Only", Colors.YELLOW)
    print_colored(f"4. {symbols.GEAR} Restore Scheduled Tasks Only", Colors.YELLOW)
    print_colored(f"5. {symbols.GLOBE} Restore Hosts File Only", Colors.YELLOW)
    print_colored(f"6. {symbols.WAVE} Exit", Colors.RED)

def restore_all_updates():
    """Execute all update restoration methods."""
    print_colored("\n" + "=" * 70, Colors.GREEN)
    print_colored(f"{symbols.RECYCLE} RESTORING ALL WINDOWS UPDATES", Colors.BOLD + Colors.GREEN)
    print_colored("=" * 70, Colors.GREEN)

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
                print_colored(f"\n{symbols.WAVE} Goodbye! Your updates are restored!", Colors.BOLD + Colors.GREEN)
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-6.")

            if choice in ['1', '2', '3', '4', '5']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

        except KeyboardInterrupt:
            print_colored(f"\n\n{symbols.WAVE} Goodbye! Your updates are restored!", Colors.BOLD + Colors.GREEN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
