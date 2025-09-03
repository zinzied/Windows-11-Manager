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
import json
import re
import platform
import ctypes
from datetime import datetime

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
            self.CERTIFICATE = "📜"
            self.LICENSE = "📄"
            self.HARDWARE = "💻"
            self.GLOBE = "🌐"
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
            self.CERTIFICATE = "[CERT]"
            self.LICENSE = "[LIC]"
            self.HARDWARE = "[HW]"
            self.GLOBE = "[GLOBE]"

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

def print_header():
    """Print the header for this module."""
    print_colored("\n" + "=" * 70, Colors.MAGENTA)
    print_colored(f"{symbols.KEY}  WINDOWS ACTIVATION MANAGER - WINDOWS 10 & 11", Colors.BOLD + Colors.MAGENTA)
    print_colored("    Created by Zied Boughdir - 2025", Colors.CYAN)
    print_colored("    GitHub: https://github.com/zinzied", Colors.BLUE)
    print_colored("=" * 70, Colors.MAGENTA)
    print_colored("    Manage Windows Activation Status", Colors.CYAN)
    print_colored("=" * 70, Colors.MAGENTA)

def check_admin():
    """Check if running as administrator."""
    try:
        subprocess.run(['net', 'session'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_activation_status():
    """Get the current Windows activation status."""
    try:
        # Use slmgr.vbs to get activation status
        # Instead of capturing output, redirect to a temp file to avoid encoding issues
        import tempfile

        # Create a temporary file to store the output
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dli'], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        # Parse the output to extract key information
        status = {
            'licensed': False,
            'product_key': None,
            'description': None,
            'license_status': None,
            'remaining_time': None
        }

        lines = output.split('\n')
        for line in lines:
            if 'License Status' in line:
                status['license_status'] = line.split(':')[1].strip() if ':' in line else 'Unknown'
                if 'Licensed' in status['license_status']:
                    status['licensed'] = True
            elif 'Product Key' in line:
                status['product_key'] = line.split(':')[1].strip() if ':' in line else 'Not available'
            elif 'Description' in line:
                status['description'] = line.split(':')[1].strip() if ':' in line else 'Not available'
            elif 'Remaining Windows' in line and 'rearm' not in line.lower():
                status['remaining_time'] = line.split(':')[1].strip() if ':' in line else 'Unknown'

        return status
    except subprocess.CalledProcessError as e:
        print_colored(f"\n{symbols.CROSS} Error checking activation status: {e}", Colors.RED)
        return None
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Unexpected error checking activation status: {e}", Colors.RED)
        return None

def display_activation_status():
    """Display the current Windows activation status."""
    print_colored(f"\n{symbols.INFO}  CHECKING ACTIVATION STATUS", Colors.BOLD + Colors.CYAN)

    status = get_activation_status()
    if not status:
        return

    print_colored("\n" + "=" * 50, Colors.BLUE)
    print_colored(f"{symbols.LICENSE}  ACTIVATION DETAILS", Colors.BOLD + Colors.BLUE)
    print_colored("=" * 50, Colors.BLUE)

    if status['licensed']:
        print_colored(f"{symbols.CHECK} License Status: {status['license_status']}", Colors.GREEN)
        print_colored(f"{symbols.CERTIFICATE} Product Key: {status['product_key'] if status['product_key'] else 'Not available'}", Colors.WHITE)
        print_colored(f"{symbols.INFO} Description: {status['description'] if status['description'] else 'Not available'}", Colors.WHITE)

        if status['remaining_time']:
            print_colored(f"{symbols.GLOBE} Remaining Time: {status['remaining_time']}", Colors.CYAN)
    else:
        print_colored(f"{symbols.CROSS} License Status: {status['license_status']}", Colors.RED)
        print_colored(f"{symbols.WARNING} Windows is not activated", Colors.YELLOW)
        print_colored(f"{symbols.INFO} Description: {status['description'] if status['description'] else 'Not available'}", Colors.WHITE)

def validate_product_key(product_key):
    """
    Validate the format of a Windows product key.
    
    Windows product keys are typically in one of these formats:
    - XXXXX-XXXXX-XXXXX-XXXXX-XXXXX (25 characters, 5 groups of 5)
    - XXXXXXXXX-XXXXXXXXX-XXXXXXXXX-XXXXXXXXX-XXXXXXXXX (45 characters, 5 groups of 9)
    """
    if not product_key:
        return False, "Product key cannot be empty."
    
    # Remove any whitespace
    key = product_key.strip().upper()
    
    # Check for common invalid inputs
    if len(key) < 10:  # Too short to be a valid key
        return False, "Product key is too short. Windows product keys are typically 25 or 29 characters."
    
    if key.isdigit() and len(key) < 10:  # Just a number like "2"
        return False, "Invalid product key format. Please enter a valid Windows product key (e.g., XXXXX-XXXXX-XXXXX-XXXXX-XXXXX)."
    
    # Check for standard Windows key format (25 characters with dashes)
    if len(key) == 29 and key.count('-') == 4:
        parts = key.split('-')
        if len(parts) == 5 and all(len(part) == 5 for part in parts):
            # Check if all parts contain only alphanumeric characters
            if all(part.replace('-', '').isalnum() for part in parts):
                return True, "Valid product key format."
    
    # Check for KMS/MAK key format (might be different)
    if len(key) >= 25 and '-' in key:
        # Allow other dash-separated formats
        parts = key.split('-')
        if len(parts) >= 4:  # At least 4 parts
            return True, "Product key format appears valid."
    
    # If no dashes, check if it's 25 characters of alphanumeric
    if len(key) == 25 and key.isalnum():
        return True, "Product key format appears valid."
    
    return False, "Invalid product key format. Windows product keys should be in format XXXXX-XXXXX-XXXXX-XXXXX-XXXXX."

def activate_windows(product_key=None):
    """Attempt to activate Windows with a product key."""
    print_colored(f"\n{symbols.ROCKET}  ACTIVATING WINDOWS", Colors.BOLD + Colors.CYAN)

    if not product_key:
        print_colored(f"\n{symbols.INFO} Please enter your Windows product key:", Colors.CYAN)
        print_colored(f"Example format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX", Colors.WHITE)
        product_key = input(f"{Colors.BOLD}Enter your Windows product key: {Colors.END}").strip()
        
        if not product_key:
            print_colored(f"\n{symbols.CROSS} No product key provided.", Colors.RED)
            return False

    # Validate the product key format
    is_valid, message = validate_product_key(product_key)
    if not is_valid:
        print_colored(f"\n{symbols.CROSS} {message}", Colors.RED)
        print_colored(f"{symbols.INFO} Please ensure you have a valid Windows product key.", Colors.YELLOW)
        print_colored(f"{symbols.INFO} You can find your product key on your Windows installation media, email receipt, or Certificate of Authenticity.", Colors.YELLOW)
        return False
    
    print_colored(f"\n{symbols.CHECK} Product key format validated.", Colors.GREEN)

    try:
        import tempfile

        # Use slmgr.vbs to install the product key
        print_colored(f"\n{symbols.INFO} Installing product key...", Colors.CYAN)

        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/ipk', product_key], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        if result.returncode == 0:
            print_colored(f"{symbols.CHECK} Product key installed successfully.", Colors.GREEN)

            # Now try to activate
            print_colored(f"\n{symbols.INFO} Attempting to activate Windows...", Colors.CYAN)

            with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
                temp_file_path = temp_file.name

            # Run the command and redirect output to our temp file in binary mode
            with open(temp_file_path, 'wb') as temp_output:
                result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/ato'], 
                                      stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

            # Read the output from the temp file in binary mode and decode with cp1252
            with open(temp_file_path, 'rb') as temp_file:
                output = temp_file.read().decode('cp1252', errors='replace')

            # Clean up the temp file
            os.unlink(temp_file_path)

            if result.returncode == 0:
                print_colored(f"{symbols.CHECK} Windows activation completed successfully!", Colors.GREEN)
                return True
            else:
                print_colored(f"{symbols.CROSS} Windows activation failed.", Colors.RED)
                print_colored(f"Output: {output}", Colors.YELLOW)
                return False
        else:
            print_colored(f"{symbols.CROSS} Failed to install product key.", Colors.RED)
            print_colored(f"Output: {output}", Colors.YELLOW)
            return False

    except subprocess.CalledProcessError as e:
        # Provide more specific error messages based on return codes
        error_code = e.returncode
        if error_code == 3221549136:  # 0xC0000130
            print_colored(f"\n{symbols.CROSS} Invalid product key format or characters.", Colors.RED)
            print_colored(f"{symbols.INFO} Please check that your product key is entered correctly.", Colors.YELLOW)
            print_colored(f"{symbols.INFO} Windows product keys should be in format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX", Colors.YELLOW)
        elif error_code == -1073422315:  # 0xC004F015
            print_colored(f"\n{symbols.CROSS} Product key is not valid for this version of Windows.", Colors.RED)
            print_colored(f"{symbols.INFO} Make sure the product key matches your Windows edition.", Colors.YELLOW)
        elif error_code == -1073418194:  # 0xC004F02E  
            print_colored(f"\n{symbols.CROSS} Product key format is invalid.", Colors.RED)
            print_colored(f"{symbols.INFO} Please verify the product key and try again.", Colors.YELLOW)
        else:
            print_colored(f"\n{symbols.CROSS} Error activating Windows (Code: {error_code}): {e}", Colors.RED)
            print_colored(f"{symbols.INFO} This may be due to network issues, invalid key, or system restrictions.", Colors.YELLOW)
        
        print_colored(f"\n{symbols.BOOK} Troubleshooting Tips:", Colors.BOLD + Colors.CYAN)
        print_colored(f"• Ensure you're connected to the internet", Colors.WHITE)
        print_colored(f"• Verify the product key is correct and unused", Colors.WHITE)
        print_colored(f"• Check that the key matches your Windows edition", Colors.WHITE)
        print_colored(f"• Try running Windows Update first", Colors.WHITE)
        return False
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Unexpected error activating Windows: {e}", Colors.RED)
        return False

def check_activation_details():
    """Show detailed activation information."""
    print_colored(f"\n{symbols.INFO}  DETAILED ACTIVATION INFORMATION", Colors.BOLD + Colors.CYAN)

    try:
        import tempfile

        # Get detailed information about the license
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dlv'], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        print_colored("\n" + "=" * 50, Colors.BLUE)
        print_colored(f"{symbols.CERTIFICATE}  LICENSE DETAILS", Colors.BOLD + Colors.BLUE)
        print_colored("=" * 50, Colors.BLUE)
        print_colored(output, Colors.WHITE)

        # Get installation ID
        print_colored("\n" + "=" * 50, Colors.BLUE)
        print_colored(f"{symbols.HARDWARE}  INSTALLATION ID", Colors.BOLD + Colors.BLUE)
        print_colored("=" * 50, Colors.BLUE)

        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/dti'], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        print_colored(output, Colors.WHITE)

        return True

    except subprocess.CalledProcessError as e:
        print_colored(f"\n{symbols.CROSS} Error getting activation details: {e}", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Unexpected error getting activation details: {e}", Colors.RED)
        return False

def reset_activation():
    """Reset Windows activation (rearm)."""
    print_colored(f"\n{symbols.WARNING}  RESET WINDOWS ACTIVATION (REARM)", Colors.BOLD + Colors.YELLOW)
    print_colored(f"{symbols.WARNING} This will reset the activation status and may require reactivation.", Colors.YELLOW)
    print_colored(f"{symbols.WARNING} This can only be done a limited number of times (typically 3 times).", Colors.YELLOW)

    confirm = input(f"\n{Colors.BOLD}Are you sure you want to reset activation? (y/N): {Colors.END}").strip().lower()

    if confirm != 'y':
        print_colored(f"\n{symbols.CHECK} Activation reset cancelled.", Colors.GREEN)
        return False

    try:
        import tempfile

        # Use slmgr.vbs to rearm Windows
        print_colored(f"\n{symbols.INFO} Resetting activation...", Colors.CYAN)

        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as temp_file:
            temp_file_path = temp_file.name

        # Run the command and redirect output to our temp file in binary mode
        with open(temp_file_path, 'wb') as temp_output:
            result = subprocess.run(['cscript', '//Nologo', 'C:\\Windows\\System32\\slmgr.vbs', '/rearm'], 
                                  stdout=temp_output, stderr=subprocess.DEVNULL, check=True)

        # Read the output from the temp file in binary mode and decode with cp1252
        with open(temp_file_path, 'rb') as temp_file:
            output = temp_file.read().decode('cp1252', errors='replace')

        # Clean up the temp file
        os.unlink(temp_file_path)

        if result.returncode == 0:
            print_colored(f"{symbols.CHECK} Windows activation has been reset successfully!", Colors.GREEN)
            print_colored(f"{symbols.INFO} You will need to reactivate Windows.", Colors.CYAN)
            print_colored(f"{symbols.INFO} Please restart your computer for changes to take effect.", Colors.CYAN)
            return True
        else:
            print_colored(f"{symbols.CROSS} Failed to reset Windows activation.", Colors.RED)
            print_colored(f"Output: {output}", Colors.YELLOW)
            return False

    except subprocess.CalledProcessError as e:
        print_colored(f"\n{symbols.CROSS} Error resetting activation: {e}", Colors.RED)
        return False
    except Exception as e:
        print_colored(f"\n{symbols.CROSS} Unexpected error resetting activation: {e}", Colors.RED)
        return False

def show_activation_help():
    """Show help information about Windows activation."""
    print_colored(f"\n{symbols.BOOK}  WINDOWS ACTIVATION HELP", Colors.BOLD + Colors.CYAN)

    print_colored("\n" + "=" * 70, Colors.BLUE)
    print_colored(f"{symbols.INFO} UNDERSTANDING WINDOWS ACTIVATION", Colors.BOLD + Colors.BLUE)
    print_colored("=" * 70, Colors.BLUE)

    print_colored(f"\n{symbols.LICENSE} WHAT IS WINDOWS ACTIVATION?", Colors.BOLD + Colors.WHITE)
    print_colored("Windows activation is a validation process that verifies your Windows operating system is genuine and properly licensed.", Colors.WHITE)
    print_colored("Activation helps ensure that your PC is running genuine Windows software and not counterfeit or pirated software.", Colors.WHITE)

    print_colored(f"\n{symbols.KEY} HOW TO ACTIVATE WINDOWS", Colors.BOLD + Colors.WHITE)
    print_colored("1. Purchase a valid Windows license from Microsoft or an authorized retailer", Colors.WHITE)
    print_colored("2. Use the product key that came with your Windows purchase", Colors.WHITE)
    print_colored("3. Run this tool and select 'Activate Windows'", Colors.WHITE)
    print_colored("4. Enter your product key when prompted", Colors.WHITE)
    print_colored("5. Follow the on-screen instructions to complete activation", Colors.WHITE)

    print_colored(f"\n{symbols.LICENSE} PRODUCT KEY FORMATS", Colors.BOLD + Colors.WHITE)
    print_colored("• Standard Format: XXXXX-XXXXX-XXXXX-XXXXX-XXXXX (25 characters)", Colors.WHITE)
    print_colored("• Example: 7B9N3-2V7C8-JQKMG-X7DQT-BHBB6", Colors.CYAN)
    print_colored("• Characters: Letters (A-Z) and Numbers (0-9) only", Colors.WHITE)
    print_colored("• Dashes: Required every 5 characters", Colors.WHITE)
    print_colored("• Case: Not case-sensitive (automatically converted to uppercase)", Colors.WHITE)

    print_colored(f"\n{symbols.CERTIFICATE} TYPES OF WINDOWS LICENSES", Colors.BOLD + Colors.WHITE)
    print_colored("• Retail License: Can be transferred to different computers", Colors.WHITE)
    print_colored("• OEM License: Tied to the original hardware it came with", Colors.WHITE)
    print_colored("• Volume License: For organizations with multiple computers", Colors.WHITE)
    print_colored("• Digital License: Automatically assigned after first activation", Colors.WHITE)

    print_colored(f"\n{symbols.WARNING} IMPORTANT NOTES", Colors.BOLD + Colors.YELLOW)
    print_colored("• This tool only works on genuine Windows installations", Colors.YELLOW)
    print_colored("• Using invalid or counterfeit product keys is against Microsoft's terms", Colors.YELLOW)
    print_colored("• The reset option (rearm) can only be used a limited number of times", Colors.YELLOW)
    print_colored("• Some editions of Windows (like Home) cannot be activated with KMS or MAK keys", Colors.YELLOW)

    print_colored(f"\n{symbols.CHECK} ACTIVATION TROUBLESHOOTING", Colors.BOLD + Colors.GREEN)
    print_colored("• Ensure you're connected to the internet", Colors.WHITE)
    print_colored("• Check that your system clock is set correctly", Colors.WHITE)
    print_colored("• Make sure you're using the correct product key for your Windows edition", Colors.WHITE)
    print_colored("• Verify the product key hasn't been used on another computer (if retail)", Colors.WHITE)
    print_colored("• Try running Windows Update first to ensure system compatibility", Colors.WHITE)
    print_colored("• If using a Volume License key, ensure your organization allows activation", Colors.WHITE)
    print_colored("• For persistent issues, use Microsoft's automated phone activation", Colors.WHITE)
    print_colored("• If issues persist, contact Microsoft Support", Colors.WHITE)

    print_colored(f"\n{symbols.WARNING} COMMON ERROR SOLUTIONS", Colors.BOLD + Colors.YELLOW)
    print_colored("• 'Invalid product key': Check format and ensure key matches Windows edition", Colors.WHITE)
    print_colored("• 'Key already in use': Key may be installed on another computer", Colors.WHITE)
    print_colored("• 'Cannot connect to activation server': Check internet connection", Colors.WHITE)
    print_colored("• 'Hardware change detected': May need to reactivate after major hardware changes", Colors.WHITE)

    print_colored("\n" + "=" * 70, Colors.BLUE)

def show_main_menu():
    """Display the main menu for activation manager."""
    print_header()
    print_colored(f"\n{symbols.TARGET} What would you like to do?", Colors.BOLD + Colors.CYAN)

    print_colored(f"\n{symbols.INFO} ACTIVATION STATUS:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"1. {symbols.INFO}  Check Activation Status", Colors.BLUE)
    print_colored("   └─ View current Windows activation status and details", Colors.WHITE)

    print_colored(f"\n{symbols.KEY} ACTIVATION TOOLS:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"2. {symbols.KEY}  Activate Windows", Colors.GREEN)
    print_colored("   └─ Enter a product key to activate Windows", Colors.WHITE)
    print_colored(f"3. {symbols.CERTIFICATE} Check License Details", Colors.CYAN)
    print_colored("   └─ View detailed information about your Windows license", Colors.WHITE)

    print_colored(f"\n{symbols.WARNING} ADVANCED OPTIONS:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"4. {symbols.RECYCLE} Reset Activation (Rearm)", Colors.YELLOW)
    print_colored("   └─ Reset activation status (limited uses, requires reactivation)", Colors.WHITE)

    print_colored(f"\n{symbols.BOOK} HELP & INFO:", Colors.BOLD + Colors.MAGENTA)
    print_colored(f"5. {symbols.BOOK}  Activation Help", Colors.BLUE)
    print_colored("   └─ Learn about Windows activation and troubleshooting", Colors.WHITE)
    print_colored(f"0. {symbols.CROSS} Return to Main Menu", Colors.RED)

    print_colored("\n" + "=" * 70, Colors.MAGENTA)

def main():
    """Main function for activation manager."""
    # Enable ANSI colors for Windows terminals
    enable_ansi_colors()

    # Check admin status
    is_admin = check_admin()

    if not is_admin:
        print_colored(f"\n{symbols.WARNING}  NOT RUNNING AS ADMINISTRATOR", Colors.BOLD + Colors.YELLOW)
        print_colored("This application requires administrator privileges for activation.", Colors.YELLOW)
        print_colored("Please restart as Administrator.", Colors.YELLOW)
        input(f"\n{Colors.CYAN}Press Enter to return to main menu...{Colors.END}")
        return

    while True:
        show_main_menu()

        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-5, 0 to exit): {Colors.END}").strip()

            if choice == '1':
                display_activation_status()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '2':
                activate_windows()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '3':
                check_activation_details()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '4':
                reset_activation()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '5':
                show_activation_help()
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == '0':
                print_colored(f"\n{symbols.WAVE} Returning to main menu...", Colors.CYAN)
                break
            else:
                print_colored("\n{symbols.CROSS} Invalid choice! Please enter 1-5 or 0.", Colors.RED)
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

        except KeyboardInterrupt:
            print_colored(f"\n\n{symbols.WAVE} Returning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_colored(f"\n{symbols.CROSS} An error occurred: {str(e)}", Colors.RED)
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
