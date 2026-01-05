#!/usr/bin/env python3
"""
Software Installer Module for Windows 11 Update Manager
Allows easy installation of essential software using winget.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import os
import sys

try:
    from console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info
except ImportError:
    from modules.console_utils import Colors, matches as symbols, print_colored, print_header, print_success, print_error, print_warning, print_info

def check_winget():
    """Check if winget is installed."""
    try:
        subprocess.run("winget --version", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def install_package(package_id, name):
    """Install a package using winget."""
    print_info(f"Installing {name}...")
    try:
        # -e: exact match, --accept-source-agreements --accept-package-agreements: auto accept
        cmd = f'winget install --id "{package_id}" -e --accept-source-agreements --accept-package-agreements'
        subprocess.run(cmd, shell=True, check=True)
        print_success(f"Successfully installed {name}!")
    except subprocess.CalledProcessError:
        print_error(f"Failed to install {name}. It might be already installed or network issue.")
    except Exception as e:
        print_error(f"Error: {e}")

def show_category_menu(category_name, packages):
    while True:
        print_colored(f"\n{symbols.FOLDER} Category: {category_name}", Colors.BOLD + Colors.MAGENTA)
        for i, (name, pkg_id) in enumerate(packages, 1):
            print_colored(f"{i}. {name}", Colors.WHITE)
        print_colored(f"{len(packages) + 1}. Install ALL in this category", Colors.YELLOW)
        print_colored(f"{len(packages) + 2}. Back", Colors.CYAN)
        
        try:
            choice = int(input(f"\n{Colors.BOLD}Select app to install: {Colors.END}"))
            
            if 1 <= choice <= len(packages):
                name, pkg_id = packages[choice - 1]
                install_package(pkg_id, name)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == len(packages) + 1:
                confirm = input(f"{Colors.YELLOW}Install ALL {len(packages)} apps in this category? (y/n): {Colors.END}")
                if confirm.lower() == 'y':
                    for name, pkg_id in packages:
                        install_package(pkg_id, name)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == len(packages) + 2:
                break
            else:
                print_error("Invalid choice.")
        except ValueError:
            print_error("Please enter a number.")

def show_main_menu():
    
    # Software Categories
    browsers = [
        ("Google Chrome", "Google.Chrome"),
        ("Mozilla Firefox", "Mozilla.Firefox"),
        ("Brave Browser", "Brave.Brave"),
        ("Microsoft Edge", "Microsoft.Edge")
    ]
    
    media = [
        ("VLC Media Player", "VideoLAN.VLC"),
        ("Spotify", "Spotify.Spotify"),
        ("Discord", "Discord.Discord"),
        ("OBS Studio", "OBSProject.OBSStudio")
    ]
    
    dev = [
        ("VS Code", "Microsoft.VisualStudioCode"),
        ("Python 3", "Python.Python.3"),
        ("Node.js LTS", "OpenJS.NodeJS.LTS"),
        ("Git", "Git.Git"),
        ("Notepad++", "Notepad++.Notepad++")
    ]
    
    tools = [
        ("7-Zip", "7zip.7zip"),
        ("Powertoys", "Microsoft.PowerToys"),
        ("WinRAR", "RARLab.WinRAR"),
        ("AnyDesk", "AnyDeskSoftwareGmbH.AnyDesk")
    ]

    while True:
        print_colored("\n" + "=" * 60, Colors.CYAN)
        print_colored(f"{symbols.TOOLS}  SOFTWARE INSTALLER (using Winget)", Colors.BOLD + Colors.CYAN)
        print_colored("=" * 60, Colors.CYAN)
        
        if not check_winget():
            print_error("Winget is not detected on your system!")
            print_info("Please update Windows App Installer from Microsoft Store.")
            return

        print_colored("\n📋 Select Category:", Colors.BOLD + Colors.CYAN)
        print_colored("\n1. 🌐 Browsers (Chrome, Firefox...)", Colors.GREEN)
        print_colored(f"2. {symbols.CLOUD} Media & Social (VLC, Discord...)", Colors.MAGENTA)
        print_colored(f"3. {symbols.GEAR} Development (VS Code, Python...)", Colors.YELLOW)
        print_colored(f"4. {symbols.TOOLS} Tools & Utilities (7-Zip, PowerToys...)", Colors.BLUE)
        print_colored("5. 🔙 Return to Main Menu", Colors.CYAN)

        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-5): {Colors.END}").strip()
            
            if choice == '1':
                show_category_menu("Browsers", browsers)
            elif choice == '2':
                show_category_menu("Media & Social", media)
            elif choice == '3':
                show_category_menu("Development", dev)
            elif choice == '4':
                show_category_menu("Tools & Utilities", tools)
            elif choice == '5':
                break
            else:
                print_error("Invalid choice.")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print_error(f"Error: {e}")

if __name__ == "__main__":
    show_main_menu()
