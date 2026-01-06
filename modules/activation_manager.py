#!/usr/bin/env python3
"""
Windows Activation Manager for Windows 10 and 11
This script provides tools to manage Windows activation status.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import sys
import os
import platform
import ctypes
import tempfile
import time
import winreg

try:
    from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info, clear_screen
except ImportError:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info, clear_screen

def check_admin():
    """Check if running as administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_mas_script_path(script_path):
    """Identify absolute path for the MAS script."""
    # Check relatively to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, script_path)
    if os.path.exists(path):
        return path
        
    # Check in MAS/Separate-Files-Version relative to project root
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_path, "MAS", "Separate-Files-Version", script_path)
    if os.path.exists(path):
        return path
        
    return None

def run_mas_online_aio():
    """Run the Online MAS All-In-One script."""
    print_colored(f"\n{symbols.GLOBE}  ONLINE MAS ACTIVATION (AIO)", Colors.BOLD + Colors.CYAN)
    print_colored("This will launch the official Microsoft Activation Scripts (MAS) from massgrave.dev.", Colors.CYAN)
    print_colored("You can use this to activate Windows (HWID/KMS38) and Office (Ohook) permanently.", Colors.CYAN)
    
    confirm = input(f"\n{Colors.BOLD}Launch MAS Online? (y/N): {Colors.END}").strip().lower()
    if confirm != 'y':
        return False

    try:
        print_info("Launching MAS via PowerShell...")
        cmd = 'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://massgrave.dev/get | iex"'
        subprocess.run(cmd, shell=True)
        return True
    except Exception as e:
        print_error(f"Failed to launch MAS: {e}")
        return False

def get_activation_status():
    """Get the current Windows activation status (legacy method)."""
    try:
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as tf:
            tf_path = tf.name
        
        try:
            subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dli'], 
                         stdout=open(tf_path, 'wb'), stderr=subprocess.DEVNULL, check=True)
            with open(tf_path, 'rb') as f:
                output = f.read().decode('cp1252', errors='replace')
        finally:
            if os.path.exists(tf_path): os.unlink(tf_path)

        status = {'licensed': False, 'license_status': 'Unknown', 'product_key': None, 'description': None}
        
        for line in output.split('\n'):
            if 'License Status' in line:
                status['license_status'] = line.split(':')[1].strip() if ':' in line else 'Unknown'
                if 'Licensed' in status['license_status']:
                    status['licensed'] = True
            elif 'Product Key' in line:
                status['product_key'] = line.split(':')[1].strip() if ':' in line else 'Not available'
            elif 'Description' in line:
                status['description'] = line.split(':')[1].strip() if ':' in line else 'Not available'

        return status
    except Exception as e:
        print_error(f"Error checking status: {e}")
        return None

def display_activation_status():
    """Display the current Windows activation status."""
    print_colored(f"\n{symbols.INFO}  ACTIVATION STATUS CHECK", Colors.BOLD + Colors.CYAN)
    status = get_activation_status()
    if not status: return

    print_colored("=" * 50, Colors.BLUE)
    if status['licensed']:
        print_success(f"Status: {status['license_status']}")
        print_colored(f"{symbols.KEY} Product Key: {status['product_key']}", Colors.WHITE)
        print_info(f"Description: {status['description']}")
    else:
        print_error(f"Status: {status['license_status']}")
        print_warning("Windows is not activated")
        print_info(f"Description: {status['description']}")

def activate_windows(product_key=None):
    """Attempt to activate Windows with a product key."""
    print_colored(f"\n{symbols.KEY}  ACTIVATE WINDOWS WITH KEY", Colors.BOLD + Colors.CYAN)

    if not product_key:
        print_info("Enter your 25-character product key:")
        product_key = input(f"{Colors.BOLD}> {Colors.END}").strip()
        if not product_key: return

    print_info("Installing key...")
    try:
        subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/ipk', product_key], check=True, stdout=subprocess.DEVNULL)
        print_success("Key installed. Activating...")
        subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/ato'], check=True, stdout=subprocess.DEVNULL)
        print_success("Activation command sent successfully!")
        display_activation_status()
    except subprocess.CalledProcessError:
        print_error("Activation failed. Key may be invalid or blocked.")

def reset_activation():
    """Reset Windows activation (rearm)."""
    print_colored(f"\n{symbols.WARNING}  RESET ACTIVATION (REARM)", Colors.BOLD + Colors.YELLOW)
    print_warning("This resets activation status and trial timers.")
    if input(f"{Colors.BOLD}Confirm reset? (y/N): {Colors.END}").lower() != 'y': return

    print_info("Resetting...")
    try:
        subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/rearm'], check=True, stdout=subprocess.DEVNULL)
        print_success("Reset complete! Restart your computer.")
    except Exception as e:
        print_error(f"Reset failed: {e}")

def show_activation_help():
    """Show help information."""
    print_colored(f"\n{symbols.BOOK}  ACTIVATION HELP", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 50, Colors.CYAN)
    print_colored(f"• {symbols.SHIELD} MAS Online: Launches the Microsoft Activation Scripts menu.", Colors.WHITE)
    print_colored("  - HWID: Permanent activation for Win 10/11.", Colors.WHITE)
    print_colored("  - Ohook: Permanent activation for Office.", Colors.WHITE)
    print_colored(f"• {symbols.KEY} Product Key: Use a retail/OEM key if you have one.", Colors.WHITE)
    print_colored(f"• {symbols.RECYCLE} Rearm: Fixes activation errors by resetting state.", Colors.WHITE)

def main_menu():
    """Main menu for activation manager."""
    while True:
        clear_screen()
        print_header("WINDOWS ACTIVATION MANAGER")
        
        print_colored(f"\n{symbols.TARGET} Choose an option:", Colors.BOLD + Colors.CYAN)
        print_colored(f"1. {symbols.INFO} Check Activation Status", Colors.WHITE)
        print_colored(f"2. {symbols.GLOBE} Run MAS Online (HWID/Ohook/KMS38)", Colors.GREEN)
        print_colored(f"3. {symbols.KEY} Activate with Product Key", Colors.WHITE)
        print_colored(f"4. {symbols.RECYCLE} Reset Activation (Rearm)", Colors.YELLOW)
        print_colored(f"5. {symbols.BOOK} Activation Help", Colors.BLUE)
        print_colored(f"0. {symbols.WAVE} Return to Main Menu", Colors.CYAN)
        
        choice = input(f"\n{Colors.BOLD}Choice (0-5): {Colors.END}").strip()
        
        if choice == '1': display_activation_status()
        elif choice == '2': run_mas_online_aio()
        elif choice == '3': activate_windows()
        elif choice == '4': reset_activation()
        elif choice == '5': show_activation_help()
        elif choice == '0': break
        
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    if not check_admin():
        print_warning("Run as Administrator for full functionality.")
    main_menu()
