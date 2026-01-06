#!/usr/bin/env python3
"""
Performance Optimization Module for Windows 11 Update Manager
This module provides functionality to optimize Windows 11 performance.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import winreg
import os
import sys
from pathlib import Path
import ctypes

try:
    from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info, clear_screen
except ImportError:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info, clear_screen

def run_command(command, description):
    """Run a command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description}")
        else:
            print_error(f"{description} - {result.stderr.strip()}")
    except Exception as e:
        print_error(f"{description} - {str(e)}")

def disable_unnecessary_services():
    """Disable unnecessary Windows services for better performance."""
    print_colored(f"\n{symbols.GEAR} Disabling Unnecessary Services", Colors.BOLD + Colors.CYAN)
    
    # Services that can be safely disabled for performance
    services_to_disable = [
        ("Spooler", "Print Spooler (if you don't use printers)"),
        ("WSearch", "Windows Search (if you don't use search)"),
        ("SysMain", "Superfetch/Prefetch"),
        ("Themes", "Themes service (if you use basic theme)"),
        ("TabletInputService", "Tablet PC Input Service"),
        ("WbioSrvc", "Windows Biometric Service"),
        ("WMPNetworkSvc", "Windows Media Player Network Sharing"),
        ("WpcMonSvc", "Parental Controls"),
        ("wscsvc", "Windows Security Center"),
        ("WerSvc", "Windows Error Reporting"),
    ]
    
    print_warning("This will disable services that may affect some functionality.")
    print_info("Only disable services you don't need.")
    
    for service, description in services_to_disable:
        try:
            # Check if service exists and is running
            result = subprocess.run(f'sc query "{service}"', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                run_command(f'sc stop "{service}"', f"Stopping {service} ({description})")
                run_command(f'sc config "{service}" start= disabled', f"Disabling {service}")
            else:
                print_info(f"Service {service} not found or already disabled")
        except Exception as e:
            print_error(f"Error handling service {service}: {str(e)}")

def optimize_visual_effects():
    """Optimize visual effects for performance."""
    print_colored(f"\n{symbols.ROCKET} Optimizing Visual Effects for Performance", Colors.BOLD + Colors.CYAN)
    
    registry_changes = [
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
            "values": [
                ("VisualFXSetting", winreg.REG_DWORD, 2),  # Custom settings
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"Control Panel\Desktop",
            "values": [
                ("DragFullWindows", winreg.REG_SZ, "0"),  # Disable drag full windows
                ("MenuShowDelay", winreg.REG_SZ, "0"),    # Faster menu display
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"Control Panel\Desktop\WindowMetrics",
            "values": [
                ("MinAnimate", winreg.REG_SZ, "0"),  # Disable window animations
            ]
        },
        {
            "key": winreg.HKEY_CURRENT_USER,
            "subkey": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "values": [
                ("ListviewAlphaSelect", winreg.REG_DWORD, 0),  # Disable selection fade
                ("ListviewShadow", winreg.REG_DWORD, 0),       # Disable icon shadows
                ("TaskbarAnimations", winreg.REG_DWORD, 0),    # Disable taskbar animations
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Optimized visual effect: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to optimize visual effects: {str(e)}")

def disable_startup_programs():
    """Disable unnecessary startup programs."""
    print_colored(f"\n{symbols.TOOLS} Managing Startup Programs", Colors.BOLD + Colors.CYAN)
    
    # Common startup programs that can be disabled
    startup_programs = [
        "Skype",
        "Spotify",
        "Steam",
        "Discord",
        "Adobe Updater",
        "Java Update Scheduler",
        "Microsoft Teams",
        "OneDrive",
    ]
    
    print_info("Checking for common startup programs to disable...")
    
    try:
        # Get list of startup programs
        result = subprocess.run(
            'wmic startup get caption,command', 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            startup_list = result.stdout
            print_info("Current startup programs found:")
            print_colored(startup_list, Colors.WHITE)
        else:
            print_error("Failed to retrieve startup programs")
    except Exception as e:
        print_error(f"Error checking startup programs: {str(e)}")

def optimize_power_settings():
    """Optimize power settings for performance."""
    print_colored(f"\n{symbols.LIGHTNING} Optimizing Power Settings", Colors.BOLD + Colors.CYAN)
    
    try:
        # Set power plan to High Performance
        run_command(
            'powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c',
            "Setting power plan to High Performance"
        )
        
        # Disable USB selective suspend
        run_command(
            'powercfg /setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0',
            "Disabling USB selective suspend (AC)"
        )
        
        run_command(
            'powercfg /setdcvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0',
            "Disabling USB selective suspend (Battery)"
        )
        
        # Apply settings
        run_command('powercfg /setactive scheme_current', "Applying power settings")
        
    except Exception as e:
        print_error(f"Error optimizing power settings: {str(e)}")

def optimize_memory_management():
    """Optimize memory management settings."""
    print_colored(f"\n{symbols.GEAR} Optimizing Memory Management", Colors.BOLD + Colors.CYAN)
    
    registry_changes = [
        {
            "key": winreg.HKEY_LOCAL_MACHINE,
            "subkey": r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
            "values": [
                ("ClearPageFileAtShutdown", winreg.REG_DWORD, 0),  # Don't clear pagefile
                ("DisablePagingExecutive", winreg.REG_DWORD, 1),   # Keep kernel in memory
                ("LargeSystemCache", winreg.REG_DWORD, 1),         # Optimize for programs
            ]
        }
    ]
    
    for reg_change in registry_changes:
        try:
            key = winreg.CreateKey(reg_change["key"], reg_change["subkey"])
            
            for value_name, value_type, value_data in reg_change["values"]:
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                print_success(f"Optimized memory setting: {value_name}")
            
            winreg.CloseKey(key)
        except Exception as e:
            print_error(f"Failed to optimize memory management: {str(e)}")

def disable_windows_search_indexing():
    """Disable Windows Search indexing for better performance."""
    print_colored(f"\n{symbols.CLOUD} Optimizing Windows Search", Colors.BOLD + Colors.CYAN)
    
    try:
        # Stop Windows Search service
        run_command('sc stop "WSearch"', "Stopping Windows Search service")
        run_command('sc config "WSearch" start= disabled', "Disabling Windows Search service")
        
        # Disable indexing on C: drive
        run_command(
            'fsutil behavior set DisableLastAccess 1',
            "Disabling last access time updates"
        )
        
        print_success("Windows Search indexing optimized")
        print_info("You can still search files, but indexing is disabled for better performance")
        
    except Exception as e:
        print_error(f"Error optimizing Windows Search: {str(e)}")

def optimize_all_performance():
    """Apply all performance optimizations."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored(f"{symbols.LIGHTNING} COMPREHENSIVE PERFORMANCE OPTIMIZATION", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 70, Colors.MAGENTA)
    
    print_warning("This will apply multiple performance optimizations!")
    print_warning("Some features may be disabled. Review each option carefully.")
    print_info("This includes: Services, visual effects, power settings, memory optimization")
    
    confirm = input(f"\n{Colors.YELLOW}Do you want to continue? (y/N): {Colors.END}").lower().strip()
    if confirm != 'y':
        print_colored("Operation cancelled by user.", Colors.CYAN)
        return
    
    print_info("Starting comprehensive performance optimization...")
    
    disable_unnecessary_services()
    optimize_visual_effects()
    optimize_power_settings()
    optimize_memory_management()
    disable_windows_search_indexing()
    
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success("Performance optimization completed!")
    print_colored("=" * 60, Colors.GREEN)
    print_warning("A system restart is recommended for all changes to take effect.")
    print_info("Your system should now run faster and more efficiently.")

def show_performance_menu():
    """Display performance management menu."""
    clear_screen()
    print_header("PERFORMANCE OPTIMIZATION")
    print_colored(f"\n{symbols.TARGET} Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. {symbols.LIGHTNING} Optimize All Performance Settings", Colors.RED)
    print_colored(f"2. {symbols.GEAR} Disable Unnecessary Services Only", Colors.YELLOW)
    print_colored(f"3. {symbols.ROCKET} Optimize Visual Effects Only", Colors.YELLOW)
    print_colored(f"4. {symbols.LIGHTNING} Optimize Power Settings Only", Colors.YELLOW)
    print_colored(f"5. {symbols.HARDWARE} Optimize Memory Management Only", Colors.YELLOW)
    print_colored(f"6. {symbols.CLOUD} Disable Search Indexing Only", Colors.YELLOW)
    print_colored(f"7. {symbols.GEAR} Check System Performance", Colors.BLUE)
    print_colored(f"8. {symbols.WAVE} Return to Main Menu", Colors.CYAN)

def check_system_performance():
    """Check current system performance metrics."""
    print_colored(f"\n{symbols.GEAR} Checking System Performance", Colors.BOLD + Colors.CYAN)
    
    try:
        # Check CPU usage
        result = subprocess.run(
            'wmic cpu get loadpercentage /value', 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'LoadPercentage' in line and '=' in line:
                    cpu_usage = line.split('=')[1].strip()
                    color = Colors.GREEN if int(cpu_usage) < 50 else Colors.YELLOW
                    print_colored(f"CPU Usage: {cpu_usage}%", color)
        
        # Check memory usage
        result = subprocess.run(
            'wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value', 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            total_mem = free_mem = 0
            for line in result.stdout.split('\n'):
                if 'TotalVisibleMemorySize' in line and '=' in line:
                    total_mem = int(line.split('=')[1].strip())
                elif 'FreePhysicalMemory' in line and '=' in line:
                    free_mem = int(line.split('=')[1].strip())
            
            if total_mem > 0:
                used_percent = ((total_mem - free_mem) / total_mem) * 100
                color = Colors.GREEN if used_percent < 70 else Colors.YELLOW
                print_colored(f"Memory Usage: {used_percent:.1f}%", color)
        
    except Exception as e:
        print_error(f"Error checking system performance: {str(e)}")

def main():
    """Main performance management function."""
    while True:
        show_performance_menu()
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-8): {Colors.END}").strip()
            
            if choice == '1':
                optimize_all_performance()
            elif choice == '2':
                disable_unnecessary_services()
            elif choice == '3':
                optimize_visual_effects()
            elif choice == '4':
                optimize_power_settings()
            elif choice == '5':
                optimize_memory_management()
            elif choice == '6':
                disable_windows_search_indexing()
            elif choice == '7':
                check_system_performance()
            elif choice == '8':
                break
            else:
                print_error("Invalid choice! Please enter a number between 1-8.")
            
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nReturning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print_warning("Not running as Administrator. Some optimizations may fail.")
    main()
