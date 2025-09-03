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
import ctypes
import platform

# Set UTF-8 encoding for better symbol support
if sys.platform == 'win32':
    try:
        # Try to set console to UTF-8
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass

# Try to import colorama for better Windows color support
try:
    from colorama import init, Fore, Back, Style
    COLORAMA_AVAILABLE = True
    # Initialize colorama
    init(autoreset=True)
except ImportError:
    COLORAMA_AVAILABLE = False

# Symbol definitions with fallbacks for terminals that don't support Unicode
class Symbols:
    def __init__(self):
        # Test if terminal supports Unicode
        self.unicode_supported = self._test_unicode_support()

        if self.unicode_supported:
            # Unicode symbols
            self.SHIELD = "🛡️"
            self.TARGET = "🎯"
            self.GEAR = "🔧"
            self.TOOLS = "🛠️"
            self.CLOUD = "☁️"
            self.LOCK = "🔒"
            self.TRASH = "🗑️"
            self.LIGHTNING = "⚡"
            self.INFO = "ℹ️"
            self.CROSS = "❌"
            self.CHECK = "✅"
            self.WARNING = "⚠️"
            self.ROCKET = "🚀"
            self.STOP = "⏹️"
            self.WAVE = "👋"
            self.RECYCLE = "🔄"
            self.BLOCK = "🚫"
            self.KEY = "🔑"
            self.FOLDER = "📁"
            self.BOOK = "📖"
        else:
            # ASCII fallbacks
            self.SHIELD = "[SHIELD]"
            self.TARGET = "[TARGET]"
            self.GEAR = "[GEAR]"
            self.TOOLS = "[TOOLS]"
            self.CLOUD = "[CLOUD]"
            self.LOCK = "[LOCK]"
            self.TRASH = "[TRASH]"
            self.LIGHTNING = "[FAST]"
            self.INFO = "[INFO]"
            self.CROSS = "[X]"
            self.CHECK = "[OK]"
            self.WARNING = "[!]"
            self.ROCKET = "[START]"
            self.STOP = "[STOP]"
            self.WAVE = "[BYE]"
            self.RECYCLE = "[CYCLE]"
            self.BLOCK = "[BLOCK]"
            self.KEY = "[KEY]"
            self.FOLDER = "[FOLDER]"
            self.BOOK = "[BOOK]"

    def _test_unicode_support(self):
        """Test if the terminal supports Unicode symbols."""
        try:
            # Try to encode a Unicode symbol
            test_symbol = "🛡️"
            test_symbol.encode(sys.stdout.encoding or 'utf-8')
            return True
        except (UnicodeEncodeError, AttributeError):
            return False

# Initialize symbols
symbols = Symbols()

# Enable ANSI color support on Windows
def enable_ansi_colors():
    """Enable ANSI color codes on Windows terminals."""
    if platform.system() == "Windows":
        try:
            # Enable ANSI escape sequence processing
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True

# Color codes for terminal output
class Colors:
    if COLORAMA_AVAILABLE:
        # Use colorama colors for better Windows support
        RED = Fore.RED + Style.BRIGHT
        GREEN = Fore.GREEN + Style.BRIGHT
        YELLOW = Fore.YELLOW + Style.BRIGHT
        BLUE = Fore.BLUE + Style.BRIGHT
        MAGENTA = Fore.MAGENTA + Style.BRIGHT
        CYAN = Fore.CYAN + Style.BRIGHT
        WHITE = Fore.WHITE + Style.BRIGHT
        BOLD = Style.BRIGHT
        UNDERLINE = ''  # Colorama doesn't have underline
        END = Style.RESET_ALL
    else:
        # Fallback to ANSI codes
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
    if COLORAMA_AVAILABLE:
        # Colorama handles everything for us
        print(f"{color}{text}")
    else:
        # Try ANSI codes with fallback
        try:
            if not hasattr(print_colored, '_ansi_tested'):
                enable_ansi_colors()
                print_colored._ansi_tested = True
            print(f"{color}{text}{Colors.END}")
        except Exception:
            # Fallback to plain text
            print(text)

def print_header():
    """Print the main header."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored(f"{symbols.SHIELD}  WINDOWS 11 UPDATE MANAGER - MAIN LAUNCHER", Colors.BOLD + Colors.MAGENTA)
    print_colored("    Created by Zied Boughdir - 2025", Colors.CYAN)
    print_colored("    GitHub: https://github.com/zinzied", Colors.BLUE)
    print_colored("=" * 70, Colors.MAGENTA)
    print_colored("    Complete Control Over Your Windows 11 Updates", Colors.CYAN)
    print_colored("=" * 70, Colors.MAGENTA)

def show_main_menu():
    """Display the main launcher menu."""
    print_header()
    print_colored(f"\n{symbols.TARGET} What would you like to do?", Colors.BOLD + Colors.CYAN)

    print_colored(f"\n{symbols.RECYCLE} UPDATE MANAGEMENT:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"1. {symbols.BLOCK} DISABLE Windows Updates", Colors.RED)
    print_colored("   └─ Stop, disable, and block all Windows update mechanisms", Colors.WHITE)
    print_colored(f"2. {symbols.RECYCLE} RESTORE Windows Updates", Colors.GREEN)
    print_colored("   └─ Re-enable all Windows update functionality", Colors.WHITE)
    print_colored(f"3. {symbols.RECYCLE} COMPREHENSIVE RESTORE", Colors.BOLD + Colors.GREEN)
    print_colored("   └─ Restore ALL system modifications (Updates, OneDrive, etc.)", Colors.WHITE)

    print_colored(f"\n{symbols.TOOLS}  SYSTEM MANAGEMENT:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"4. {symbols.CLOUD}  OneDrive Management", Colors.CYAN)
    print_colored("   └─ Disable/enable OneDrive completely", Colors.WHITE)
    print_colored(f"5. {symbols.LOCK} Privacy & Telemetry Control", Colors.CYAN)
    print_colored("   └─ Disable telemetry and enhance privacy", Colors.WHITE)
    print_colored(f"6. {symbols.TRASH}  Bloatware Removal", Colors.CYAN)
    print_colored("   └─ Remove unnecessary Windows apps and features", Colors.WHITE)
    print_colored(f"7. {symbols.LIGHTNING} Performance Optimization", Colors.CYAN)
    print_colored("   └─ Optimize system performance and speed", Colors.WHITE)
    print_colored(f"8. {symbols.KEY} Windows Activation Manager", Colors.CYAN)
    print_colored("   └─ Manage Windows 10/11 activation status", Colors.WHITE)

    print_colored(f"\n{symbols.BOOK} HELP & INFO:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"9. {symbols.INFO}  INFORMATION", Colors.BLUE)
    print_colored("   └─ Learn about Windows system management", Colors.WHITE)

    # Show admin option if not running as admin
    if not check_admin():
        print_colored(f"10. {symbols.KEY} RESTART AS ADMINISTRATOR", Colors.BOLD + Colors.GREEN)
        print_colored("   └─ Restart with elevated privileges", Colors.WHITE)
        print_colored(f"0. {symbols.CROSS} EXIT", Colors.YELLOW)
    else:
        print_colored(f"0. {symbols.CROSS} EXIT", Colors.YELLOW)

    print_colored("\n" + "=" * 70, Colors.MAGENTA)

def show_information():
    """Display information about the tools."""
    print_colored("\n" + "=" * 70, Colors.BLUE)
    print_colored(f"{symbols.INFO}  WINDOWS 11 SYSTEM MANAGER - INFORMATION", Colors.BOLD + Colors.BLUE)
    print_colored("=" * 70, Colors.BLUE)

    print_colored(f"\n{symbols.GEAR} UPDATE MANAGEMENT:", Colors.BOLD + Colors.CYAN)
    print_colored("• Stops Windows Update services (wuauserv, bits, dosvc, UsoSvc)", Colors.WHITE)
    print_colored("• Modifies registry to disable automatic updates", Colors.WHITE)
    print_colored("• Disables Windows Update scheduled tasks", Colors.WHITE)
    print_colored("• Blocks Windows Update URLs in hosts file", Colors.WHITE)
    print_colored("• Provides complete restoration capabilities", Colors.WHITE)

    print_colored(f"\n{symbols.TOOLS}  SYSTEM MANAGEMENT:", Colors.BOLD + Colors.CYAN)
    print_colored("• OneDrive: Complete disable/enable with registry cleanup", Colors.WHITE)
    print_colored("• Telemetry: Disable data collection and enhance privacy", Colors.WHITE)
    print_colored("• Bloatware: Remove unnecessary Windows apps and features", Colors.WHITE)
    print_colored("• Performance: Optimize services, visual effects, and power", Colors.WHITE)
    print_colored("• Privacy: Control location, advertising ID, and feedback", Colors.WHITE)

    print_colored(f"\n{symbols.WARNING}  IMPORTANT WARNINGS:", Colors.BOLD + Colors.YELLOW)
    print_colored("• Run as Administrator for full functionality", Colors.YELLOW)
    print_colored("• Disabling updates can leave your system vulnerable", Colors.YELLOW)
    print_colored("• Only disable updates when absolutely necessary", Colors.YELLOW)
    print_colored("• Keep the restore script safe for future use", Colors.YELLOW)
    print_colored("• Restart recommended after making changes", Colors.YELLOW)

    print_colored(f"\n{symbols.TARGET} WHEN TO USE:", Colors.BOLD + Colors.GREEN)
    print_colored("• System stability issues caused by updates", Colors.WHITE)
    print_colored("• Professional environments requiring controlled updates", Colors.WHITE)
    print_colored("• Limited bandwidth or metered connections", Colors.WHITE)
    print_colored("• Gaming or performance-critical applications", Colors.WHITE)
    print_colored("• Legacy software compatibility requirements", Colors.WHITE)
    print_colored("• Development and testing environments", Colors.WHITE)

    print_colored(f"\n{symbols.FOLDER} FILES INCLUDED:", Colors.BOLD + Colors.MAGENTA)
    print_colored("• disable_windows_updates.py - Main disable script", Colors.WHITE)
    print_colored("• restore_windows_updates.py - Restoration script", Colors.WHITE)
    print_colored("• launcher.py - This main menu launcher", Colors.WHITE)
    print_colored("• modules/onedrive_manager.py - OneDrive management", Colors.WHITE)
    print_colored("• modules/telemetry_manager.py - Privacy & telemetry control", Colors.WHITE)
    print_colored("• modules/bloatware_manager.py - Bloatware removal", Colors.WHITE)
    print_colored("• modules/performance_manager.py - Performance optimization", Colors.WHITE)
    print_colored("• README.md - Complete documentation", Colors.WHITE)
    print_colored("• requirements.txt - Dependency information", Colors.WHITE)

    print_colored("\n" + "=" * 70, Colors.BLUE)

def run_script(script_name):
    """Run a Python script."""
    try:
        print_colored(f"\n{symbols.ROCKET} Launching {script_name}...", Colors.CYAN)
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print_colored(f"\n{symbols.CROSS} Error running {script_name}: {e}", Colors.RED)
    except FileNotFoundError:
        print_colored(f"\n{symbols.CROSS} Script not found: {script_name}", Colors.RED)
        print_colored("Make sure all files are in the same directory.", Colors.YELLOW)
    except KeyboardInterrupt:
        print_colored(f"\n{symbols.STOP}  {script_name} was interrupted by user.", Colors.YELLOW)

def run_module(module_path):
    """Run a Python module."""
    try:
        if not os.path.exists(module_path):
            print_colored(f"\n{symbols.CROSS} Module not found: {module_path}", Colors.RED)
            print_colored("Make sure the modules directory exists.", Colors.YELLOW)
            return

        print_colored(f"\n{symbols.ROCKET} Launching {module_path}...", Colors.CYAN)
        subprocess.run([sys.executable, module_path], check=True)
    except subprocess.CalledProcessError as e:
        print_colored(f"\n{symbols.CROSS} Error running {module_path}: {e}", Colors.RED)
    except FileNotFoundError:
        print_colored(f"\n{symbols.CROSS} Module not found: {module_path}", Colors.RED)
        print_colored("Make sure all module files are in the modules directory.", Colors.YELLOW)
    except KeyboardInterrupt:
        print_colored(f"\n{symbols.STOP}  {module_path} was interrupted by user.", Colors.YELLOW)

def check_admin():
    """Check if running as administrator."""
    try:
        subprocess.run(['net', 'session'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def request_admin():
    """Request administrator privileges by restarting the script with elevated permissions."""
    try:
        if sys.platform == 'win32':
            # Use ShellExecute to run the script as administrator
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                f'"{os.path.abspath(__file__)}"',
                None,
                1
            )
            return True
        else:
            print_colored("\n❌ Admin privilege request is only supported on Windows.", Colors.RED)
            return False
    except Exception as e:
        print_colored(f"\n❌ Failed to request admin privileges: {e}", Colors.RED)
        return False

def main():
    """Main launcher function."""
    # Enable ANSI colors for Windows terminals
    enable_ansi_colors()

    # Check admin status
    is_admin = check_admin()

    # If not running as admin, offer to restart with admin privileges
    if not is_admin:
        print_colored(f"\n{symbols.WARNING}  NOT RUNNING AS ADMINISTRATOR", Colors.BOLD + Colors.YELLOW)
        print_colored("This application requires administrator privileges for full functionality.", Colors.YELLOW)
        print_colored("\nOptions:", Colors.CYAN)
        print_colored(f"1. {symbols.KEY} Restart with Administrator privileges (Recommended)", Colors.GREEN)
        print_colored(f"2. {symbols.BLOCK} Continue without Administrator privileges (Limited functionality)", Colors.YELLOW)

        try:
            admin_choice = input(f"\n{Colors.BOLD}Choose option (1 or 2): {Colors.END}").strip()

            if admin_choice == '1':
                print_colored(f"\n{symbols.RECYCLE} Requesting administrator privileges...", Colors.CYAN)
                print_colored("Please click 'Yes' in the UAC dialog that appears.", Colors.YELLOW)

                if request_admin():
                    print_colored(f"{symbols.CHECK} Admin request sent. The application will restart with elevated privileges.", Colors.GREEN)
                    sys.exit(0)  # Exit current instance
                else:
                    print_colored(f"{symbols.CROSS} Failed to request admin privileges. Continuing with limited functionality.", Colors.RED)
            elif admin_choice == '2':
                print_colored(f"\n{symbols.WARNING}  Continuing with limited functionality...", Colors.YELLOW)
            else:
                print_colored(f"\n{symbols.CROSS} Invalid choice. Continuing with limited functionality...", Colors.RED)

        except KeyboardInterrupt:
            print_colored(f"\n\n{symbols.WAVE} Goodbye! Thanks for using Windows 11 Update Manager!", Colors.BOLD + Colors.CYAN)
            return

    while True:
        show_main_menu()

        if not is_admin:
            print_colored(f"\n{symbols.WARNING}  NOT RUNNING AS ADMINISTRATOR", Colors.BOLD + Colors.YELLOW)
            print_colored("Some features may not work properly. You can restart as Administrator anytime.", Colors.YELLOW)
        else:
            print_colored(f"\n{symbols.CHECK} RUNNING AS ADMINISTRATOR", Colors.BOLD + Colors.GREEN)
        
        try:
            if not is_admin:
                choice = input(f"\n{Colors.BOLD}Enter your choice (1-10, 0 to exit): {Colors.END}").strip()
            else:
                choice = input(f"\n{Colors.BOLD}Enter your choice (1-9, 0 to exit): {Colors.END}").strip()

            if choice == '1':
                run_script("disable_windows_updates.py")
            elif choice == '2':
                run_script("restore_windows_updates.py")
            elif choice == '3':
                run_script("comprehensive_restore.py")
            elif choice == '4':
                run_module("modules/onedrive_manager.py")
            elif choice == '5':
                run_module("modules/telemetry_manager.py")
            elif choice == '6':
                run_module("modules/bloatware_manager.py")
            elif choice == '7':
                run_module("modules/performance_manager.py")
            elif choice == '8':
                run_module("modules/activation_manager.py")
            elif choice == '9':
                show_information()
                input(f"\n{Colors.CYAN}Press Enter to return to main menu...{Colors.END}")
            elif choice == '10' and not is_admin:
                # Restart as Administrator option (only when not admin)
                print_colored(f"\n{symbols.RECYCLE} Requesting administrator privileges...", Colors.CYAN)
                print_colored("Please click 'Yes' in the UAC dialog that appears.", Colors.YELLOW)
                if request_admin():
                    print_colored(f"{symbols.CHECK} Admin request sent. The application will restart with elevated privileges.", Colors.GREEN)
                    sys.exit(0)
                else:
                    print_colored(f"{symbols.CROSS} Failed to request admin privileges.", Colors.RED)
            elif choice == '0':
                if not is_admin:
                    # Option 0 is "Exit" when not running as admin
                    print_colored("\n👋 Thank you for using Windows 11 System Manager!", Colors.BOLD + Colors.CYAN)
                    print_colored("Stay safe and keep your system optimized! 🛡️", Colors.GREEN)
                    break
                else:
                    # Option 0 is "Exit" when running as admin
                    print_colored("\n👋 Thank you for using Windows 11 System Manager!", Colors.BOLD + Colors.CYAN)
                    print_colored("Stay safe and keep your system optimized! 🛡️", Colors.GREEN)
                    break
            else:
                if not is_admin:
                    print_colored("\n❌ Invalid choice! Please enter 1-10 or 0.", Colors.RED)
                else:
                    print_colored("\n❌ Invalid choice! Please enter 1-9 or 0.", Colors.RED)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\n👋 Goodbye! Thanks for using Windows 11 Update Manager!", Colors.BOLD + Colors.CYAN)
            break
        except Exception as e:
            print_colored(f"\n❌ An error occurred: {str(e)}", Colors.RED)
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
