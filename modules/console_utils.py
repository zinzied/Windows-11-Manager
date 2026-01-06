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
import codecs

# 1. COLORAMA & ENCODING SETUP
OUTPUT_ENCODING = "utf-8"

if sys.platform == "win32":
    # Encourage UTF-8 everywhere
    os.environ["PYTHONIOENCODING"] = OUTPUT_ENCODING
    try:
        os.system("chcp 65001 >nul 2>&1")
    except Exception:
        pass

    try:
        sys.stdout.reconfigure(encoding=OUTPUT_ENCODING)
        sys.stderr.reconfigure(encoding=OUTPUT_ENCODING)
    except AttributeError:
        # Older Python versions
        try:
            sys.stdout = codecs.getwriter(OUTPUT_ENCODING)(sys.stdout.buffer, "strict")
            sys.stderr = codecs.getwriter(OUTPUT_ENCODING)(sys.stderr.buffer, "strict")
        except Exception:
            pass

# Import Colorama
try:
    from colorama import init, Fore, Style

    init(autoreset=True, convert=True, strip=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


# 2. COLOR DEFINITIONS
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
        UNDERLINE = ""
        END = Style.RESET_ALL
    else:
        # ANSI Escape Codes (Fallback)
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        END = "\033[0m"


# 3. SYMBOL DEFINITIONS
class Symbols:
    def __init__(self):
        # Allow disabling unicode via env var if users have issues
        if os.environ.get("NO_UNICODE"):
            self.use_unicode = False
            return

        # Prefer UTF-friendly consoles
        try:
            encoding = sys.stdout.encoding.lower() if sys.stdout.encoding else "ascii"
            self.use_unicode = "utf" in encoding
        except Exception:
            self.use_unicode = False

    def _pick(self, emoji, fallback):
        """Return emoji when supported, otherwise an ASCII fallback."""
        return emoji if self.use_unicode else fallback

    @property
    def SHIELD(self): return self._pick("🛡️", "[#]")
    @property
    def TARGET(self): return self._pick("🎯", "[O]")
    @property
    def GEAR(self): return self._pick("⚙️", "[*]")
    @property
    def TOOLS(self): return self._pick("🛠️", "[T]")
    @property
    def CLOUD(self): return self._pick("☁️", "[C]")
    @property
    def LOCK(self): return self._pick("🔒", "[L]")
    @property
    def TRASH(self): return self._pick("🗑️", "[D]")
    @property
    def LIGHTNING(self): return self._pick("⚡", "[!]")
    @property
    def INFO(self): return self._pick("ℹ️", "[i]")
    @property
    def CROSS(self): return self._pick("❌", "[X]")
    @property
    def CHECK(self): return self._pick("✅", "[V]")
    @property
    def WARNING(self): return self._pick("⚠️", "[!]")
    @property
    def ROCKET(self): return self._pick("🚀", "[>]")
    @property
    def STOP(self): return self._pick("🛑", "[S]")
    @property
    def WAVE(self): return self._pick("👋", "[-]")
    @property
    def RECYCLE(self): return self._pick("♻️", "[@]")
    @property
    def BLOCK(self): return self._pick("⛔", "[/]")
    @property
    def KEY(self): return self._pick("🔑", "[K]")
    @property
    def FOLDER(self): return self._pick("📁", "[F]")
    @property
    def BOOK(self): return self._pick("📘", "[B]")
    @property
    def GLOBE(self): return self._pick("🌐", "[NET]")
    @property
    def HARDWARE(self): return self._pick("💾", "[HW]")
    @property
    def CONTROL(self): return self._pick("🎮", "[GAME]")
    @property
    def DOWNLOAD(self): return self._pick("📦", "[PKG]")
    @property
    def BULLET(self): return self._pick("•", "-")
    @property
    def PROMPT(self): return self._pick("👉", ">")


# Global Symbols Instance
matches = Symbols()


# 4. PRINT HELPERS
def print_colored(text, color=Colors.WHITE):
    """Print text with color."""
    try:
        print(f"{color}{text}", flush=True)
    except Exception:
        try:
            print(text.encode("ascii", "replace").decode("ascii"))
        except Exception:
            pass


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
    os.system("cls" if os.name == "nt" else "clear")
