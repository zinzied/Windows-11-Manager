# 🛡️ Windows 11 System Manager - Take Back Control of Your PC!

<div align="center">

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support%20my%20work-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/Zied)

**Created with ❤️ by Zied Boughdir**
**GitHub:** [https://github.com/zinzied](https://github.com/zinzied) | **Year:** 2025

*Tired of Windows 11 doing things you don't want? This toolkit puts YOU back in control!*

</div>

---

## 👋 Hey there, fellow Windows user!

Are you frustrated with Windows 11's constant updates, privacy invasions, and bloatware? I feel your pain! That's why I created this comprehensive toolkit to help you reclaim control over your own computer.

This isn't just another script collection - it's a **complete system management solution** built by someone who understands the daily struggles of Windows 11 users. Whether you're a privacy-conscious user, a performance enthusiast, or just someone who wants their computer to behave the way THEY want it to, this tool is for you!

## 🤔 Why I Built This (And Why You Need It)

Let me be honest - Windows 11 can be incredibly frustrating. Microsoft seems to think they know better than you about how YOUR computer should work. Sound familiar? Here are the problems I was facing (and I bet you are too):

- 😤 **Forced updates** that break things or restart your computer at the worst possible moment
- 🕵️ **Privacy invasion** with constant telemetry and data collection
- 🗑️ **Bloatware everywhere** - Xbox apps, Cortana, widgets you never asked for
- 🐌 **Sluggish performance** from unnecessary background services
- ☁️ **OneDrive integration** forced down your throat

So I decided to do something about it. This toolkit is the result of months of research, testing, and refinement. It's not just about disabling things - it's about giving you **intelligent control** over your system.

## 🎯 What This Toolkit Actually Does For You

### 🔄 **Update Control** - Stop the Madness
- **No more surprise restarts** during important work
- **Block problematic updates** that break your workflow
- **Update when YOU want to**, not when Microsoft decides
- **Complete restore capability** when you need updates back

### 🔒 **Privacy Protection** - Your Data Stays Yours
- **Stop Microsoft from spying** on your activities
- **Disable advertising tracking** and targeted ads
- **Control location access** and app permissions
- **Remove annoying feedback requests** once and for all

### 🗑️ **Bloatware Elimination** - Clean House
- **Remove useless apps** you never wanted (Xbox, Cortana, etc.)
- **Disable background services** that slow you down
- **Clean up Start Menu** from Microsoft's "suggestions"
- **Reclaim disk space** and system resources

### ⚡ **Performance Boost** - Make It Fast Again
- **Optimize visual effects** for speed over eye candy
- **Disable resource-hungry services** you don't need
- **Improve boot times** and system responsiveness
- **Monitor system performance** to see the difference

### ☁️ **OneDrive Freedom** - Your Files, Your Choice
- **Completely remove OneDrive** if you don't want it
- **Stop forced cloud sync** of your personal files
- **Clean up File Explorer** from OneDrive integration
- **Use the cloud storage YOU choose**

2. **Professional/Enterprise Environments**
   - Need for controlled update deployment schedules
   - Testing requirements before rolling out updates
   - Maintaining specific system configurations for production environments

3. **Limited Bandwidth/Data Constraints**
   - Metered internet connections with data caps
   - Slow internet connections where large updates disrupt work
   - Remote locations with unreliable internet access

4. **Gaming and Performance**
   - Preventing updates during critical gaming sessions or live streams
   - Avoiding performance impacts from background update processes
   - Maintaining optimal system performance for resource-intensive applications

5. **Legacy Software Dependencies**
   - Running older software that may break with newer Windows versions
   - Maintaining compatibility with specialized hardware or industrial equipment
   - Preserving specific system configurations required by legacy applications

6. **Development and Testing**
   - Creating stable development environments
   - Testing software on specific Windows versions
   - Preventing unexpected changes during development cycles

7. **System Control and Privacy**
   - Maintaining full control over what gets installed on the system
   - Avoiding unwanted feature changes or UI modifications
   - Preventing automatic installation of optional features or apps

### ⚖️ **Important Considerations:**

**Security Trade-offs**: Disabling updates means missing important security patches. Consider:
- Only disable updates temporarily when necessary
- Manually install critical security updates when possible
- Re-enable updates periodically to stay protected
- Use additional security measures (antivirus, firewall) when updates are disabled

**Best Practices**:
- Create system restore points before disabling updates
- Keep the restore script readily available
- Monitor Microsoft security bulletins manually
- Consider selective update installation rather than complete disabling

## Files Structure

```
Windows-11-System-Manager/
├── launcher.py                    # Main menu launcher
├── disable_windows_updates.py     # Windows Update disable script
├── restore_windows_updates.py     # Windows Update restore script
├── modules/
│   ├── onedrive_manager.py        # OneDrive management
│   ├── telemetry_manager.py       # Privacy & telemetry control
│   ├── bloatware_manager.py       # Bloatware removal
│   └── performance_manager.py     # Performance optimization
├── README.md                      # This documentation
└── requirements.txt               # Dependencies
```

## Features Overview

### 🔄 **Update Management**
- **Disable Updates**: Stop services, modify registry, disable tasks, block URLs
- **Restore Updates**: Re-enable all Windows Update functionality
- **Granular Control**: Choose specific components to disable/enable

### ☁️ **OneDrive Management**
- **Complete Disable**: Stop processes, disable services, modify registry
- **Startup Prevention**: Remove from startup locations
- **Registry Cleanup**: Clean OneDrive-related registry entries
- **File Explorer Integration**: Remove OneDrive from File Explorer

### 🔒 **Privacy & Telemetry Control**
- **Telemetry Disable**: Stop diagnostic data collection
- **Advertising ID**: Disable targeted advertising
- **Location Tracking**: Control location access
- **Activity History**: Disable timeline and activity tracking
- **Feedback**: Remove Windows feedback notifications

### 🗑️ **Bloatware Removal**
- **Windows Apps**: Remove unnecessary pre-installed apps
- **Xbox Services**: Disable Xbox-related services
- **Cortana**: Disable Cortana and web search
- **Widgets**: Remove Windows 11 widgets
- **Edge Integration**: Disable Microsoft Edge integration
- **Start Menu**: Clean suggestions and ads

### ⚡ **Performance Optimization**
- **Services**: Disable unnecessary background services
- **Visual Effects**: Optimize for performance over appearance
- **Power Settings**: Set high-performance power plan
- **Memory Management**: Optimize memory usage
- **Search Indexing**: Disable for better performance

## 🚀 Ready to Take Control? Here's What You Need

Don't worry - I've made this as simple as possible! You just need:

- **Windows 11** (obviously! 😄)
- **Python 3.6 or higher** ([Download here if you don't have it](https://www.python.org/downloads/))
- **Administrator privileges** (Right-click → "Run as administrator" - trust me, it's worth it!)

That's it! No complicated setup, no weird dependencies. Just download, run, and take back control of your PC.

## 🎮 How to Use This Magic

### ⚡ Super Quick Start (2 Minutes to Freedom!)

1. **Download** this repository (green "Code" button → "Download ZIP")
2. **Extract** all files to a folder (like `C:\WindowsManager\`)
3. **Choose your preferred method to run with admin privileges:**

   **🎯 Method 1: Automatic Admin Request (Easiest)**
   - Double-click `run_as_admin.bat` OR
   - Right-click `run_as_admin.ps1` → "Run with PowerShell"
   - Click "Yes" when Windows asks for admin privileges

   **🎯 Method 2: Manual Admin Setup**
   - Right-click Command Prompt → "Run as administrator"
   - Navigate to your folder: `cd C:\WindowsManager\`
   - Run the launcher: `python launcher.py`

   **🎯 Method 3: Built-in Admin Request**
   - Run `python launcher.py` normally
   - The app will detect you're not admin and offer to restart with privileges

4. **Choose what annoys you most** and let the tool fix it!
5. **Restart your PC** when prompted (trust me, it's worth the 30 seconds)

**That's it!** You're now in control of your own computer again. Feels good, doesn't it? 😊

### 🎛️ Your Control Panel (Main Menu)

When you run the tool, you'll see this beautiful menu (yes, I'm proud of it! 😄):

```
🔄 UPDATE MANAGEMENT:
1. 🚫 DISABLE Windows Updates        ← Stop the update madness!
2. 🔄 RESTORE Windows Updates        ← Bring them back if needed
3. 🔄 COMPREHENSIVE RESTORE          ← Undo EVERYTHING safely

🛠️ SYSTEM MANAGEMENT:
4. ☁️  OneDrive Management           ← Kick OneDrive to the curb
5. 🔒 Privacy & Telemetry Control    ← Stop Microsoft spying
6. 🗑️  Bloatware Removal            ← Delete the junk
7. ⚡ Performance Optimization       ← Make it fast again

📖 HELP & INFO:
8. ℹ️  INFORMATION                   ← Learn what each tool does
9. ❌ EXIT                           ← See you later!
```

**Pro tip:** Start with option 8 (Information) if you're new to this. I've written detailed explanations of what each tool does!

### 🎨 Enhanced Visual Experience

The latest version includes **automatic color and symbol support** for the best terminal experience:

- **🌈 Smart Color Detection** - Automatically uses colorama for perfect Windows color support
- **🔤 Unicode Symbols** - Beautiful icons with ASCII fallbacks for older terminals
- **🖥️ Terminal Adaptation** - Automatically detects your terminal's capabilities
- **⚡ UTF-8 Support** - Proper encoding for international characters

**Test Your Terminal:**
```cmd
python test_colors_symbols.py
```

**Setup Enhanced Colors (optional):**
```cmd
python setup_colors.py
```

If colors or symbols don't display properly, the app automatically falls back to ASCII alternatives - it always works!

### Individual Module Usage

You can also run individual modules directly:

```cmd
# OneDrive management
python modules/onedrive_manager.py

# Privacy and telemetry control
python modules/telemetry_manager.py

# Bloatware removal
python modules/bloatware_manager.py

# Performance optimization
python modules/performance_manager.py
```

## Safety and Restore Features

### 🔄 **Comprehensive Restore**
The tool includes a comprehensive restore script (`comprehensive_restore.py`) that can:
- Restore all Windows Update functionality
- Re-enable OneDrive services and integration
- Restore telemetry and diagnostic services
- Reset performance optimizations
- Re-enable Xbox services
- Restore all registry modifications

### 🛡️ **Safety Features**
- **Confirmation prompts** for all major operations
- **Detailed logging** of all changes made
- **Granular control** - choose specific features to modify
- **Administrator detection** - warns if not running with proper privileges
- **Error handling** - graceful handling of permission issues

### ⚠️ **Important Warnings**
- **Always run as Administrator** for full functionality
- **Create a system restore point** before making changes
- **Some features may affect system functionality** - review carefully
- **Restart recommended** after making changes
- **Keep restore scripts safe** for future use

### Restore Script Actions:
1. **Service Restoration**:
   - Re-enables all Windows Update services
   - Sets startup type to "Automatic"
   - Starts the services

2. **Registry Cleanup**:
   - Removes policy registry keys that disable updates

3. **Task Restoration**:
   - Re-enables all Windows Update scheduled tasks

4. **Network Restoration**:
   - Removes URL blocks from hosts file

## Important Notes

⚠️ **Warnings**:
- These scripts modify system settings and should be used with caution
- Always run as Administrator for full functionality
- A system restart is recommended after running either script
- Keep the restore script safe in case you need to re-enable updates

🔒 **Security Considerations**:
- Disabling Windows Updates can leave your system vulnerable to security threats
- Only disable updates temporarily and for specific reasons
- Consider re-enabling updates regularly to receive security patches

📝 **Compatibility**:
- Designed for Windows 11
- May work on Windows 10 with minor modifications
- Some features require Administrator privileges

## Troubleshooting

### Common Issues:

1. **"Access Denied" errors**:
   - Run the script as Administrator
   - Some operations require elevated privileges

2. **Service start/stop failures**:
   - Some services may be protected by Windows
   - Try running the script multiple times
   - Restart and try again

3. **Registry access errors**:
   - Ensure you're running as Administrator
   - Some registry keys may be protected

4. **Hosts file modification fails**:
   - Check if antivirus is blocking hosts file changes
   - Ensure Administrator privileges

### Manual Verification:

After running the disable script, you can verify:
- Services: `services.msc` → Check Windows Update services are stopped/disabled
- Registry: `regedit` → Navigate to Windows Update policy keys
- Tasks: `taskschd.msc` → Check Windows Update tasks are disabled
- Hosts: Check `C:\Windows\System32\drivers\etc\hosts` for blocked URLs

## License

These scripts are provided as-is for educational and administrative purposes. Use at your own risk.

## Author

**Zied Boughdir**
GitHub: [https://github.com/zinzied](https://github.com/zinzied)
Year: 2025

## � What Makes This Special

I didn't just throw together some scripts and call it a day. This toolkit represents **months of research, testing, and refinement**. Here's what makes it different:

### 🧠 **Smart & Safe**
- **Confirmation prompts** before making any changes (no accidental disasters!)
- **Comprehensive restore** functionality (made a mistake? No problem!)
- **Detailed explanations** of what each tool does (no mysterious black boxes)
- **Error handling** that actually makes sense (no cryptic error messages)

### 🎯 **User-Focused Design**
- **Modular approach** - use only what you need
- **Clear, colorful interface** that's actually pleasant to use
- **Real-world scenarios** - built by someone who actually uses Windows 11 daily
- **Honest documentation** - I tell you exactly what each tool does and why

### � **Constantly Improving**
This isn't a "set it and forget it" project. I actively use this toolkit on my own systems and continuously improve it based on real-world experience.

## 💡 Real-World Examples (Because I Know You Want to See Results!)

### 🕵️ **"I Want My Privacy Back" Setup**
*Perfect for people who are tired of Microsoft knowing everything about them*

```
Step 1: Run launcher.py as Administrator
Step 2: Choose option 5 (Privacy & Telemetry Control)
Step 3: Select "Disable All Telemetry & Enhance Privacy"
Step 4: Choose option 4 (OneDrive Management)
Step 5: Select "Disable OneDrive Completely"

Result: Microsoft stops collecting your data, no more OneDrive nagging!
```

### 🚀 **"Make My PC Fast Again" Setup**
*For when your computer feels like it's running through molasses*

```
Step 1: Run launcher.py as Administrator
Step 2: Choose option 7 (Performance Optimization)
Step 3: Select "Optimize All Performance Settings"
Step 4: Choose option 6 (Bloatware Removal)
Step 5: Select "Remove All Bloatware"

Result: Faster boot times, more responsive system, cleaner interface!
```

### 🛡️ **"Nuclear Option" - Complete Control Setup**
*When you want to take back FULL control of your computer*

```
Step 1: Run launcher.py as Administrator
Step 2: Choose option 1 (Disable Windows Updates)
Step 3: Choose option 5 (Privacy & Telemetry Control)
Step 4: Choose option 6 (Bloatware Removal)
Step 5: Choose option 7 (Performance Optimization)

Result: YOUR computer finally behaves like YOUR computer!
```

## ☕ Support My Work

If this toolkit saved you hours of frustration (and let's be honest, it probably did! 😄), consider buying me a coffee! It helps me keep improving this tool and creating new ones.

<div align="center">

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://www.buymeacoffee.com/Zied)

**[☕ Buy me a coffee](https://www.buymeacoffee.com/Zied)**

*Your support means the world to me and helps keep this project alive!*

</div>

---

## ⚠️ The Boring But Important Legal Stuff

Look, I have to say this (lawyers, you know 🙄):

**This tool modifies Windows system settings.** I've tested it extensively on my own systems, but every computer is different. While I've built in safety features and restore capabilities, you should:

- **Create a system backup** before making major changes (Windows has built-in backup tools!)
- **Start with small changes** to see how your system responds
- **Read the information section** (option 8) to understand what each tool does
- **Keep the restore scripts handy** (that's why I built them!)

I use this toolkit daily on my own computers, but I can't be responsible if something goes wrong on yours. That said, I've designed it to be as safe as possible, and the restore functionality can undo everything if needed.

**Bottom line:** Use common sense, start small, and you'll be fine! 🙂

---

## 🤝 Let's Connect!

I'm always working on new tools and improvements. If you have suggestions, found a bug, or just want to say thanks:

- **GitHub:** [https://github.com/zinzied](https://github.com/zinzied)
- **Buy me a coffee:** [https://www.buymeacoffee.com/Zied](https://www.buymeacoffee.com/Zied)

**Made with ❤️ and lots of coffee by Zied Boughdir**
*"Because your computer should work for YOU, not against you!"*

---

<div align="center">

**⭐ If this helped you, please star this repository! ⭐**

*It helps other frustrated Windows users find this toolkit!*

</div>
