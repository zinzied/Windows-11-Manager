#!/usr/bin/env python3
"""
Context Menu Manager for Windows 11 Update Manager
This module allows switching between Windows 11 (Modern) and Windows 10 (Classic) context menus.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import winreg
import os
import sys
import ctypes
import time

try:
    from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info
except ImportError:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info

def restart_explorer():
    """Restart Windows Explorer to apply changes."""
    print_info("Restarting Windows Explorer to apply changes...")
    try:
        subprocess.run("taskkill /f /im explorer.exe", shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        subprocess.Popen("explorer.exe")
        print_success("Windows Explorer restarted successfully.")
    except Exception as e:
        print_error(f"Failed to restart Explorer: {e}")

def enable_classic_context_menu():
    """Enable the Classic Windows 10 Context Menu."""
    print_header("Enabling Classic Context Menu")
    
    key_path = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
    
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)
        
        print_success("Classic Context Menu registry key added.")
        restart_explorer()
        print_success("Classic Windows 10 Context Menu enabled!")
        
    except Exception as e:
        print_error(f"Failed to enable Classic Context Menu: {e}")

def enable_modern_context_menu():
    """Restore the default Windows 11 Modern Context Menu."""
    print_header("Restoring Modern Context Menu")
    
    key_path = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}"
    
    try:
        # Check if key exists first
        try:
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        except FileNotFoundError:
            print_info("Modern Context Menu is already enabled (key not found).")
            return

        # Delete the key tree
        # Using reg delete is often more reliable for recursive delete
        subprocess.run(f'reg delete "HKCU\\{key_path}" /f', shell=True, check=True, stdout=subprocess.DEVNULL)
        
        print_success("Classic Context Menu registry key removed.")
        restart_explorer()
        print_success("Modern Windows 11 Context Menu restored!")
        
    except subprocess.CalledProcessError:
        print_error("Failed to delete registry key using reg command. (Maybe it's already gone?)")
    except Exception as e:
        print_error(f"Failed to restore Modern Context Menu: {e}")

def check_status():
    """Check which menu is currently active."""
    print_header("Checking Context Menu Status")
    key_path = r"Software\Classes\CLSID\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\InprocServer32"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.CloseKey(key)
        print_colored("Current Status: CLASSIC (Windows 10 Style)", Colors.GREEN)
        return "Classic"
    except FileNotFoundError:
        print_colored("Current Status: MODERN (Windows 11 Style)", Colors.BLUE)
        return "Modern"
    except Exception as e:
        print_error(f"Error checking status: {e}")
        return "Unknown"

def show_menu():
    """Display the menu."""
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored(f"{symbols.GEAR}  CONTEXT MENU MANAGER", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored("\n📋 Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. 💻 Enable Classic Context Menu (Win 10)", Colors.GREEN)
    print_colored("2. 🎨 Restore Modern Context Menu (Win 11)", Colors.BLUE)
    print_colored("3. 🔍 Check Current Status", Colors.YELLOW)
    print_colored("4. 🔙 Return to Main Menu", Colors.CYAN)

def main():
    while True:
        show_menu()
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-4): {Colors.END}").strip()
            
            if choice == '1':
                enable_classic_context_menu()
            elif choice == '2':
                enable_modern_context_menu()
            elif choice == '3':
                check_status()
            elif choice == '4':
                break
            else:
                print_error("Invalid choice! Please enter 1-4.")
            
            if choice in ['1', '2', '3']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nReturning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {e}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
