#!/usr/bin/env python3
"""
Fusion 360 GitHub Pages - Simple Setup
Tự động tạo và upload lên GitHub
"""

import os
import subprocess
import sys

def check_git():
    """Kiểm tra Git có cài đặt không"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def run_command(cmd, cwd=None):
    """Chạy command và hiển thị output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 FUSION 360 GITHUB PAGES SETUP")
    print("=" * 40)
    
    # Check git
    if not check_git():
        print("❌ Git không được cài đặt!")
        print("📥 Download tại: https://git-scm.com/")
        input("Press Enter to exit...")
        return
    
    print("✅ Git detected")
    
    # Get user input
    username = input("Nhập GitHub username: ").strip()
    repo_name = input("Nhập repository name (default: fusion360-control-panel): ").strip()
    
    if not repo_name:
        repo_name = "fusion360-control-panel"
    
    if not username:
        print("❌ Username is required!")
        return
    
    # Confirm
    print(f"\n📋 Thông tin:")
    print(f"Username: {username}")
    print(f"Repository: {repo_name}")
    print(f"URL: https://{username}.github.io/{repo_name}/online-index.html")
    
    confirm = input("\nTiếp tục? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Create temp directory
    import tempfile
    temp_dir = os.path.join(tempfile.gettempdir(), repo_name)
    
    if os.path.exists(temp_dir):
        import shutil
        shutil.rmtree(temp_dir)
    
    os.makedirs(temp_dir)
    print(f"📁 Created temp directory: {temp_dir}")
    
    # Copy files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(current_dir, 'resources', 'html', 'online-index.html')
    readme_file = os.path.join(current_dir, '..', '..', '..', 'README-ONLINE.md')
    
    if os.path.exists(html_file):
        import shutil
        shutil.copy2(html_file, temp_dir)
        print("✅ Copied online-index.html")
    else:
        print(f"❌ HTML file not found: {html_file}")
        return
    
    if os.path.exists(readme_file):
        import shutil
        shutil.copy2(readme_file, os.path.join(temp_dir, 'README.md'))
        print("✅ Copied README.md")
    
    # Create .gitignore
    gitignore_content = """node_modules/
.DS_Store
*.log
__pycache__/
.env
"""
    with open(os.path.join(temp_dir, '.gitignore'), 'w') as f:
        f.write(gitignore_content)
    
    # Git operations
    print("\n🔧 Setting up Git...")
    
    commands = [
        "git init",
        "git add .",
        'git commit -m "Add Fusion 360 HTML Control Panel"',
        "git branch -M main"
    ]
    
    for cmd in commands:
        if not run_command(cmd, temp_dir):
            print(f"❌ Failed: {cmd}")
            return
    
    print("✅ Git setup complete")
    
    # Instructions for GitHub
    print("\n" + "="*50)
    print("🌐 BẠN CẦN TẠO REPOSITORY TRÊN GITHUB:")
    print("="*50)
    print("1. Mở: https://github.com/new")
    print(f"2. Repository name: {repo_name}")
    print("3. ✅ Public")
    print("4. ❌ KHÔNG tick 'Add a README file'")
    print("5. Click 'Create repository'")
    print("="*50)
    
    created = input("\nĐã tạo repository chưa? (y/n): ").strip().lower()
    if created != 'y':
        print("❌ Vui lòng tạo repository trước")
        return
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    
    push_commands = [
        f"git remote add origin https://github.com/{username}/{repo_name}.git",
        "git push -u origin main"
    ]
    
    for cmd in push_commands:
        if not run_command(cmd, temp_dir):
            print(f"❌ Failed: {cmd}")
            print("\n🔍 Possible issues:")
            print("- Repository doesn't exist")
            print("- Not public repository")
            print("- Wrong username/repo name")
            print("- No push access")
            return
    
    print("✅ Upload successful!")
    
    # Update entry.py
    print("\n🔧 Updating entry.py...")
    entry_file = os.path.join(current_dir, 'entry.py')
    
    if os.path.exists(entry_file):
        with open(entry_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update URL
        new_url = f"https://{username}.github.io/{repo_name}/online-index.html"
        
        import re
        pattern = r"PALETTE_URL = 'https://[^']+\.github\.io/[^']+'"
        replacement = f"PALETTE_URL = '{new_url}'"
        
        content = re.sub(pattern, replacement, content)
        content = re.sub(r'USE_ONLINE_VERSION = False', 'USE_ONLINE_VERSION = True', content)
        
        with open(entry_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ entry.py updated")
    
    # Final instructions
    print("\n" + "🎉" * 20)
    print("SETUP HOÀN THÀNH!")
    print("🎉" * 20)
    print(f"\n📋 BƯỚC CUỐI:")
    print(f"1. Vào: https://github.com/{username}/{repo_name}/settings/pages")
    print("2. Source: Deploy from a branch")
    print("3. Branch: main")
    print("4. Folder: / (root)")
    print("5. Click Save")
    print(f"\n🌐 URL: https://{username}.github.io/{repo_name}/online-index.html")
    print("\n⏰ Đợi 1-2 phút để GitHub deploy")
    print("🔄 Restart add-in trong Fusion 360")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
