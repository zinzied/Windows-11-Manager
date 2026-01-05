#!/usr/bin/env python3
"""
Console Utilities for Windows 11 Update Manager
Provides consistent color output, symbol handling, and encoding fixes for Windows consoles.

Author: Zied Boughdir
GitHub: https://github.com/zinzied
Year: 2025
"""

import sys
import os
import platform
import ctypes

# 1. ENCODING FIX FOR WINDOWS
if sys.platform == 'win32':
    # Force UTF-8 encoding for stdout/stderr
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    try:
        # Command equivalent to 'chcp 65001' to set console code page to UTF-8
        # This is CRITICAL for emojis/symbols to show up on Windows 10
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass
    
    # Enable ANSI escape sequences (Virtual Terminal Processing)
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11) # STD_OUTPUT_HANDLE
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        mode.value |= 4 # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        kernel32.SetConsoleMode(handle, mode)
    except:
        pass

# 2. COLOR DEFINITIONS
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

class Colors:
    if COLORAMA_AVAILABLE:
        RED = Fore.RED + Style.BRIGHT
        GREEN = Fore.GREEN + Style.BRIGHT
        YELLOW = Fore.YELLOW + Style.BRIGHT
        BLUE = Fore.BLUE + Style.BRIGHT
        MAGENTA = Fore.MAGENTA + Style.BRIGHT
        CYAN = Fore.CYAN + Style.BRIGHT
        WHITE = Fore.WHITE + Style.BRIGHT
        BOLD = Style.BRIGHT
        UNDERLINE = ''
        END = Style.RESET_ALL
    else:
        # ANSI Escape Codes
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

# 3. SYMBOL DEFINITIONS
class Symbols:
    # Safely return symbol or fallback
    
    def __init__(self):
        # We assume Unicode is supported because we forced chcp 65001
        # If user still has issues, we can add a toggle here.
        self.use_unicode = True

    @property
    def SHIELD(self): return "🛡️" if self.use_unicode else "[#]"
    @property
    def TARGET(self): return "🎯" if self.use_unicode else "[O]"
    @property
    def GEAR(self): return "🔧" if self.use_unicode else "[*]"
    @property
    def TOOLS(self): return "🛠️" if self.use_unicode else "[T]"
    @property
    def CLOUD(self): return "☁️" if self.use_unicode else "[C]"
    @property
    def LOCK(self): return "🔒" if self.use_unicode else "[L]"
    @property
    def TRASH(self): return "🗑️" if self.use_unicode else "[D]"
    @property
    def LIGHTNING(self): return "⚡" if self.use_unicode else "[!]"
    @property
    def INFO(self): return "ℹ️" if self.use_unicode else "[i]"
    @property
    def CROSS(self): return "❌" if self.use_unicode else "[X]"
    @property
    def CHECK(self): return "✅" if self.use_unicode else "[V]"
    @property
    def WARNING(self): return "⚠️" if self.use_unicode else "[!]"
    @property
    def ROCKET(self): return "🚀" if self.use_unicode else "[>]"
    @property
    def STOP(self): return "⏹️" if self.use_unicode else "[S]"
    @property
    def WAVE(self): return "👋" if self.use_unicode else "[-]"
    @property
    def RECYCLE(self): return "🔄" if self.use_unicode else "[@]"
    @property
    def BLOCK(self): return "🚫" if self.use_unicode else "[/]"
    @property
    def KEY(self): return "🔑" if self.use_unicode else "[K]"
    @property
    def FOLDER(self): return "📁" if self.use_unicode else "[F]"
    @property
    def BOOK(self): return "📖" if self.use_unicode else "[B]"

# Global Symbols Instance
matches = Symbols()

# 4. PRINT HELPERS
def print_colored(text, color=Colors.WHITE):
    """Print text with color, handling ANSI setup implicitly."""
    if COLORAMA_AVAILABLE:
        print(f"{color}{text}")
    else:
        print(f"{color}{text}{Colors.END}")

def print_header(title):
    print_colored(f"\n{'=' * 60}", Colors.CYAN)
    print_colored(f"{matches.GEAR}  {title}", Colors.BOLD + Colors.CYAN)
    print_colored(f"{'=' * 60}", Colors.CYAN)

def print_success(message):
    print_colored(f"{matches.CHECK} {message}", Colors.GREEN)

def print_error(message):
    print_colored(f"{matches.CROSS} {message}", Colors.RED)

def print_warning(message):
    print_colored(f"{matches.WARNING}  {message}", Colors.YELLOW)

def print_info(message):
    print_colored(f"{matches.INFO}  {message}", Colors.BLUE)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
