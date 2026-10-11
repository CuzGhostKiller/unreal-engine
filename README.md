# Unreal Engine Project

This repository contains tools and resources for working with Unreal Engine 4 projects, including a blueprint reader for cooked UE4 assets.

## Blueprint Reader

The `blueprint_reader.py` script provides functionality to read information from cooked UE4 blueprint files (.uasset files).

### Features
- Parse UE4 file headers
- Extract basic blueprint information
- Identify blueprint types and structure
- Detect Unreal Engine version from installation path
- Support for multiple UE4 versions

### Usage
```bash
# Basic usage
python blueprint_reader.py /path/to/MyBlueprint.uasset

# With Unreal Engine installation path for version detection
python blueprint_reader.py /path/to/MyBlueprint.uasset /path/to/UnrealEngine
```

### Version Detection
The reader can detect the Unreal Engine version by:
1. Looking at the installation path (e.g., "UE_4.27", "UE_5.0")
2. Parsing version files like Build.version
3. Extracting version information from UE4 source files

This allows for version-specific handling of different file formats and serialization methods.

### Limitations
This is a basic implementation. A full UE4 blueprint parser would need to:
- Understand the complete UE4 serialization format
- Parse UObject structures properly
- Handle different UE4 versions and file formats
- Extract actual blueprint node information, variables, functions, etc.

For production use, consider using:
- UE4's own tools (like UnrealPak, UModel)
- Third-party libraries like unreal-engine-parser
- Direct integration with UE4's C++ APIs

### Supported UE4 Versions
The reader supports the following UE4 versions:
- UE4.27
- UE4.26 
- UE4.25
- UE4.24
- UE4.23
- UE4.22
- UE4.21
- UE4.20
- UE4.19
- UE4.18
- UE4.17
- UE4.16
- UE4.15
- UE4.14
- UE4.13
- UE4.12
- UE4.11
- UE4.10
