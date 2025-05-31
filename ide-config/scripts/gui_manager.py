#!/usr/bin/env python3
"""
gui_manager.py - GUI interface for Dev Environment Readyifier

This script provides a modern dashboard interface for the Dev Environment Readyifier,
with scanning visualization, environment detection, extension management, and
security hardening features.
"""

import os
import sys
import json
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, font
from typing import Dict, List, Any, Optional

class GUIManager:
    """Manages the GUI interface for the Dev Environment Readyifier."""
    
    def __init__(
        self,
        environments: Dict[str, Any],
        missing_extensions: Dict[str, Dict[str, List[Any]]],
        large_files: List[tuple],
        extension_manager,
        repo_context_manager,
        file_structure_manager
    ):
        """Initialize the GUI manager."""
        self.environments = environments
        self.missing_extensions = missing_extensions or {}
        self.large_files = large_files or []
        self.extension_manager = extension_manager
        self.repo_context_manager = repo_context_manager
        self.file_structure_manager = file_structure_manager
        
        # Selected items
        self.selected_extensions = {}
        self.selected_md_files = []
        self.selected_files = []
        self.selected_ides = []
        
        # Initialize GUI
        self.root = None
        self.style = None
        self.notebook = None
        self.current_page = 0
        self.pages = []
        
        # Dashboard elements
        self.progress_var = None
        self.status_var = None
        self.log_text = None
    
    def run(self):
        """Run the GUI."""
        self.root = tk.Tk()
        self.root.title("IDE Config Dashboard")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set style
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a modern theme
        
        # Configure colors
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Subheader.TLabel", font=("Arial", 12, "bold"))
        self.style.configure("Dashboard.TFrame", background="#ffffff")
        
        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        ttk.Label(
            header_frame, 
            text="IDE Config Dashboard", 
            style="Header.TLabel"
        ).pack(side=tk.LEFT)
        
        # Create content area with notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create pages
        self.create_welcome_page()
        self.create_scanning_page()
        self.create_detection_page()
        self.create_selection_page()
        self.create_configuration_page()
        self.create_verification_page()
        
        # Show first page
        self.show_page(0)
        
        # Create footer with status
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.status_var = tk.StringVar(value="Ready to start")
        status_label = ttk.Label(footer_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar(value=0)
        progress_bar = ttk.Progressbar(
            footer_frame, 
            variable=self.progress_var,
            length=200
        )
        progress_bar.pack(side=tk.RIGHT)
        
        # Start the main loop
        self.root.mainloop()
    
    def create_welcome_page(self):
        """Create the welcome page."""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Welcome")
        self.pages.append(page)
        
        # Welcome content
        welcome_frame = ttk.Frame(page, style="Dashboard.TFrame")
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Logo or icon could go here
        ttk.Label(
            welcome_frame, 
            text="Welcome to IDE Config Dashboard", 
            style="Header.TLabel"
        ).pack(pady=(40, 20))
        
        ttk.Label(
            welcome_frame,
            text="This tool will help you configure your development environment with best practices",
            wraplength=600
        ).pack(pady=(0, 20))
        
        ttk.Label(
            welcome_frame,
            text="• Scan your system for installed IDEs and tools\n"
                 "• Detect missing extensions and configurations\n"
                 "• Apply security hardening based on expert recommendations\n"
                 "• Configure AI coding assistants with optimal rules\n"
                 "• Set up project templates and reference files",
            justify=tk.LEFT,
            wraplength=600
        ).pack(pady=(0, 40))
        
        ttk.Button(
            welcome_frame,
            text="Start Scanning",
            command=lambda: self.start_scanning()
        ).pack(pady=(0, 40))
        
        # Version info
        ttk.Label(
            welcome_frame,
            text="Version 1.0.0",
            font=("Arial", 8)
        ).pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)
    
    def create_scanning_page(self):
        """Create the scanning page with visualization."""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Scanning")
        self.pages.append(page)
        
        # Scanning content
        scanning_frame = ttk.Frame(page, style="Dashboard.TFrame")
        scanning_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            scanning_frame, 
            text="Scanning Your System", 
            style="Header.TLabel"
        ).pack(pady=(40, 20))
        
        # Scanning animation placeholder
        canvas = tk.Canvas(scanning_frame, width=400, height=200, bg="white", highlightthickness=0)
        canvas.pack(pady=(0, 20))
        
        # Create scanning animation
        self.scanning_progress = ttk.Progressbar(
            scanning_frame, 
            mode="indeterminate",
            length=400
        )
        self.scanning_progress.pack(pady=(0, 20))
        
        # Scanning status
        self.scanning_status = tk.StringVar(value="Preparing to scan...")
        ttk.Label(
            scanning_frame,
            textvariable=self.scanning_status,
            wraplength=600
        ).pack(pady=(0, 40))
        
        # Log area
        log_frame = ttk.Frame(scanning_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(
            log_frame,
            text="Scan Log:",
            anchor=tk.W
        ).pack(fill=tk.X)
        
        self.log_text = tk.Text(log_frame, height=10, width=60)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text.config(yscrollcommand=log_scrollbar.set)
    
    def create_detection_page(self):
        """Create the detection results page."""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Detection")
        self.pages.append(page)
        
        # Detection content
        detection_frame = ttk.Frame(page, style="Dashboard.TFrame")
        detection_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            detection_frame, 
            text="Detection Results", 
            style="Header.TLabel"
        ).pack(pady=(20, 20))
        
        # Create notebook for detection categories
        detection_notebook = ttk.Notebook(detection_frame)
        detection_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # System info tab
        system_frame = ttk.Frame(detection_notebook)
        detection_notebook.add(system_frame, text="System Info")
        
        # IDEs tab
        ides_frame = ttk.Frame(detection_notebook)
        detection_notebook.add(ides_frame, text="IDEs")
        
        # AI Tools tab
        ai_tools_frame = ttk.Frame(detection_notebook)
        detection_notebook.add(ai_tools_frame, text="AI Tools")
        
        # Extensions tab
        extensions_frame = ttk.Frame(detection_notebook)
        detection_notebook.add(extensions_frame, text="Extensions")
        
        # Conda Environments tab
        conda_frame = ttk.Frame(detection_notebook)
        detection_notebook.add(conda_frame, text="Conda Environments")
        
        # Navigation buttons
        button_frame = ttk.Frame(detection_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="Back",
            command=lambda: self.show_page(1)
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            button_frame,
            text="Continue",
            command=lambda: self.show_page(3)
        ).pack(side=tk.RIGHT)
        
        # Store frames for later population
        self.detection_frames = {
            "system": system_frame,
            "ides": ides_frame,
            "ai_tools": ai_tools_frame,
            "extensions": extensions_frame,
            "conda": conda_frame
        }
    
    def create_selection_page(self):
        """Create the selection page."""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Selection")
        self.pages.append(page)
        
        # Selection content
        selection_frame = ttk.Frame(page, style="Dashboard.TFrame")
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            selection_frame, 
            text="Select Items to Configure", 
            style="Header.TLabel"
        ).pack(pady=(20, 20))
        
        # Create notebook for selection categories
        selection_notebook = ttk.Notebook(selection_frame)
        selection_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # IDEs tab
        ides_frame = ttk.Frame(selection_notebook)
        selection_notebook.add(ides_frame, text="IDEs")
        
        # Extensions tab
        extensions_frame = ttk.Frame(selection_notebook)
        selection_notebook.add(extensions_frame, text="Extensions")
        
        # Files tab
        files_frame = ttk.Frame(selection_notebook)
        selection_notebook.add(files_frame, text="Files")
        
        # Templates tab
        templates_frame = ttk.Frame(selection_notebook)
        selection_notebook.add(templates_frame, text="Templates")
        
        # Navigation buttons
        button_frame = ttk.Frame(selection_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="Back",
            command=lambda: self.show_page(2)
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            button_frame,
            text="Continue",
            command=lambda: self.show_page(4)
        ).pack(side=tk.RIGHT)
        
        # Store frames for later population
        self.selection_frames = {
            "ides": ides_frame,
            "extensions": extensions_frame,
            "files": files_frame,
            "templates": templates_frame
        }
    
    def create_configuration_page(self):
        """Create the configuration page."""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Configuration")
        self.pages.append(page)
        
        # Configuration content
        config_frame = ttk.Frame(page, style="Dashboard.TFrame")
        config_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            config_frame, 
            text="Applying Configuration", 
            style="Header.TLabel"
        ).pack(pady=(20, 20))
        
        # Configuration progress
        self.config_progress = ttk.Progressbar(
            config_frame, 
            mode="determinate",
            length=600
        )
        self.config_progress.pack(pady=(20, 20))
        
        # Configuration status
        self.config_status = tk.StringVar(value="Ready to apply configuration")
        ttk.Label(
            config_frame,
            textvariable=self.config_status,
            wraplength=600
        ).pack(pady=(0, 20))
        
        # Configuration log
        log_frame = ttk.Frame(config_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(
            log_frame,
            text="Configuration Log:",
            anchor=tk.W
        ).pack(fill=tk.X)
        
        self.config_log = tk.Text(log_frame, height=15, width=70)
        self.config_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        config_log_scrollbar = ttk.Scrollbar(log_frame, command=self.config_log.yview)
        config_log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.config_log.config(yscrollcommand=config_log_scrollbar.set)
        
        # Navigation buttons
        button_frame = ttk.Frame(config_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="Back",
            command=lambda: self.show_page(3)
        ).pack(side=tk.LEFT)
        
        self.apply_button = ttk.Button(
            button_frame,
            text="Apply Configuration",
            command=self.apply_configuration
        )
        self.apply_button.pack(side=tk.RIGHT)
        
        self.next_button = ttk.Button(
            button_frame,
            text="Continue",
            command=lambda: self.show_page(5),
            state=tk.DISABLED
        )
        self.next_button.pack(side=tk.RIGHT, padx=(0, 10))
    
    def create_verification_page(self):
        """Create the verification page."""
        page = ttk.Frame(self.notebook)
        self.notebook.add(page, text="Verification")
        self.pages.append(page)
        
        # Verification content
        verify_frame = ttk.Frame(page, style="Dashboard.TFrame")
        verify_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            verify_frame, 
            text="Verification Complete", 
            style="Header.TLabel"
        ).pack(pady=(40, 20))
        
        # Success icon placeholder
        canvas = tk.Canvas(verify_frame, width=100, height=100, bg="white", highlightthickness=0)
        canvas.pack(pady=(0, 20))
        
        # Draw checkmark
        canvas.create_oval(10, 10, 90, 90, outline="#4CAF50", width=5)
        canvas.create_line(30, 50, 45, 65, width=5, fill="#4CAF50")
        canvas.create_line(45, 65, 75, 35, width=5, fill="#4CAF50")
        
        ttk.Label(
            verify_frame,
            text="Your development environment has been successfully configured!",
            wraplength=600,
            font=("Arial", 12)
        ).pack(pady=(0, 20))
        
        # Summary frame
        summary_frame = ttk.Frame(verify_frame)
        summary_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(
            summary_frame,
            text="Configuration Summary:",
            style="Subheader.TLabel",
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 10))
        
        self.summary_text = tk.Text(summary_frame, height=10, width=70)
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        summary_scrollbar = ttk.Scrollbar(summary_frame, command=self.summary_text.yview)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.summary_text.config(yscrollcommand=summary_scrollbar.set)
        
        # Next steps
        ttk.Label(
            verify_frame,
            text="Next Steps:",
            style="Subheader.TLabel",
            anchor=tk.W
        ).pack(fill=tk.X, padx=20, pady=(20, 10))
        
        ttk.Label(
            verify_frame,
            text="1. Restart your IDE to apply all changes\n"
                 "2. Open a project to test the new configuration\n"
                 "3. Check the generated documentation in your project",
            justify=tk.LEFT,
            wraplength=600
        ).pack(padx=20, pady=(0, 20))
        
        # Finish button
        ttk.Button(
            verify_frame,
            text="Finish",
            command=self.root.destroy
        ).pack(pady=(0, 40))
    
    def show_page(self, page_index):
        """Show the specified page."""
        if 0 <= page_index < len(self.pages):
            self.notebook.select(page_index)
            self.current_page = page_index
            
            # Special handling for specific pages
            if page_index == 1:  # Scanning page
                pass  # Scanning is started by the Start Scanning button
            elif page_index == 2:  # Detection page
                self.populate_detection_page()
            elif page_index == 3:  # Selection page
                self.populate_selection_page()
    
    def start_scanning(self):
        """Start the scanning process."""
        self.show_page(1)
        self.scanning_progress.start()
        self.scanning_status.set("Scanning your system for development environments...")
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Start scanning in a separate thread
        threading.Thread(target=self._scanning_thread).start()
    
    def _scanning_thread(self):
        """Scanning thread to avoid blocking the UI."""
        try:
            # Simulate scanning steps
            self._update_log("Starting system scan...")
            time.sleep(0.5)
            
            # OS detection
            self._update_log("Detecting operating system...")
            os_info = self.environments.get("os_info", {})
            system = os_info.get("system", "Unknown")
            release = os_info.get("release", "Unknown")
            python_version = os_info.get("python_version", "Unknown")
            self._update_log(f"Found: {system} {release} with Python {python_version}")
            time.sleep(0.5)
            
            # IDE detection
            self._update_log("Scanning for installed IDEs...")
            ides = self.environments.get("ides", {})
            for ide_name, ide_info in ides.items():
                self._update_log(f"Found: {ide_name} ({ide_info.get('version', 'Unknown')})")
                time.sleep(0.3)
            
            if not ides:
                self._update_log("No IDEs detected")
            
            # AI tools detection
            self._update_log("Scanning for AI coding tools...")
            ai_tools = self.environments.get("ai_tools", {})
            for tool_name, tool_info in ai_tools.items():
                self._update_log(f"Found: {tool_name} ({tool_info.get('version', 'Unknown')})")
                time.sleep(0.3)
            
            if not ai_tools:
                self._update_log("No AI coding tools detected")
            
            # Extensions detection
            self._update_log("Checking for installed extensions...")
            vscode_extensions = self.environments.get("vscode_extensions", [])
            if vscode_extensions:
                self._update_log(f"Found {len(vscode_extensions)} VS Code extensions")
            else:
                self._update_log("No VS Code extensions detected")
            
            # Conda environments detection
            self._update_log("Scanning for Conda environments...")
            conda_envs = self.environments.get("conda_environments", [])
            for env in conda_envs:
                self._update_log(f"Found: {env.get('name', 'Unknown')}")
                time.sleep(0.2)
            
            if not conda_envs:
                self._update_log("No Conda environments detected")
            
            # Missing extensions check
            self._update_log("Checking for missing recommended extensions...")
            if self.missing_extensions:
                total_missing = sum(
                    sum(len(exts) for exts in categories.values())
                    for categories in self.missing_extensions.values()
                )
                self._update_log(f"Found {total_missing} missing recommended extensions")
            else:
                self._update_log("No missing extensions detected")
            
            # File size check
            self._update_log("Checking file sizes...")
            if self.large_files:
                self._update_log(f"Found {len(self.large_files)} files exceeding the recommended 200-line limit")
            else:
                self._update_log("No files exceed the 200-line limit")
            
            # Complete
            self._update_log("Scan complete!")
            self.scanning_status.set("Scan complete! Click Continue to view results.")
            
            # Stop progress bar
            self.root.after(0, self.scanning_progress.stop)
            
            # Add continue button
            self.root.after(0, self._add_continue_button)
            
        except Exception as e:
            self._update_log(f"Error during scanning: {e}")
            self.scanning_status.set(f"Error: {e}")
            self.root.after(0, self.scanning_progress.stop)
    
    def _add_continue_button(self):
        """Add continue button to scanning page."""
        continue_button = ttk.Button(
            self.pages[1],
            text="Continue",
            command=lambda: self.show_page(2)
        )
        continue_button.pack(side=tk.BOTTOM, pady=(0, 20))
    
    def _update_log(self, message):
        """Update the log with a message."""
        self.root.after(0, lambda: self._update_log_ui(message))
    
    def _update_log_ui(self, message):
        """Update the log UI with a message."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def populate_detection_page(self):
        """Populate the detection page with results."""
        # Clear existing content
        for frame in self.detection_frames.values():
            for widget in frame.winfo_children():
                widget.destroy()
        
        # System info
        system_frame = self.detection_frames["system"]
        os_info = self.environments.get("os_info", {})
        
        ttk.Label(
            system_frame,
            text="System Information",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        system_info = ttk.Frame(system_frame)
        system_info.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create a two-column layout
        row = 0
        for label, value in [
            ("Operating System:", f"{os_info.get('system', 'Unknown')} {os_info.get('release', 'Unknown')}"),
            ("Python Version:", os_info.get("python_version", "Unknown")),
        ]:
            ttk.Label(system_info, text=label).grid(row=row, column=0, sticky=tk.W, padx=(0, 10), pady=5)
            ttk.Label(system_info, text=value).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1
        
        # IDEs
        ides_frame = self.detection_frames["ides"]
        ides = self.environments.get("ides", {})
        
        ttk.Label(
            ides_frame,
            text="Detected IDEs",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        if ides:
            ide_tree = ttk.Treeview(ides_frame, columns=("version", "path"), show="headings")
            ide_tree.heading("version", text="Version")
            ide_tree.heading("path", text="Path")
            ide_tree.column("version", width=100)
            ide_tree.column("path", width=400)
            ide_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            for ide_name, ide_info in ides.items():
                ide_tree.insert("", tk.END, text=ide_name, values=(
                    ide_info.get("version", "Unknown"),
                    ide_info.get("path", "Unknown")
                ))
        else:
            ttk.Label(
                ides_frame,
                text="No IDEs detected",
                foreground="gray"
            ).pack(pady=20)
        
        # AI Tools
        ai_tools_frame = self.detection_frames["ai_tools"]
        ai_tools = self.environments.get("ai_tools", {})
        
        ttk.Label(
            ai_tools_frame,
            text="Detected AI Tools",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        if ai_tools:
            tool_tree = ttk.Treeview(ai_tools_frame, columns=("version", "path"), show="headings")
            tool_tree.heading("version", text="Version")
            tool_tree.heading("path", text="Path")
            tool_tree.column("version", width=100)
            tool_tree.column("path", width=400)
            tool_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            for tool_name, tool_info in ai_tools.items():
                tool_tree.insert("", tk.END, text=tool_name, values=(
                    tool_info.get("version", "Unknown"),
                    tool_info.get("path", "Unknown")
                ))
        else:
            ttk.Label(
                ai_tools_frame,
                text="No AI tools detected",
                foreground="gray"
            ).pack(pady=20)
        
        # Extensions
        extensions_frame = self.detection_frames["extensions"]
        vscode_extensions = self.environments.get("vscode_extensions", [])
        
        ttk.Label(
            extensions_frame,
            text="Detected Extensions",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        if vscode_extensions:
            ext_tree = ttk.Treeview(extensions_frame, columns=("id", "version"), show="headings")
            ext_tree.heading("id", text="ID")
            ext_tree.heading("version", text="Version")
            ext_tree.column("id", width=300)
            ext_tree.column("version", width=100)
            ext_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            for ext in vscode_extensions:
                ext_tree.insert("", tk.END, text=ext.get("name", "Unknown"), values=(
                    ext.get("id", "Unknown"),
                    ext.get("version", "Unknown")
                ))
        else:
            ttk.Label(
                extensions_frame,
                text="No extensions detected",
                foreground="gray"
            ).pack(pady=20)
        
        # Conda Environments
        conda_frame = self.detection_frames["conda"]
        conda_envs = self.environments.get("conda_environments", [])
        
        ttk.Label(
            conda_frame,
            text="Detected Conda Environments",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        if conda_envs:
            conda_tree = ttk.Treeview(conda_frame, columns=("path",), show="headings")
            conda_tree.heading("path", text="Path")
            conda_tree.column("path", width=500)
            conda_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            for env in conda_envs:
                conda_tree.insert("", tk.END, text=env.get("name", "Unknown"), values=(
                    env.get("path", "Unknown"),
                ))
        else:
            ttk.Label(
                conda_frame,
                text="No Conda environments detected",
                foreground="gray"
            ).pack(pady=20)
    
    def populate_selection_page(self):
        """Populate the selection page with options."""
        # Clear existing content
        for frame in self.selection_frames.values():
            for widget in frame.winfo_children():
                widget.destroy()
        
        # IDEs selection
        ides_frame = self.selection_frames["ides"]
        ides = self.environments.get("ides", {})
        
        ttk.Label(
            ides_frame,
            text="Select IDEs to Configure",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        if ides:
            # Create checkbuttons for each IDE
            self.ide_vars = {}
            for ide_name in ides.keys():
                var = tk.BooleanVar(value=True)  # Default to selected
                self.ide_vars[ide_name] = var
                
                ttk.Checkbutton(
                    ides_frame,
                    text=f"{ide_name} ({ides[ide_name].get('version', 'Unknown')})",
                    variable=var
                ).pack(anchor=tk.W, padx=20, pady=5)
        else:
            ttk.Label(
                ides_frame,
                text="No IDEs detected",
                foreground="gray"
            ).pack(pady=20)
        
        # Extensions selection
        extensions_frame = self.selection_frames["extensions"]
        
        ttk.Label(
            extensions_frame,
            text="Select Extensions to Install",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        if self.missing_extensions:
            # Create a notebook for each IDE with missing extensions
            extensions_notebook = ttk.Notebook(extensions_frame)
            extensions_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            self.extension_vars = {}
            
            for env_name, categories in self.missing_extensions.items():
                # Create a frame for this IDE
                env_frame = ttk.Frame(extensions_notebook)
                extensions_notebook.add(env_frame, text=env_name)
                
                # Create a section for each category
                for category, extensions in categories.items():
                    if extensions:
                        # Create a LabelFrame for this category
                        category_frame = ttk.LabelFrame(env_frame, text=category.title())
                        category_frame.pack(fill=tk.X, expand=False, padx=10, pady=5)
                        
                        # Create checkbuttons for each extension
                        for ext in extensions:
                            if isinstance(ext, dict):
                                ext_id = ext.get("id", "Unknown")
                                ext_name = ext.get("name", ext_id)
                                
                                if env_name not in self.extension_vars:
                                    self.extension_vars[env_name] = {}
                                
                                if category not in self.extension_vars[env_name]:
                                    self.extension_vars[env_name][category] = {}
                                
                                var = tk.BooleanVar(value=True)  # Default to selected
                                self.extension_vars[env_name][category][ext_id] = var
                                
                                ttk.Checkbutton(
                                    category_frame,
                                    text=f"{ext_name} ({ext_id})",
                                    variable=var
                                ).pack(anchor=tk.W, padx=10, pady=2)
                            else:
                                # Handle string extension IDs
                                if env_name not in self.extension_vars:
                                    self.extension_vars[env_name] = {}
                                
                                if category not in self.extension_vars[env_name]:
                                    self.extension_vars[env_name][category] = {}
                                
                                var = tk.BooleanVar(value=True)  # Default to selected
                                self.extension_vars[env_name][category][ext] = var
                                
                                ttk.Checkbutton(
                                    category_frame,
                                    text=ext,
                                    variable=var
                                ).pack(anchor=tk.W, padx=10, pady=2)
        else:
            ttk.Label(
                extensions_frame,
                text="No missing extensions detected",
                foreground="gray"
            ).pack(pady=20)
        
        # Files selection
        files_frame = self.selection_frames["files"]
        
        ttk.Label(
            files_frame,
            text="Select Files to Optimize",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        if self.large_files:
            # Create a treeview for large files
            file_tree = ttk.Treeview(files_frame, columns=("lines",), show="headings")
            file_tree.heading("lines", text="Lines")
            file_tree.column("lines", width=100)
            file_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            self.file_vars = {}
            
            for file_path, line_count in self.large_files:
                item_id = file_tree.insert("", tk.END, text=file_path, values=(line_count,))
                self.file_vars[file_path] = (item_id, tk.BooleanVar(value=True))  # Default to selected
            
            # Add select/deselect buttons
            button_frame = ttk.Frame(files_frame)
            button_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
            
            ttk.Button(
                button_frame,
                text="Select All",
                command=lambda: self._select_all_files(True)
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            ttk.Button(
                button_frame,
                text="Deselect All",
                command=lambda: self._select_all_files(False)
            ).pack(side=tk.LEFT)
        else:
            ttk.Label(
                files_frame,
                text="No large files detected",
                foreground="gray"
            ).pack(pady=20)
        
        # Templates selection
        templates_frame = self.selection_frames["templates"]
        
        ttk.Label(
            templates_frame,
            text="Select Templates to Create",
            style="Subheader.TLabel"
        ).pack(pady=(20, 10))
        
        # Create checkbuttons for each template
        self.template_vars = {}
        for template_name, description in [
            ("roadmap.md", "Project roadmap and feature planning"),
            ("architecture.md", "System architecture documentation"),
            ("mvp.md", "Minimum Viable Product definition"),
            ("context.md", "Repository context for AI assistants"),
            ("security.md", "Security guidelines and best practices"),
        ]:
            var = tk.BooleanVar(value=True)  # Default to selected
            self.template_vars[template_name] = var
            
            template_frame = ttk.Frame(templates_frame)
            template_frame.pack(fill=tk.X, padx=20, pady=5)
            
            ttk.Checkbutton(
                template_frame,
                text=template_name,
                variable=var
            ).pack(side=tk.LEFT)
            
            ttk.Label(
                template_frame,
                text=description,
                foreground="gray"
            ).pack(side=tk.LEFT, padx=(10, 0))
    
    def _select_all_files(self, select):
        """Select or deselect all files."""
        for var in self.file_vars.values():
            var[1].set(select)
    
    def apply_configuration(self):
        """Apply the selected configuration."""
        # Disable the apply button
        self.apply_button.config(state=tk.DISABLED)
        
        # Clear log
        self.config_log.delete(1.0, tk.END)
        
        # Collect selected items
        self._collect_selections()
        
        # Start configuration in a separate thread
        threading.Thread(target=self._configuration_thread).start()
    
    def _collect_selections(self):
        """Collect all selected items."""
        # Collect selected IDEs
        self.selected_ides = []
        if hasattr(self, 'ide_vars'):
            for ide_name, var in self.ide_vars.items():
                if var.get():
                    self.selected_ides.append(ide_name)
        
        # Collect selected extensions
        self.selected_extensions = {}
        if hasattr(self, 'extension_vars'):
            for env_name, categories in self.extension_vars.items():
                self.selected_extensions[env_name] = {}
                for category, extensions in categories.items():
                    self.selected_extensions[env_name][category] = []
                    for ext_id, var in extensions.items():
                        if var.get():
                            self.selected_extensions[env_name][category].append(ext_id)
        
        # Collect selected files
        self.selected_files = []
        if hasattr(self, 'file_vars'):
            for file_path, (_, var) in self.file_vars.items():
                if var.get():
                    self.selected_files.append(file_path)
        
        # Collect selected templates
        self.selected_md_files = []
        if hasattr(self, 'template_vars'):
            for template_name, var in self.template_vars.items():
                if var.get():
                    self.selected_md_files.append(template_name)
    
    def _configuration_thread(self):
        """Configuration thread to avoid blocking the UI."""
        try:
            # Update status
            self.root.after(0, lambda: self.config_status.set("Applying configuration..."))
            
            # Set progress to indeterminate
            self.root.after(0, lambda: self.config_progress.config(mode="indeterminate"))
            self.root.after(0, self.config_progress.start)
            
            # Log selected items
            self._update_config_log("Selected configuration:")
            self._update_config_log(f"- IDEs: {', '.join(self.selected_ides) if self.selected_ides else 'None'}")
            
            ext_count = sum(
                sum(len(exts) for exts in categories.values())
                for categories in self.selected_extensions.values()
            )
            self._update_config_log(f"- Extensions: {ext_count}")
            
            self._update_config_log(f"- Files: {len(self.selected_files)}")
            self._update_config_log(f"- Templates: {', '.join(self.selected_md_files) if self.selected_md_files else 'None'}")
            self._update_config_log("")
            
            # Apply configuration
            self._update_config_log("Starting configuration process...")
            
            # Install extensions
            if self.selected_extensions:
                self._update_config_log("Installing extensions...")
                for env_name, categories in self.selected_extensions.items():
                    for category, ext_ids in categories.items():
                        if ext_ids:
                            self._update_config_log(f"  Installing {len(ext_ids)} extensions for {env_name} ({category})...")
                            # Convert extension IDs to proper format for installer
                            selections = {env_name: {category: ext_ids}}
                            results = self.extension_manager.install_selected_extensions(selections)
                            self._update_config_log(f"    Successfully installed: {len(results['success'])}")
                            self._update_config_log(f"    Failed installations: {len(results['failed'])}")
            
            # Create specialized markdown files
            if self.selected_md_files:
                self._update_config_log("Creating specialized markdown files...")
                for filename in self.selected_md_files:
                    self._update_config_log(f"  Creating {filename}...")
                
                # Filter md_files to only include selected ones
                filtered_md_files = {k: v for k, v in self.repo_context_manager.md_files.items() if k in self.selected_md_files}
                self.repo_context_manager.md_files = filtered_md_files
                results = self.repo_context_manager.create_specialized_md_files()
                for filename, status in results.items():
                    self._update_config_log(f"    {status}")
            
            # Add file annotations
            self._update_config_log("Adding file annotations...")
            modified_files = self.file_structure_manager.add_file_annotations()
            self._update_config_log(f"  Added annotations to {len(modified_files)} files")
            
            # Analyze large files
            if self.selected_files:
                self._update_config_log("Analyzing large files...")
                suggestions = self.file_structure_manager.suggest_file_splits()
                for suggestion in suggestions:
                    self._update_config_log(f"  {suggestion['file']}: {suggestion['split_suggestion']}")
            
            # Generate repository context prompt
            self._update_config_log("Generating repository context prompt...")
            prompt = self.repo_context_manager.generate_repo_prompt()
            prompt_file = os.path.join(self.repo_context_manager.repo_path, "repo_prompt.md")
            with open(prompt_file, 'w') as f:
                f.write(prompt)
            self._update_config_log(f"  Saved prompt to {prompt_file}")
            
            # Complete
            self._update_config_log("\nConfiguration complete!")
            
            # Update status
            self.root.after(0, lambda: self.config_status.set("Configuration complete!"))
            
            # Stop progress bar
            self.root.after(0, self.config_progress.stop)
            self.root.after(0, lambda: self.config_progress.config(mode="determinate", value=100))
            
            # Enable next button
            self.root.after(0, lambda: self.next_button.config(state=tk.NORMAL))
            
            # Prepare summary for verification page
            summary = f"Configuration Summary:\n\n"
            summary += f"- IDEs configured: {len(self.selected_ides)}\n"
            summary += f"- Extensions installed: {ext_count}\n"
            summary += f"- Files annotated: {len(modified_files)}\n"
            summary += f"- Templates created: {len(self.selected_md_files)}\n\n"
            
            if self.selected_ides:
                summary += "Configured IDEs:\n"
                for ide in self.selected_ides:
                    summary += f"- {ide}\n"
                summary += "\n"
            
            self.root.after(0, lambda: self.summary_text.insert(tk.END, summary))
            
        except Exception as e:
            self._update_config_log(f"Error during configuration: {e}")
            self.root.after(0, lambda: self.config_status.set(f"Error: {e}"))
            self.root.after(0, self.config_progress.stop)
            
            # Re-enable apply button
            self.root.after(0, lambda: self.apply_button.config(state=tk.NORMAL))
    
    def _update_config_log(self, message):
        """Update the configuration log with a message."""
        self.root.after(0, lambda: self._update_config_log_ui(message))
    
    def _update_config_log_ui(self, message):
        """Update the configuration log UI with a message."""
        self.config_log.insert(tk.END, message + "\n")
        self.config_log.see(tk.END)
        self.root.update_idletasks()

# Example usage
if __name__ == "__main__":
    import sys
    
    print("This module should be imported and used by setup.py.")
    print("Run setup.py to start the Dev Environment Readyifier.")
    sys.exit(1)
