"""
Fusion 360 HTML Control Panel - Mode Switcher
Switches between local and online versions
"""

import os
import re

def switch_mode(use_online=True, custom_url=None):
    """
    Switch between local and online mode
    
    Args:
        use_online (bool): True for online mode, False for local mode
        custom_url (str): Custom online URL (optional)
    """
    
    # Path to entry.py file
    entry_file = os.path.join(os.path.dirname(__file__), 'entry.py')
    
    if not os.path.exists(entry_file):
        print(f"❌ Entry file not found: {entry_file}")
        return False
    
    # Read current content
    with open(entry_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update USE_ONLINE_VERSION
    pattern = r'USE_ONLINE_VERSION = (True|False)'
    new_value = 'True' if use_online else 'False'
    content = re.sub(pattern, f'USE_ONLINE_VERSION = {new_value}', content)
    
    # Update custom URL if provided
    if use_online and custom_url:
        url_pattern = r"PALETTE_URL = 'https://[^']+'"
        content = re.sub(url_pattern, f"PALETTE_URL = '{custom_url}'", content)
    
    # Write back to file
    with open(entry_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    mode = "online" if use_online else "local"
    print(f"✅ Switched to {mode} mode successfully!")
    
    if use_online and custom_url:
        print(f"🌐 Online URL: {custom_url}")
    elif use_online:
        print("🌐 Using default online URL (update it in entry.py)")
    else:
        print("📁 Using local HTML files")
    
    print("\n🔄 Please restart the add-in in Fusion 360 to see changes.")
    
    return True

def get_current_mode():
    """Get current mode (online/local)"""
    entry_file = os.path.join(os.path.dirname(__file__), 'entry.py')
    
    if not os.path.exists(entry_file):
        return None
    
    with open(entry_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'USE_ONLINE_VERSION = True' in content:
        # Extract URL
        import re
        url_match = re.search(r"PALETTE_URL = '([^']+)'", content)
        url = url_match.group(1) if url_match else "Unknown"
        return {"mode": "online", "url": url}
    else:
        return {"mode": "local", "url": "Local files"}

if __name__ == "__main__":
    print("🚀 Fusion 360 HTML Control Panel - Mode Switcher")
    print("=" * 50)
    
    # Show current mode
    current = get_current_mode()
    if current:
        print(f"📍 Current mode: {current['mode']}")
        print(f"🔗 URL: {current['url']}")
        print()
    
    print("Choose an option:")
    print("1. Switch to Local mode")
    print("2. Switch to Online mode (GitHub Pages)")
    print("3. Switch to Online mode (Custom URL)")
    print("4. Show current status")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-4): ").strip()
    
    if choice == "1":
        switch_mode(use_online=False)
        
    elif choice == "2":
        # GitHub Pages example
        username = input("Enter your GitHub username: ").strip()
        repo = input("Enter repository name (default: fusion360-control-panel): ").strip()
        if not repo:
            repo = "fusion360-control-panel"
        
        url = f"https://{username}.github.io/{repo}/online-index.html"
        switch_mode(use_online=True, custom_url=url)
        
    elif choice == "3":
        # Custom URL
        url = input("Enter your custom URL: ").strip()
        if url:
            switch_mode(use_online=True, custom_url=url)
        else:
            print("❌ No URL provided")
            
    elif choice == "4":
        current = get_current_mode()
        if current:
            print(f"\n📍 Current mode: {current['mode']}")
            print(f"🔗 URL: {current['url']}")
        else:
            print("❌ Could not determine current mode")
            
    elif choice == "0":
        print("👋 Goodbye!")
        
    else:
        print("❌ Invalid choice")
