#!/usr/bin/env python3
"""
Windows 11 Update Disabler Script
This script stops and disables Windows 11 automatic updates using multiple methods.
Run as Administrator for full functionality.
"""

import subprocess
import sys
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

def stop_update_services():
    """Stop Windows Update related services."""
    services = [
        "wuauserv",  # Windows Update Service
        "bits",      # Background Intelligent Transfer Service
        "dosvc",     # Delivery Optimization Service
        "UsoSvc",    # Update Orchestrator Service
    ]
    
    print("\n=== Stopping Windows Update Services ===")
    for service in services:
        run_command(f'sc stop "{service}"', f"Stopping {service}")
        run_command(f'sc config "{service}" start= disabled', f"Disabling {service}")

def modify_registry():
    """Modify registry to disable automatic updates."""
    print("\n=== Modifying Registry Settings ===")
    
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
                print(f"✓ Set registry value: {reg_change['subkey']}\\{value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print(f"✗ Failed to modify registry: {reg_change['subkey']} - {str(e)}")

def disable_update_tasks():
    """Disable Windows Update scheduled tasks."""
    print("\n=== Disabling Scheduled Tasks ===")
    
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
    print("\n=== Blocking Update URLs in Hosts File ===")
    
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
                print(f"✓ Blocked: {url}")
        
        # Write back to hosts file if modified
        if modified:
            with open(hosts_file, 'w') as f:
                f.write(content)
            print("✓ Hosts file updated successfully")
        else:
            print("✓ All URLs already blocked in hosts file")
            
    except Exception as e:
        print(f"✗ Failed to modify hosts file: {str(e)}")

def create_restore_script():
    """Create a script to restore Windows Updates if needed."""
    print("\n=== Creating Restore Script ===")
    
    restore_script = '''#!/usr/bin/env python3
"""
Windows 11 Update Restore Script
This script re-enables Windows 11 automatic updates.
Run as Administrator.
"""

import subprocess
import winreg

def restore_services():
    """Re-enable Windows Update services."""
    services = ["wuauserv", "bits", "dosvc", "UsoSvc"]
    for service in services:
        subprocess.run(f'sc config "{service}" start= auto', shell=True)
        subprocess.run(f'sc start "{service}"', shell=True)
    print("✓ Services restored")

def restore_registry():
    """Remove registry modifications."""
    keys_to_delete = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate"),
    ]
    
    for hkey, subkey in keys_to_delete:
        try:
            winreg.DeleteKey(hkey, subkey)
            print(f"✓ Deleted registry key: {subkey}")
        except:
            pass

def restore_tasks():
    """Re-enable scheduled tasks."""
    tasks = [
        r"\\Microsoft\\Windows\\WindowsUpdate\\Scheduled Start",
        r"\\Microsoft\\Windows\\UpdateOrchestrator\\Schedule Scan",
    ]
    for task in tasks:
        subprocess.run(f'schtasks /change /tn "{task}" /enable', shell=True)
    print("✓ Tasks restored")

if __name__ == "__main__":
    print("Restoring Windows Updates...")
    restore_services()
    restore_registry()
    restore_tasks()
    print("Windows Updates have been restored!")
'''
    
    try:
        with open("restore_windows_updates.py", "w") as f:
            f.write(restore_script)
        print("✓ Restore script created: restore_windows_updates.py")
    except Exception as e:
        print(f"✗ Failed to create restore script: {str(e)}")

def main():
    """Main function to execute all update disabling methods."""
    print("Windows 11 Update Disabler")
    print("=" * 40)
    
    if not is_admin():
        print("⚠️  WARNING: This script should be run as Administrator for full functionality.")
        print("Some operations may fail without elevated privileges.")
        input("Press Enter to continue anyway, or Ctrl+C to exit...")
    
    print("\nStarting Windows Update disabling process...")
    
    # Execute all disabling methods
    stop_update_services()
    modify_registry()
    disable_update_tasks()
    block_update_urls()
    create_restore_script()
    
    print("\n" + "=" * 40)
    print("✓ Windows Update disabling process completed!")
    print("\nNOTE: A system restart is recommended for all changes to take effect.")
    print("To restore updates later, run: python restore_windows_updates.py")
    
    restart = input("\nWould you like to restart now? (y/N): ").lower().strip()
    if restart == 'y':
        print("Restarting system in 10 seconds...")
        subprocess.run("shutdown /r /t 10", shell=True)

if __name__ == "__main__":
    main()
