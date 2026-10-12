#!/usr/bin/env python3
"""
GUI Interface for UE4 Blueprint Reader

This script provides a graphical user interface to read information from cooked UE4 blueprint files.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Any, Optional

# Add current directory to Python path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blueprint_reader import UE4BlueprintReader


class BlueprintReaderUI:
    """GUI interface for the UE4 Blueprint Reader."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("UE4 Blueprint Reader")
        self.root.geometry("800x600")
        
        # Create the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive layout
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Initialize reader
        self.reader = UE4BlueprintReader()
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI widgets."""
        # Title
        title_label = ttk.Label(self.main_frame, text="UE4 Blueprint Reader", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(self.main_frame, text="Blueprint File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=60)
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.grid(row=0, column=2)
        
        # UE4 installation path section
        ue_frame = ttk.LabelFrame(self.main_frame, text="Unreal Engine Path", padding="10")
        ue_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        ue_frame.columnconfigure(1, weight=1)
        
        ttk.Label(ue_frame, text="Path:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.ue_path_var = tk.StringVar()
        ue_entry = ttk.Entry(ue_frame, textvariable=self.ue_path_var, width=60)
        ue_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ue_browse_button = ttk.Button(ue_frame, text="Browse", command=self.browse_ue_path)
        ue_browse_button.grid(row=0, column=2)
        
        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 20))
        
        self.analyze_button = ttk.Button(button_frame, text="Analyze Blueprint", command=self.analyze_blueprint)
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear Results", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT)
        
        # Results section
        results_frame = ttk.LabelFrame(self.main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Create text widget for results
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=20)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def browse_file(self):
        """Open file dialog to select a blueprint file."""
        file_path = filedialog.askopenfilename(
            title="Select Blueprint File",
            filetypes=[("UE4 Blueprint Files", "*.uasset"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def browse_ue_path(self):
        """Open directory dialog to select Unreal Engine installation path."""
        ue_path = filedialog.askdirectory(
            title="Select Unreal Engine Installation"
        )
        if ue_path:
            self.ue_path_var.set(ue_path)
            
    def analyze_blueprint(self):
        """Analyze the selected blueprint file."""
        # Get file path
        file_path = self.file_path_var.get().strip()
        if not file_path:
            messagebox.showwarning("Warning", "Please select a blueprint file to analyze.")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File does not exist: {file_path}")
            return
            
        # Get UE path
        ue_path = self.ue_path_var.get().strip()
        
        try:
            # Update status
            self.status_var.set("Analyzing blueprint...")
            self.root.update_idletasks()
            
            # Set Unreal Engine path if provided
            if ue_path:
                self.reader.set_unreal_engine_path(ue_path)
            
            # Load file
            if not self.reader.load_file(file_path):
                messagebox.showerror("Error", "Failed to load the blueprint file.")
                return
                
            # Perform analysis
            header = self.reader.parse_header()
            blueprint_info = self.reader.extract_blueprint_info()
            
            # Display results
            self.display_results(header, blueprint_info)
            
            self.status_var.set("Analysis complete")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")
            self.status_var.set("Error occurred")
            
    def display_results(self, header: Optional[Dict[str, Any]], blueprint_info: Dict[str, Any]):
        """Display the analysis results in the text widget."""
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Format and display results
        result_text = "=== UE4 Blueprint Analysis Results ===\n\n"
        
        if header:
            result_text += "Header Information:\n"
            for key, value in header.items():
                result_text += f"  {key}: {value}\n"
            result_text += "\n"
            
        if blueprint_info:
            result_text += "Blueprint Information:\n"
            for key, value in blueprint_info.items():
                result_text += f"  {key}: {value}\n"
            result_text += "\n"
            
        # Show version info if available
        version_info = self.reader.get_version_info()
        if version_info:
            result_text += "Unreal Engine Version Information:\n"
            for key, value in version_info.items():
                result_text += f"  {key}: {value}\n"
            result_text += "\n"
            
        # Show supported versions
        supported_versions = self.reader.list_supported_versions()
        result_text += "Supported UE4 Versions:\n"
        for i, version in enumerate(supported_versions):
            if i % 5 == 0 and i > 0:
                result_text += "\n"
            result_text += f"{version} "
        result_text += "\n\n"
        
        # Add some helpful information
        result_text += "=== Notes ===\n"
        result_text += "This is a basic implementation. For full blueprint parsing:\n"
        result_text += "- Use UE4's own tools (UnrealPak, UModel)\n"
        result_text += "- Consider specialized libraries like unreal-engine-parser\n"
        result_text += "- Access UE4's C++ APIs directly for complete functionality\n"
        
        self.results_text.insert(1.0, result_text)
        
        # Scroll to top
        self.results_text.see(1.0)
        
    def clear_results(self):
        """Clear the results display."""
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Results cleared")


def main():
    """Main function to run the UI."""
    root = tk.Tk()
    app = BlueprintReaderUI(root)
    
    # Set window icon (if available)
    try:
        root.iconbitmap('ue_icon.ico')  # This will only work if the file exists
    except:
        pass  # Ignore if icon file not found
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()