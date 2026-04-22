#!/usr/bin/env python3
"""
Verification script for fastapi-ready scaffold cleanliness.

Usage:
    python verify_scaffold.py /path/to/generated/project
    
This script ensures the generated scaffold contains only the expected files
and no stray libraries or environment artifacts.
"""

import sys
from pathlib import Path


EXPECTED_SCAFFOLD_FILES = {
    # Root files
    "main.py",
    ".env.example",
    "README.md",
    # Directories
    "auth",
    "config",
    "core",
    "db",
    "models",
    "router",
    "schemas",
}

FORBIDDEN_PATTERNS = {
    "__pycache__",
    ".egg-info",
    ".venv",
    "venv",
    "site-packages",
    "dist-info",
    ".pytest_cache",
    ".coverage",
}


def verify_scaffold(project_path: Path) -> bool:
    """
    Verify that a generated scaffold contains only expected files.
    
    Returns True if scaffold is clean, False otherwise.
    """
    project_path = Path(project_path).resolve()
    
    if not project_path.is_dir():
        print(f"❌ Error: {project_path} is not a directory")
        return False
    
    print(f"📋 Verifying scaffold at: {project_path}")
    print()
    
    # Get top-level items
    top_level = set()
    for item in project_path.iterdir():
        top_level.add(item.name)
    
    # Check for unexpected items at top level
    print("📂 Top-level contents:")
    unexpected = top_level - EXPECTED_SCAFFOLD_FILES
    
    for item in sorted(top_level):
        if item.startswith("."):
            print(f"   ✓ {item}")
        else:
            print(f"   ✓ {item}")
    
    print()
    
    if unexpected:
        print(f"❌ Unexpected items at top level: {', '.join(sorted(unexpected))}")
        return False
    
    # Check for forbidden patterns anywhere in tree
    print("🔍 Scanning for forbidden patterns...")
    forbidden_found = []
    for item in project_path.rglob("*"):
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in item.name:
                forbidden_found.append(item.relative_to(project_path))
    
    if forbidden_found:
        print(f"❌ Found {len(forbidden_found)} forbidden items:")
        for item in sorted(forbidden_found)[:10]:  # Show first 10
            print(f"   - {item}")
        if len(forbidden_found) > 10:
            print(f"   ... and {len(forbidden_found) - 10} more")
        return False
    
    print("   ✓ No forbidden patterns found")
    print()
    
    # Count files
    file_count = sum(1 for _ in project_path.rglob("*") if _.is_file())
    dir_count = sum(1 for _ in project_path.rglob("*") if _.is_dir())
    
    print(f"📊 Statistics:")
    print(f"   Files: {file_count}")
    print(f"   Directories: {dir_count}")
    print()
    
    print("✅ Scaffold verification passed!")
    return True


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    project_path = sys.argv[1]
    success = verify_scaffold(project_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
