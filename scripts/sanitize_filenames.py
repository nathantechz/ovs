#!/usr/bin/env python3
"""
Filename and Directory Sanitizer
Removes colons (:) and invalid URI characters from materials/ folders and files
to ensure 100% cross-platform compatibility on GitHub Pages, Linux, and Windows.
"""

import os
import glob
import json
import re

def sanitize_name(name):
    # Replace colons and em dashes with clean hyphens
    clean = name.replace(':', ' -').replace('—', '-').replace('–', '-')
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def main():
    # 1. Rename files first
    all_files = glob.glob('materials/**/*', recursive=True) + glob.glob('notes/**/*', recursive=True)
    all_files = [f for f in all_files if os.path.isfile(f)]
    
    renamed_files_count = 0
    for f in all_files:
        dirname = os.path.dirname(f)
        basename = os.path.basename(f)
        if ':' in basename or '—' in basename:
            new_basename = sanitize_name(basename)
            new_path = os.path.join(dirname, new_basename)
            os.rename(f, new_path)
            renamed_files_count += 1
            
    print(f"✓ Renamed {renamed_files_count} files with invalid characters.")
    
    # 2. Rename directories
    dirs = glob.glob('materials/*')
    dirs = [d for d in dirs if os.path.isdir(d)]
    
    renamed_dirs_count = 0
    for d in dirs:
        dirname = os.path.dirname(d)
        basename = os.path.basename(d)
        if ':' in basename or '—' in basename:
            new_basename = sanitize_name(basename)
            new_path = os.path.join(dirname, new_basename)
            os.rename(d, new_path)
            renamed_dirs_count += 1
            
    print(f"✓ Renamed {renamed_dirs_count} directories with invalid characters.")
    
    # 3. Regenerate js/materials-list.js to ensure all paths are clean
    from build_practicals_and_expanded_syllabi import main as rebuild_materials
    rebuild_materials()
    print("✓ Rebuilt js/materials-list.js with sanitized paths!")

if __name__ == "__main__":
    main()
