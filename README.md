# Unreal Engine Project

This repository contains tools and resources for working with Unreal Engine 4 projects, including a blueprint reader for cooked UE4 assets.

## Blueprint Reader

The `blueprint_reader.py` script provides functionality to read information from cooked UE4 blueprint files (.uasset files).

### Features
- Parse UE4 file headers
- Extract basic blueprint information
- Identify blueprint types and structure

### Usage
```bash
python blueprint_reader.py /path/to/MyBlueprint.uasset
```

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
