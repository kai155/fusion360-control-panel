"""
Quick GitHub Pages URL Updater
Automatically updates the GitHub Pages URL in entry.py
"""

import os
import re

def update_github_pages_url():
    print("🚀 GitHub Pages URL Updater")
    print("=" * 40)
    
    # Auto-detected information
    username = "kai155"
    repo_name = "fusion360-control-panel"
    
    print(f"✅ Auto-detected GitHub info:")
    print(f"   Username: {username}")
    print(f"   Repository: {repo_name}")
    
    # Allow user to override
    custom = input("Use different settings? (y/n, default: n): ").strip().lower()
    
    if custom == 'y':
        username = input("Enter your GitHub username: ").strip()
        repo_name = input("Enter repository name (default: fusion360-control-panel): ").strip()
        
        if not repo_name:
            repo_name = "fusion360-control-panel"
        
        if not username:
            print("❌ Username is required!")
            return False
    
    # Generate URL
    url = f"https://{username}.github.io/{repo_name}/online-index.html"
    
    print(f"\n🔗 Generated URL: {url}")
    confirm = input("Is this correct? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Operation cancelled")
        return False
    
    # Update entry.py
    entry_file = os.path.join(os.path.dirname(__file__), 'entry.py')
    
    if not os.path.exists(entry_file):
        print(f"❌ Entry file not found: {entry_file}")
        return False
    
    # Read and update content
    with open(entry_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update URL
    pattern = r"PALETTE_URL = 'https://[^']+\.github\.io/[^']+'"
    replacement = f"PALETTE_URL = '{url}'"
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
    else:
        # Fallback: replace any GitHub Pages URL
        pattern2 = r"PALETTE_URL = 'https://your-username\.github\.io/[^']+'"
        content = re.sub(pattern2, replacement, content)
    
    # Ensure online mode is enabled
    content = re.sub(r'USE_ONLINE_VERSION = False', 'USE_ONLINE_VERSION = True', content)
    
    # Write back
    with open(entry_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated entry.py successfully!")
    print(f"🌐 GitHub Pages URL: {url}")
    print("\n📋 Next steps:")
    print("1. Upload 'online-index.html' to your GitHub repo")
    print("2. Enable GitHub Pages in repo settings")
    print("3. Restart the add-in in Fusion 360")
    print("4. Test the palette!")
    
    return True

if __name__ == "__main__":
    update_github_pages_url()
    input("\nPress Enter to exit...")
