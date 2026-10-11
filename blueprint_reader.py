#!/usr/bin/env python3
"""
Blueprint Reader for Unreal Engine 4 Cooked Blueprints

This script provides functionality to read information from cooked UE4 blueprint files.
"""

import os
import sys
import struct
import json
from typing import Dict, Any, Optional, List


class UE4BlueprintReader:
    """A class to read and parse UE4 blueprint information from cooked .uasset files."""
    
    def __init__(self, unreal_engine_path: Optional[str] = None):
        self.file_path = None
        self.file_data = None
        self.unreal_engine_path = unreal_engine_path
        self.version_info = {}
        
    def set_unreal_engine_path(self, path: str) -> bool:
        """
        Set the Unreal Engine installation path to detect version information.
        
        Args:
            path (str): Path to Unreal Engine installation
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(path):
            print(f"Error: Unreal Engine path {path} does not exist")
            return False
            
        self.unreal_engine_path = path
        self._detect_unreal_version()
        return True
    
    def _detect_unreal_version(self) -> Dict[str, Any]:
        """
        Detect the Unreal Engine version from the installation path.
        
        Returns:
            Dict containing version information
        """
        if not self.unreal_engine_path:
            return {}
            
        try:
            # Look for version files or directories that indicate UE4 version
            version_info = {
                'path': self.unreal_engine_path,
                'version': 'unknown',
                'major_version': 0,
                'minor_version': 0,
                'patch_version': 0
            }
            
            # Check common version file locations
            version_files = [
                os.path.join(self.unreal_engine_path, 'Engine', 'Build', 'Build.version'),
                os.path.join(self.unreal_engine_path, 'Build', 'Build.version'),
                os.path.join(self.unreal_engine_path, 'Engine', 'Source', 'Runtime', 'Core', 'Public', 'Version.h')
            ]
            
            for version_file in version_files:
                if os.path.exists(version_file):
                    # Try to parse Build.version file
                    try:
                        with open(version_file, 'r') as f:
                            content = f.read()
                            # Look for version information in the file
                            if 'MajorVersion' in content:
                                # This is a simplified approach - real implementation 
                                # would need more sophisticated parsing
                                version_info['version'] = 'detected'
                    except Exception:
                        pass
            
            # Try to extract version from path (e.g., "UE_4.27", "UE_5.0")
            path_parts = self.unreal_engine_path.split(os.sep)
            for part in path_parts:
                if part.startswith('UE_') or part.startswith('UnrealEngine_'):
                    version_str = part.replace('UE_', '').replace('UnrealEngine_', '')
                    if '.' in version_str:
                        parts = version_str.split('.')
                        try:
                            version_info['major_version'] = int(parts[0])
                            version_info['minor_version'] = int(parts[1]) if len(parts) > 1 else 0
                            version_info['patch_version'] = int(parts[2]) if len(parts) > 2 else 0
                            version_info['version'] = version_str
                        except ValueError:
                            pass
            
            self.version_info = version_info
            return version_info
            
        except Exception as e:
            print(f"Warning: Could not detect Unreal Engine version: {e}")
            return {}
    
    def load_file(self, file_path: str) -> bool:
        """
        Load a UE4 .uasset file for parsing.
        
        Args:
            file_path (str): Path to the .uasset file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist")
            return False
            
        try:
            with open(file_path, 'rb') as f:
                self.file_data = f.read()
            self.file_path = file_path
            return True
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return False
    
    def parse_header(self) -> Optional[Dict[str, Any]]:
        """
        Parse the UE4 file header.
        
        Returns:
            Dict containing header information or None if parsing fails
        """
        if not self.file_data:
            return None
            
        try:
            # UE4 files typically start with a magic number
            magic = struct.unpack('<I', self.file_data[0:4])[0]
            
            # Common UE4 magic numbers
            ue4_magic_numbers = {
                0x9E2A83C1: "UE4 Cooked Asset",
                0x9E2A83C2: "UE4 Cooked Asset (Alternative)",
                0x9E2A83C3: "UE4 Cooked Asset (Another Variant)"
            }
            
            header_info = {
                'magic': magic,
                'magic_name': ue4_magic_numbers.get(magic, f"Unknown magic {magic}"),
                'file_size': len(self.file_data),
                'ue_version': self.version_info
            }
            
            return header_info
            
        except Exception as e:
            print(f"Error parsing header: {e}")
            return None
    
    def extract_blueprint_info(self) -> Dict[str, Any]:
        """
        Extract blueprint information from the loaded file.
        
        Returns:
            Dict containing blueprint information
        """
        if not self.file_data:
            return {}
            
        info = {
            'file_path': self.file_path,
            'header': self.parse_header(),
            'blueprint_type': 'unknown',
            'properties': {},
            'references': [],
            'version_info': self.version_info
        }
        
        # Basic parsing - in a real implementation, this would be much more complex
        try:
            # Look for common blueprint identifiers or patterns
            data = self.file_data.decode('utf-8', errors='ignore')
            
            # Try to find blueprint-related strings
            if 'Blueprint' in data or 'blueprint' in data.lower():
                info['blueprint_type'] = 'blueprint'
                
        except Exception as e:
            print(f"Warning: Could not extract text information: {e}")
            
        return info
    
    def get_blueprint_structure(self) -> Dict[str, Any]:
        """
        Get the structure of the blueprint.
        
        Returns:
            Dict containing blueprint structure information
        """
        info = self.extract_blueprint_info()
        
        # This would be expanded in a real implementation to parse
        # the actual UE4 serialization format
        structure = {
            'file_info': info,
            'components': [],
            'functions': [],
            'variables': [],
            'events': []
        }
        
        return structure
    
    def get_version_info(self) -> Dict[str, Any]:
        """
        Get the detected Unreal Engine version information.
        
        Returns:
            Dict containing version information
        """
        return self.version_info
    
    def list_supported_versions(self) -> List[str]:
        """
        List supported UE4 versions that this reader can handle.
        
        Returns:
            List of supported version strings
        """
        # This would be expanded with actual version-specific handling
        return [
            "UE4.27",
            "UE4.26", 
            "UE4.25",
            "UE4.24",
            "UE4.23",
            "UE4.22",
            "UE4.21",
            "UE4.20",
            "UE4.19",
            "UE4.18",
            "UE4.17",
            "UE4.16",
            "UE4.15",
            "UE4.14",
            "UE4.13",
            "UE4.12",
            "UE4.11",
            "UE4.10"
        ]


def main():
    """Main function to demonstrate blueprint reading."""
    if len(sys.argv) < 2:
        print("Usage: python blueprint_reader.py <path_to_uasset_file> [unreal_engine_path]")
        print("Example: python blueprint_reader.py /path/to/MyBlueprint.uasset /path/to/UE4")
        return
        
    file_path = sys.argv[1]
    
    # Get optional Unreal Engine path
    unreal_engine_path = None
    if len(sys.argv) > 2:
        unreal_engine_path = sys.argv[2]
    
    reader = UE4BlueprintReader(unreal_engine_path)
    
    # Set Unreal Engine path if provided
    if unreal_engine_path:
        reader.set_unreal_engine_path(unreal_engine_path)
    
    if not reader.load_file(file_path):
        print(f"Failed to load {file_path}")
        return
        
    print(f"Reading blueprint from: {file_path}")
    
    # Show version information
    version_info = reader.get_version_info()
    if version_info:
        print("Unreal Engine Version Information:")
        for key, value in version_info.items():
            print(f"  {key}: {value}")
    
    # Parse header information
    header = reader.parse_header()
    if header:
        print("\nHeader Information:")
        for key, value in header.items():
            print(f"  {key}: {value}")
    
    # Extract blueprint info
    blueprint_info = reader.extract_blueprint_info()
    print("\nBlueprint Information:")
    for key, value in blueprint_info.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()