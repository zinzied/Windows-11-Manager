#!/usr/bin/env python3
"""
DNS Manager Module for Windows 11 Update Manager
Allows quick switching between common DNS providers.

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

def get_active_adapter():
    """Get the name of the currently active network adapter."""
    try:
        # PowerShell command to get the interface alias of the connected adapter
        cmd = 'powershell -Command "Get-NetAdapter | Where-Object Status -eq Up | Select-Object -ExpandProperty Name"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            adapters = result.stdout.strip().split('\n')
            if adapters and adapters[0]:
                return adapters[0].strip()
    except Exception as e:
        print_error(f"Error checking adapters: {e}")
    return "Ethernet" # Fallback

def set_dns(primary, secondary, name):
    """Set DNS servers for the active adapter."""
    adapter = get_active_adapter()
    print_info(f"Setting {name} DNS for adapter: {adapter}...")
    
    try:
        # Set primary DNS
        cmd_primary = f'netsh interface ip set dns name="{adapter}" source=static addr={primary} register=primary'
        subprocess.run(cmd_primary, shell=True, check=True, stdout=subprocess.DEVNULL)
        
        # Set secondary DNS
        cmd_secondary = f'netsh interface ip add dns name="{adapter}" addr={secondary} index=2'
        subprocess.run(cmd_secondary, shell=True, check=False, stdout=subprocess.DEVNULL) # Might fail if already set, check=False
        
        print_success(f"DNS changed to {name} ({primary}, {secondary})")
        
        # Flush DNS to ensure immediate effect
        subprocess.run('ipconfig /flushdns', shell=True, stdout=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to set DNS: {e}")
        print_info("Make sure you are running as Administrator.")

def reset_to_dhcp():
    """Reset DNS to automatic (DHCP)."""
    adapter = get_active_adapter()
    print_info(f"Reseting DNS to Automatic (DHCP) for: {adapter}...")
    
    try:
        cmd = f'netsh interface ip set dns name="{adapter}" source=dhcp'
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL)
        
        print_success("DNS reset to Automatic (DHCP).")
        subprocess.run('ipconfig /flushdns', shell=True, stdout=subprocess.DEVNULL)
        
    except subprocess.CalledProcessError:
        print_error("Failed to reset DNS.")

def check_current_dns():
    """Show current DNS settings."""
    adapter = get_active_adapter()
    print_header(f"Current DNS Settings ({adapter})")
    
    try:
        cmd = f'powershell -Command "Get-DnsClientServerAddress -InterfaceAlias \'{adapter}\' | Select-Object -ExpandProperty ServerAddresses"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            dns_servers = result.stdout.strip().split('\n')
                if dns_servers and dns_servers[0]:
                    for dns in dns_servers:
                        if dns.strip():
                            print_colored(f"  {symbols.BULLET} {dns.strip()}", Colors.YELLOW)
                else:
                    print_colored(f"  {symbols.BULLET} Automatic (DHCP) / Unknown", Colors.WHITE)
        else:
            # Fallback to netsh
            os.system(f'netsh interface ip show dns "{adapter}"')
            
    except Exception:
        pass

def show_menu():
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored(f"{symbols.CLOUD}  DNS SWITCHER", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    print_colored(f"\n{symbols.TARGET} Choose a DNS Provider:", Colors.BOLD + Colors.CYAN)
    print_colored(f"\n1. {symbols.GLOBE} Google DNS (8.8.8.8)", Colors.GREEN)
    print_colored("   - Fast, reliable, standard choice", Colors.WHITE)
    print_colored(f"2. {symbols.CLOUD}  Cloudflare DNS (1.1.1.1)", Colors.MAGENTA)
    print_colored("   - Focused on privacy and speed", Colors.WHITE)
    print_colored(f"3. {symbols.SHIELD}  OpenDNS (208.67.222.222)", Colors.YELLOW)
    print_colored("   - Good for phishing protection", Colors.WHITE)
    print_colored(f"4. {symbols.RECYCLE} Reset to Automatic (DHCP)", Colors.BLUE)
    print_colored("   - Use your ISP's default DNS", Colors.WHITE)
    print_colored(f"5. {symbols.INFO} Check Current DNS", Colors.CYAN)
    print_colored(f"6. {symbols.WAVE} Return to Main Menu", Colors.CYAN)

def main():
    while True:
        show_menu()
        try:
            choice = input(f"\n{Colors.BOLD}Enter your choice (1-6): {Colors.END}").strip()
            
            if choice == '1':
                set_dns("8.8.8.8", "8.8.4.4", "Google")
            elif choice == '2':
                set_dns("1.1.1.1", "1.0.0.1", "Cloudflare")
            elif choice == '3':
                set_dns("208.67.222.222", "208.67.220.220", "OpenDNS")
            elif choice == '4':
                reset_to_dhcp()
            elif choice == '5':
                check_current_dns()
            elif choice == '6':
                break
            else:
                print_error("Invalid choice! Please enter 1-6.")
            
            if choice in ['1', '2', '3', '4', '5']:
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                
        except KeyboardInterrupt:
            print_colored("\n\nReturning to main menu...", Colors.CYAN)
            break
        except Exception as e:
            print_error(f"An error occurred: {e}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print_warning("Warning: Admin privileges required to change DNS settings.")
    main()
