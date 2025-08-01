# 🛡️ Windows 11 Update Manager - Complete Control Over System Updates

**Created by:** Zied Boughdir
**GitHub:** [https://github.com/zinzied](https://github.com/zinzied)
**Year:** 2025

This repository contains Python scripts to stop/disable and restore Windows 11 automatic updates.

## Introduction: Why Disable Windows Updates?

While Windows Updates are generally important for security and functionality, there are legitimate scenarios where users may need to temporarily or permanently disable automatic updates:

### 🎯 **Common Reasons to Disable Updates:**

1. **System Stability Issues**
   - Problematic updates causing system crashes or boot failures
   - Driver conflicts introduced by recent updates
   - Software compatibility issues with critical applications

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

## Files

- `disable_windows_updates.py` - Main script to disable Windows 11 updates
- `restore_windows_updates.py` - Script to restore Windows 11 updates functionality
- `README.md` - This documentation file

## Features

### Disable Script (`disable_windows_updates.py`)
- **Stops Windows Update Services**: Stops and disables core update services
- **Registry Modifications**: Sets registry keys to prevent automatic updates
- **Disables Scheduled Tasks**: Disables Windows Update related scheduled tasks
- **Blocks Update URLs**: Adds Windows Update URLs to hosts file to block network access
- **Creates Restore Script**: Automatically generates the restore script

### Restore Script (`restore_windows_updates.py`)
- **Re-enables Services**: Restores Windows Update services to automatic startup
- **Cleans Registry**: Removes registry modifications that disable updates
- **Re-enables Tasks**: Restores Windows Update scheduled tasks
- **Unblocks URLs**: Removes Windows Update URL blocks from hosts file

## Requirements

- Windows 11
- Python 3.6 or higher
- Administrator privileges (recommended for full functionality)

## Usage

### To Disable Windows Updates

1. **Run as Administrator** (recommended):
   ```cmd
   # Right-click Command Prompt -> "Run as administrator"
   python disable_windows_updates.py
   ```

2. **Or run normally** (some features may not work):
   ```cmd
   python disable_windows_updates.py
   ```

3. Follow the prompts and restart when asked for changes to take full effect.

### To Restore Windows Updates

1. **Run as Administrator**:
   ```cmd
   python restore_windows_updates.py
   ```

2. Follow the prompts and restart when asked.

## What Each Script Does

### Disable Script Actions:
1. **Service Management**:
   - Stops: `wuauserv`, `bits`, `dosvc`, `UsoSvc`
   - Sets startup type to "Disabled"

2. **Registry Changes**:
   - Sets `NoAutoUpdate = 1`
   - Sets `AUOptions = 1` (notify before download)
   - Disables Windows Update access
   - Sets dummy update server URLs

3. **Scheduled Tasks**:
   - Disables Windows Update and Update Orchestrator tasks

4. **Network Blocking**:
   - Blocks Windows Update URLs in hosts file

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

## Disclaimer

Modifying Windows Update settings can impact system security and stability. The author is not responsible for any issues that may arise from using these scripts. Always ensure you have proper backups and understand the implications before disabling system updates.
