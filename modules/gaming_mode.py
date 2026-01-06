#!/usr/bin/env python3
"""
Gaming Mode Manager for Windows 11 Update Manager
Optimizes system performance for gaming sessions.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import os
import sys
import ctypes

try:
    from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info
except ImportError:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info

def enable_gaming_mode():
    """Enable Gaming Mode optimizations."""
    print_header("Activating Gaming Mode")
    
    # 1. Switch to High Performance Power Plan
    print_info("Switching to High Performance Power Plan...")
    try:
        # High Performance GUID: 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
        subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True, check=True, stdout=subprocess.DEVNULL)
        print_success("High Performance plan activated.")
    except Exception:
        print_error("Failed to set power plan.")

    # 2. Stop unnecessary services
    print_info("Stopping background services...")
    services_to_pause = ["Spooler", "WSearch", "SysMain", "Themes"]
    services_list = []
    
    for service in services_to_pause:
        try:
            subprocess.run(f'net stop "{service}"', shell=True, capture_output=True)
            services_list.append(service)
        except:
            pass
            
    if services_list:
        print_success(f"Paused services: {', '.join(services_list)}")

    # 3. Optimize Visual Effects (Optional - minimal)
    # We won't disable everything, just maybe animations if we wanted to, but let's stick to safe tweaks
    
    print_colored(f"\n{symbols.LIGHTNING} GAMING MODE ACTIVATED!", Colors.GREEN + Colors.BOLD)
    print_info(f"{symbols.BULLET} Power Plan: High Performance")
    print_info(f"{symbols.BULLET} Background Services: Paused")
    print_info(f"{symbols.BULLET} System resources focused on gaming")
    print_info("\nDon't forget to deactivate Gaming Mode when finished!")

def disable_gaming_mode():
    """Disable Gaming Mode and restore settings."""
    print_header("Deactivating Gaming Mode")
    
    # 1. Restore Balanced Power Plan
    print_info("Restoring Balanced Power Plan...")
    try:
        # Balanced GUID: 381b4222-f694-41f0-9685-ff5bb260df2e
        subprocess.run('powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e', shell=True, check=True, stdout=subprocess.DEVNULL)
        print_success("Balanced plan restored.")
    except Exception:
        print_error("Failed to restore power plan.")

    # 2. Restart services
    print_info("Restarting background services...")
    services_to_resume = ["Spooler", "WSearch", "SysMain", "Themes"]
    services_list = []
    
    for service in services_to_resume:
        try:
            subprocess.run(f'net start "{service}"', shell=True, capture_output=True)
            services_list.append(service)
        except:
            pass
            
    if services_list:
        print_success(f"Resumed services: {', '.join(services_list)}")

    print_colored(f"\n{symbols.STOP} GAMING MODE DEACTIVATED", Colors.YELLOW + Colors.BOLD)
    print_success("System settings restored to normal.")

def show_menu():
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored(f"{symbols.LIGHTNING}  GAMING MODE OPTIMIZER", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored(f"\n{symbols.TARGET} Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. {symbols.ROCKET} Activate Gaming Mode (High Perf + Kill Services)", Colors.GREEN)
    print_colored(f"2. {symbols.STOP} Deactivate Gaming Mode (Restore Defaults)", Colors.YELLOW)
    print_colored(f"3. {symbols.WAVE} Return to Main Menu", Colors.CYAN)

def main():
    while True:
        show_menu()
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-3): {Colors.END}").strip()
            
            if choice == '1':
                enable_gaming_mode()
            elif choice == '2':
                disable_gaming_mode()
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
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print_warning("Admin privileges required for power plans and services.")
    main()
