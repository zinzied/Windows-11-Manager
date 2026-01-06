#!/usr/bin/env python3
"""
System Cleaner Module for Windows 11 Update Manager
This module provides functionality to clean temporary files and caches.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import os
import shutil
import time
import ctypes

try:
    from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info
except ImportError:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info

def get_dir_size(path):
    """Calculate directory size in MB."""
    total_size = 0
    try:
        if os.path.exists(path):
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        total_size += os.path.getsize(fp)
                    except:
                        pass
        return total_size / (1024 * 1024)
    except:
        return 0

def clean_directory(path, name):
    """Clean contents of a directory."""
    if not os.path.exists(path):
        print_info(f"{name} path not found: {path} (Skipping)")
        return 0

    size_before = get_dir_size(path)
    print_info(f"Cleaning {name} ({size_before:.2f} MB)...")
    
    deleted_files = 0
    errors = 0
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                deleted_files += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                deleted_files += 1
        except Exception as e:
            errors += 1
            # print_error(f"Failed to delete {item}: {e}") # Too verbose
    
    size_after = get_dir_size(path)
    cleaned = size_before - size_after
    
    if errors > 0:
        print_warning(f"Cleaned {name}: Removed {deleted_files} items. {errors} items skipped (in use/access denied).")
    else:
        print_success(f"Cleaned {name}: All items removed.")
    
    print_colored(f"Space freed: {cleaned:.2f} MB", Colors.GREEN)
    return cleaned

def clean_temp_files():
    """Clean Windows temporary files."""
    print_header("Cleaning Temporary Files")
    
    total_freed = 0
    
    # User Temp
    user_temp = os.environ.get('TEMP')
    if user_temp:
        total_freed += clean_directory(user_temp, "User Temp")
    
    # Windows Temp
    win_temp = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp')
    total_freed += clean_directory(win_temp, "Windows Temp")
    
    return total_freed

def clean_prefetch():
    """Clean Windows Prefetch files."""
    print_header("Cleaning Windows Prefetch")
    
    prefetch_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch')
    return clean_directory(prefetch_path, "Prefetch")

def clean_update_cache():
    """Clean Windows Update Cache (SoftwareDistribution)."""
    print_header("Cleaning Windows Update Cache")
    
    # Stop services first
    print_info("Stopping Windows Update services...")
    services = ["wuauserv", "bits", "dosvc"]
    for service in services:
        subprocess.run(f'net stop "{service}"', shell=True, capture_output=True)
    
    # Clean SoftwareDistribution/Download
    update_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'SoftwareDistribution', 'Download')
    freed = clean_directory(update_path, "Update Downloads")
    
    # Restart services
    print_info("Restarting Windows Update services...")
    for service in services:
        subprocess.run(f'net start "{service}"', shell=True, capture_output=True)
        
    return freed

def flush_dns():
    """Flush DNS Resolver Cache."""
    print_header("Flushing DNS Cache")
    
    try:
        result = subprocess.run('ipconfig /flushdns', shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success("DNS Resolver Cache successfully flushed.")
            return True
        else:
            print_error("Failed to flush DNS cache.")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def clean_all_system():
    """Run all cleaning tasks."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored(f"{symbols.TRASH}  FULL SYSTEM CLEANUP", Colors.BOLD + Colors.MAGENTA)
    print_colored("=" * 70, Colors.MAGENTA)
    
    print_warning("This will delete temporary files. Ensure your work is saved.")
    confirm = input(f"\n{Colors.YELLOW}Do you want to continue? (y/N): {Colors.END}").lower().strip()
    if confirm != 'y':
        print_colored("Operation cancelled.", Colors.CYAN)
        return

    total_freed = 0
    total_freed += clean_temp_files()
    total_freed += clean_prefetch()
    total_freed += clean_update_cache()
    flush_dns()
    
    print_colored("\n" + "=" * 60, Colors.GREEN)
    print_success(f"System Cleanup Completed! Total space freed: {total_freed:.2f} MB")
    print_colored("=" * 60, Colors.GREEN)
    input(f"\n{Colors.CYAN}Press Enter to return...{Colors.END}")

def show_menu():
    """Display cleaner menu."""
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored(f"{symbols.TRASH}  SYSTEM OPTIMIZER & CLEANER", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored(f"\n{symbols.TARGET} Choose an option:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. {symbols.ROCKET} One-Click System Cleanup (Temp, Cache, Prefetch)", Colors.GREEN)
    print_colored(f"2. {symbols.TRASH}  Clean Temporary Files Only", Colors.YELLOW)
    print_colored(f"3. {symbols.FOLDER} Clean Windows Update Cache", Colors.YELLOW)
    print_colored(f"4. {symbols.LIGHTNING} Clean Prefetch Files", Colors.YELLOW)
    print_colored(f"5. {symbols.CLOUD} Flush DNS Cache", Colors.BLUE)
    print_colored(f"6. {symbols.WAVE} Return to Main Menu", Colors.CYAN)

def main():
    while True:
        show_menu()
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-6): {Colors.END}").strip()
            
            if choice == '1':
                clean_all_system()
            elif choice == '2':
                freed = clean_temp_files()
                print_success(f"Freed {freed:.2f} MB")
            elif choice == '3':
                freed = clean_update_cache()
                print_success(f"Freed {freed:.2f} MB")
            elif choice == '4':
                freed = clean_prefetch()
                print_success(f"Freed {freed:.2f} MB")
            elif choice == '5':
                flush_dns()
            elif choice == '6':
                break
            else:
                print_error("Invalid choice! Please enter 1-6.")
            
            if choice in ['2', '3', '4', '5']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nReturning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {e}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print_warning("Not running as Administrator. Some files may not be deleted.")
        print_info("For best results, run as Administrator.")
        time.sleep(2)
    main()
