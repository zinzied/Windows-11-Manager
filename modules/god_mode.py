#!/usr/bin/env python3
"""
God Mode Manager for Windows 11 Update Manager
Creates the Master Control Panel (God Mode) shortcut on the desktop.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import os
import sys

try:
    from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info
except ImportError:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info

def get_desktop_path():
    """Get the path to the user's desktop."""
    return os.path.join(os.path.expanduser("~"), "Desktop")

def enable_god_mode():
    """Create the God Mode folder on the desktop."""
    print_header("Enabling God Mode")
    
    desktop = get_desktop_path()
    # The magical folder name
    folder_name = "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}"
    full_path = os.path.join(desktop, folder_name)
    
    try:
        if not os.path.exists(full_path):
            os.mkdir(full_path)
            print_success(f"God Mode activated successfully!")
            print_colored(f"Folder created at: {desktop}\\GodMode", Colors.WHITE)
        else:
            print_warning("God Mode folder already exists on your Desktop.")
            
    except Exception as e:
        print_error(f"Failed to create God Mode folder: {e}")

def disable_god_mode():
    """Remove the God Mode folder."""
    print_header("Disabling God Mode")
    
    desktop = get_desktop_path()
    folder_name = "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}"
    full_path = os.path.join(desktop, folder_name)
    
    try:
        if os.path.exists(full_path):
            os.rmdir(full_path)
            print_success("God Mode deactivated successfully (Folder removed).")
        else:
            print_warning("God Mode folder not found.")
            
    except Exception as e:
        print_error(f"Failed to remove God Mode folder: {e}")

def show_menu():
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored(f"🎩  GOD MODE MANAGER", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored("\n📋 Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. {symbols.CHECK} Enable God Mode (Create Desktop Icon)", Colors.GREEN)
    print_colored(f"2. {symbols.CROSS} Disable God Mode (Remove Icon)", Colors.RED)
    print_colored("3. 🔙 Return to Main Menu", Colors.CYAN)

def main():
    while True:
        show_menu()
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-3): {Colors.END}").strip()
            
            if choice == '1':
                enable_god_mode()
            elif choice == '2':
                disable_god_mode()
            elif choice == '3':
                break
            else:
                print_error("Invalid choice! Please enter 1-3.")
            
            if choice in ['1', '2']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nReturning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {e}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
