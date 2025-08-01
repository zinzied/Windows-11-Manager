#!/usr/bin/env python3
"""
Windows 11 Update Manager - Main Launcher
This script provides a main menu to choose between disabling or restoring Windows updates.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import subprocess
import sys
import os

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'  # End color formatting

def print_colored(text, color=Colors.WHITE):
    """Print text with color."""
    print(f"{color}{text}{Colors.END}")

def print_header():
    """Print the main header."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored("🛡️  WINDOWS 11 UPDATE MANAGER - MAIN LAUNCHER", Colors.BOLD + Colors.MAGENTA)
    print_colored("    Created by Zied Boughdir - 2025", Colors.CYAN)
    print_colored("    GitHub: https://github.com/zinzied", Colors.BLUE)
    print_colored("=" * 70, Colors.MAGENTA)
    print_colored("    Complete Control Over Your Windows 11 Updates", Colors.CYAN)
    print_colored("=" * 70, Colors.MAGENTA)

def show_main_menu():
    """Display the main launcher menu."""
    print_header()
    print_colored("\n🎯 What would you like to do?", Colors.BOLD + Colors.CYAN)
    print_colored("\n1. 🚫 DISABLE Windows Updates", Colors.RED)
    print_colored("   └─ Stop, disable, and block all Windows update mechanisms", Colors.WHITE)
    print_colored("\n2. 🔄 RESTORE Windows Updates", Colors.GREEN)
    print_colored("   └─ Re-enable all Windows update functionality", Colors.WHITE)
    print_colored("\n3. ℹ️  INFORMATION", Colors.BLUE)
    print_colored("   └─ Learn about Windows Update management", Colors.WHITE)
    print_colored("\n4. ❌ EXIT", Colors.YELLOW)
    print_colored("\n" + "=" * 70, Colors.MAGENTA)

def show_information():
    """Display information about the tools."""
    print_colored("\n" + "=" * 70, Colors.BLUE)
    print_colored("ℹ️  WINDOWS 11 UPDATE MANAGER - INFORMATION", Colors.BOLD + Colors.BLUE)
    print_colored("=" * 70, Colors.BLUE)
    
    print_colored("\n🔧 WHAT THIS TOOL DOES:", Colors.BOLD + Colors.CYAN)
    print_colored("• Stops Windows Update services (wuauserv, bits, dosvc, UsoSvc)", Colors.WHITE)
    print_colored("• Modifies registry to disable automatic updates", Colors.WHITE)
    print_colored("• Disables Windows Update scheduled tasks", Colors.WHITE)
    print_colored("• Blocks Windows Update URLs in hosts file", Colors.WHITE)
    print_colored("• Provides complete restoration capabilities", Colors.WHITE)
    
    print_colored("\n⚠️  IMPORTANT WARNINGS:", Colors.BOLD + Colors.YELLOW)
    print_colored("• Run as Administrator for full functionality", Colors.YELLOW)
    print_colored("• Disabling updates can leave your system vulnerable", Colors.YELLOW)
    print_colored("• Only disable updates when absolutely necessary", Colors.YELLOW)
    print_colored("• Keep the restore script safe for future use", Colors.YELLOW)
    print_colored("• Restart recommended after making changes", Colors.YELLOW)
    
    print_colored("\n🎯 WHEN TO USE:", Colors.BOLD + Colors.GREEN)
    print_colored("• System stability issues caused by updates", Colors.WHITE)
    print_colored("• Professional environments requiring controlled updates", Colors.WHITE)
    print_colored("• Limited bandwidth or metered connections", Colors.WHITE)
    print_colored("• Gaming or performance-critical applications", Colors.WHITE)
    print_colored("• Legacy software compatibility requirements", Colors.WHITE)
    print_colored("• Development and testing environments", Colors.WHITE)
    
    print_colored("\n📁 FILES INCLUDED:", Colors.BOLD + Colors.MAGENTA)
    print_colored("• disable_windows_updates.py - Main disable script", Colors.WHITE)
    print_colored("• restore_windows_updates.py - Restoration script", Colors.WHITE)
    print_colored("• launcher.py - This main menu launcher", Colors.WHITE)
    print_colored("• README.md - Complete documentation", Colors.WHITE)
    print_colored("• requirements.txt - Dependency information", Colors.WHITE)
    
    print_colored("\n" + "=" * 70, Colors.BLUE)

def run_script(script_name):
    """Run a Python script."""
    try:
        print_colored(f"\n🚀 Launching {script_name}...", Colors.CYAN)
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print_colored(f"\n❌ Error running {script_name}: {e}", Colors.RED)
    except FileNotFoundError:
        print_colored(f"\n❌ Script not found: {script_name}", Colors.RED)
        print_colored("Make sure all files are in the same directory.", Colors.YELLOW)
    except KeyboardInterrupt:
        print_colored(f"\n⏹️  {script_name} was interrupted by user.", Colors.YELLOW)

def check_admin():
    """Check if running as administrator."""
    try:
        subprocess.run(['net', 'session'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main launcher function."""
    # Check admin status
    is_admin = check_admin()
    
    while True:
        show_main_menu()
        
        if not is_admin:
            print_colored("\n⚠️  NOT RUNNING AS ADMINISTRATOR", Colors.BOLD + Colors.YELLOW)
            print_colored("Some features may not work properly. Consider running as Administrator.", Colors.YELLOW)
        else:
            print_colored("\n✅ RUNNING AS ADMINISTRATOR", Colors.BOLD + Colors.GREEN)
        
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-4): {Colors.END}").strip()
            
            if choice == '1':
                run_script("disable_windows_updates.py")
            elif choice == '2':
                run_script("restore_windows_updates.py")
            elif choice == '3':
                show_information()
                input(f"\n{Colors.CYAN}Press Enter to return to main menu...{Colors.END}")
            elif choice == '4':
                print_colored("\n👋 Thank you for using Windows 11 Update Manager!", Colors.BOLD + Colors.CYAN)
                print_colored("Stay safe and keep your system secure! 🛡️", Colors.GREEN)
                break
            else:
                print_colored("\n❌ Invalid choice! Please enter 1, 2, 3, or 4.", Colors.RED)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\n👋 Goodbye! Thanks for using Windows 11 Update Manager!", Colors.BOLD + Colors.CYAN)
            break
        except Exception as e:
            print_colored(f"\n❌ An error occurred: {str(e)}", Colors.RED)
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
