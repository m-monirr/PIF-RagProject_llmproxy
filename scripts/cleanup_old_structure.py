"""
Cleanup script to remove old project structure after reorganization
Safely removes old files and directories that have been moved to new locations
"""

import sys
from pathlib import Path

# Add project root to Python path (if needed)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import os
import shutil
from datetime import datetime

# Old files and directories to remove
OLD_STRUCTURE = {
    'directories': [
        'api_code',           # Moved to src/core, src/retrieval, src/llm
        'ui_streamlit',       # Moved to src/ui
    ],
    'files': [
        'start_llm_proxy_alternative.py',  # Moved to scripts/start_llm_proxy.py
        'run_streamlit.py',                # Moved to scripts/run_streamlit.py
        'RUN_GUIDE.md',                    # Moved to docs/RUN_GUIDE.md
        'llm_proxy_config.yaml',           # Moved to config/llm_proxy_config.yaml
        '.env',                            # Moved to config/.env
        '.env.example',                    # Moved to config/.env.example
    ]
}

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent

def create_backup_list(root_dir, items_to_remove):
    """Create a backup list of items being removed"""
    backup_file = root_dir / f"cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write("# Cleanup Backup List\n")
        f.write(f"# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Directories Removed:\n")
        for dir_name in items_to_remove['directories']:
            dir_path = root_dir / dir_name
            if dir_path.exists():
                f.write(f"  - {dir_path}\n")
        
        f.write("\n## Files Removed:\n")
        for file_name in items_to_remove['files']:
            file_path = root_dir / file_name
            if file_path.exists():
                f.write(f"  - {file_path}\n")
    
    return backup_file

def check_items_exist(root_dir, items):
    """Check which items exist and return counts"""
    existing_dirs = []
    existing_files = []
    
    for dir_name in items['directories']:
        dir_path = root_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            existing_dirs.append(dir_path)
    
    for file_name in items['files']:
        file_path = root_dir / file_name
        if file_path.exists() and file_path.is_file():
            existing_files.append(file_path)
    
    return existing_dirs, existing_files

def display_items_to_remove(dirs, files):
    """Display what will be removed"""
    print("\n" + "="*60)
    print("📁 OLD STRUCTURE CLEANUP")
    print("="*60 + "\n")
    
    if dirs:
        print("🗂️  Directories to remove:")
        for d in dirs:
            print(f"   ❌ {d.name}/")
        print()
    
    if files:
        print("📄 Files to remove:")
        for f in files:
            print(f"   ❌ {f.name}")
        print()
    
    total = len(dirs) + len(files)
    print(f"📊 Total items to remove: {total}")
    print("="*60 + "\n")

def remove_items(dirs, files, backup_file):
    """Remove directories and files"""
    removed_count = 0
    errors = []
    
    # Remove directories
    for dir_path in dirs:
        try:
            print(f"🗑️  Removing directory: {dir_path.name}/")
            shutil.rmtree(dir_path)
            removed_count += 1
            print(f"   ✅ Removed successfully")
        except Exception as e:
            error_msg = f"Failed to remove {dir_path}: {str(e)}"
            errors.append(error_msg)
            print(f"   ❌ {error_msg}")
    
    # Remove files
    for file_path in files:
        try:
            print(f"🗑️  Removing file: {file_path.name}")
            file_path.unlink()
            removed_count += 1
            print(f"   ✅ Removed successfully")
        except Exception as e:
            error_msg = f"Failed to remove {file_path}: {str(e)}"
            errors.append(error_msg)
            print(f"   ❌ {error_msg}")
    
    return removed_count, errors

def main():
    """Main cleanup function"""
    print("\n🧹 PIF RAG Project - Old Structure Cleanup Tool")
    print("=" * 60)
    
    # Get project root
    root_dir = get_project_root()
    print(f"\n📂 Project directory: {root_dir}")
    
    # Check what exists
    existing_dirs, existing_files = check_items_exist(root_dir, OLD_STRUCTURE)
    
    if not existing_dirs and not existing_files:
        print("\n✨ Nothing to clean! Old structure already removed.")
        print("\n💡 Tip: Make sure new structure is in place:")
        print("   - src/core/")
        print("   - src/retrieval/")
        print("   - src/llm/")
        print("   - src/ui/")
        print("   - config/")
        print("   - scripts/")
        print("   - docs/")
        return
    
    # Display items to remove
    display_items_to_remove(existing_dirs, existing_files)
    
    # Confirm before proceeding
    print("⚠️  WARNING: This will permanently delete the above items!")
    print("💾 A backup list will be created before deletion.\n")
    
    response = input("❓ Do you want to proceed? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("\n❌ Cleanup cancelled. No files were removed.")
        return
    
    print("\n🔄 Starting cleanup process...\n")
    
    # Create backup list
    backup_file = create_backup_list(root_dir, OLD_STRUCTURE)
    print(f"💾 Backup list created: {backup_file.name}\n")
    
    # Remove items
    removed_count, errors = remove_items(existing_dirs, existing_files, backup_file)
    
    # Summary
    print("\n" + "="*60)
    print("📊 CLEANUP SUMMARY")
    print("="*60)
    print(f"✅ Successfully removed: {removed_count} items")
    
    if errors:
        print(f"❌ Errors: {len(errors)}")
        print("\nError details:")
        for error in errors:
            print(f"   • {error}")
    else:
        print("❌ Errors: 0")
    
    print(f"\n💾 Backup list saved: {backup_file.name}")
    print("\n✨ Cleanup complete!")
    print("\n💡 Next steps:")
    print("   1. Verify new structure is working: streamlit run app.py")
    print("   2. Test all functionality")
    print("   3. Delete backup file if everything works: rm cleanup_backup_*.txt")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cleanup interrupted by user. Some items may not be removed.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
