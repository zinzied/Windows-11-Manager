#!/usr/bin/env python3
"""
Windows 11 Update Restore Script
This script re-enables Windows 11 automatic updates.
Run as Administrator for full functionality.
"""

import subprocess
import os
import winreg
from pathlib import Path

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
    print(f"Executing: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✓ Success: {description}")
        if result.stdout:
            print(f"  Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {description}")
        print(f"  Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def restore_services():
    """Re-enable Windows Update services."""
    print("\n=== Restoring Windows Update Services ===")

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
    print("\n=== Restoring Registry Settings ===")

    keys_to_delete = [
        r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
        r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",
    ]

    for subkey in keys_to_delete:
        try:
            winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, subkey)
            print(f"✓ Deleted registry key: {subkey}")
        except FileNotFoundError:
            print(f"✓ Registry key not found (already clean): {subkey}")
        except Exception as e:
            print(f"✗ Failed to delete registry key {subkey}: {str(e)}")

def restore_tasks():
    """Re-enable Windows Update scheduled tasks."""
    print("\n=== Restoring Scheduled Tasks ===")

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
    print("\n=== Restoring Hosts File ===")

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
                    print(f"✓ Unblocked: {url}")
                    break
            if should_keep:
                new_lines.append(line)

        # Write back to hosts file if modified
        if modified:
            with open(hosts_file, 'w') as f:
                f.writelines(new_lines)
            print("✓ Hosts file restored successfully")
        else:
            print("✓ No blocked URLs found in hosts file")

    except Exception as e:
        print(f"✗ Failed to restore hosts file: {str(e)}")

def main():
    """Main function to restore Windows Updates."""
    print("Windows 11 Update Restore Tool")
    print("=" * 40)

    if not is_admin():
        print("⚠️  WARNING: This script should be run as Administrator for full functionality.")
        print("Some operations may fail without elevated privileges.")
        input("Press Enter to continue anyway, or Ctrl+C to exit...")

    print("\nStarting Windows Update restoration process...")

    # Execute all restoration methods
    restore_services()
    restore_registry()
    restore_tasks()
    restore_hosts_file()

    print("\n" + "=" * 40)
    print("✓ Windows Update restoration process completed!")
    print("\nNOTE: A system restart is recommended for all changes to take effect.")
    print("Windows Updates should now work normally.")

    restart = input("\nWould you like to restart now? (y/N): ").lower().strip()
    if restart == 'y':
        print("Restarting system in 10 seconds...")
        subprocess.run("shutdown /r /t 10", shell=True)

if __name__ == "__main__":
    main()