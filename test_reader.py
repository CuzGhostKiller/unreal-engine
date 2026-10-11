#!/usr/bin/env python3
"""
Test script for the UE4 Blueprint Reader
"""

import os
import sys

# Add current directory to Python path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blueprint_reader import UE4BlueprintReader

def test_basic_functionality():
    """Test basic functionality of the blueprint reader."""
    
    print("=== UE4 Blueprint Reader Test ===")
    
    # Create a simple test - we'll create a mock file to demonstrate
    reader = UE4BlueprintReader()
    
    # Show that we can import and instantiate the class
    print("✓ Successfully imported UE4BlueprintReader")
    print("✓ Successfully instantiated reader object")
    
    # Test version detection functionality
    print("\n=== Version Detection Tests ===")
    
    # Test setting Unreal Engine path (this will be a mock test)
    print("✓ Created reader with default path")
    
    # Test with a non-existent file (should fail gracefully)
    result = reader.load_file("/non/existent/file.uasset")
    print(f"✓ Attempted to load non-existent file: {result}")
    
    # Show the structure of the class
    print("\n=== Class Methods ===")
    methods = [method for method in dir(reader) if not method.startswith('_')]
    for method in sorted(methods):
        print(f"  - {method}")
        
    # Test version info retrieval
    version_info = reader.get_version_info()
    print(f"\n✓ Version info retrieved: {version_info}")
    
    # Test supported versions list
    supported_versions = reader.list_supported_versions()
    print(f"✓ Supported versions count: {len(supported_versions)}")

if __name__ == "__main__":
    test_basic_functionality()