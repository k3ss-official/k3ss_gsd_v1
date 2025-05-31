#!/usr/bin/env python3
"""
installer.py - Installation management for Dev Environment Readyifier

This script handles the installation of missing tools and application of
configurations for development environments.
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

class ToolInstaller:
    """Manages the installation of missing tools and application of configurations."""
    
    def __init__(self, detection_results=None, config_choices=None):
        """Initialize the installer with detection results and configuration choices."""
        self.detection_results = detection_results or {}
        self.config_choices = config_choices or {}
        self.os_type = platform.system()
        self.repo_base_dir = self._get_repo_base_dir()
    
    def install_missing_tools(self, tools_to_install: List[str]) -> Dict[str, Any]:
        """Install missing tools."""
        results = {
            "success": [],
            "failed": []
        }
        
        print("\n" + "="*60)
        print("  INSTALLING MISSING TOOLS")
        print("="*60)
        
        for tool in tools_to_install:
            print(f"\nInstalling {tool}...")
            if self._install_tool(tool):
                results["success"].append(tool)
                print(f"  ✓ Successfully installed {tool}")
            else:
                results["failed"].append(tool)
                print(f"  ✗ Failed to install {tool}")
        
        return results
    
    def apply_configurations(self) -> Dict[str, Any]:
        """Apply configurations to selected tools."""
        results = {
            "success": [],
            "failed": []
        }
        
        print("\n" + "="*60)
        print("  APPLYING CONFIGURATIONS")
        print("="*60)
        
        # Get selected tools
        selected_tools = self.config_choices.get("selected_tools", {})
        
        # Apply configurations to each selected tool
        for tool, selected in selected_tools.items():
            if selected:
                print(f"\nConfiguring {tool}...")
                if self._configure_tool(tool):
                    results["success"].append(tool)
                    print(f"  ✓ Successfully configured {tool}")
                else:
                    results["failed"].append(tool)
                    print(f"  ✗ Failed to configure {tool}")
        
        # Set up reference structure if selected
        if self.config_choices.get("options", {}).get("reference_structure", False):
            print("\nSetting up reference structure...")
            if self._setup_reference_structure():
                results["success"].append("reference_structure")
                print("  ✓ Successfully set up reference structure")
            else:
                results["failed"].append("reference_structure")
                print("  ✗ Failed to set up reference structure")
        
        return results
    
    def _install_tool(self, tool: str) -> bool:
        """Install a specific tool."""
        try:
            if tool == "vscode":
                return self._install_vscode()
            elif tool == "vscode_insiders":
                return self._install_vscode_insiders()
            elif tool == "trae":
                return self._install_trae()
            elif tool == "void":
                return self._install_void()
            elif tool == "cline":
                return self._install_cline()
            elif tool == "roo":
                return self._install_roo()
            elif tool == "aider":
                return self._install_aider()
            else:
                print(f"  Unknown tool: {tool}")
                return False
        except Exception as e:
            print(f"  Error installing {tool}: {e}")
            return False
    
    def _install_vscode(self) -> bool:
        """Install Visual Studio Code."""
        try:
            if self.os_type == "Darwin":  # macOS
                return self._run_command("brew install --cask visual-studio-code")
            elif self.os_type == "Linux":
                # For Ubuntu/Debian
                return self._run_command("""
                    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg &&
                    sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/ &&
                    sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list' &&
                    rm -f packages.microsoft.gpg &&
                    sudo apt update &&
                    sudo apt install -y code
                """)
            elif self.os_type == "Windows":
                return self._run_command("winget install -e --id Microsoft.VisualStudioCode")
            
            return False
        except Exception as e:
            print(f"  Error installing VS Code: {e}")
            return False
    
    def _install_vscode_insiders(self) -> bool:
        """Install Visual Studio Code Insiders."""
        try:
            if self.os_type == "Darwin":  # macOS
                return self._run_command("brew install --cask visual-studio-code-insiders")
            elif self.os_type == "Linux":
                # For Ubuntu/Debian
                return self._run_command("""
                    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg &&
                    sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/ &&
                    sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list' &&
                    rm -f packages.microsoft.gpg &&
                    sudo apt update &&
                    sudo apt install -y code-insiders
                """)
            elif self.os_type == "Windows":
                return self._run_command("winget install -e --id Microsoft.VisualStudioCode.Insiders")
            
            return False
        except Exception as e:
            print(f"  Error installing VS Code Insiders: {e}")
            return False
    
    def _install_trae(self) -> bool:
        """Install Trae IDE."""
        print("  Trae IDE installation requires manual download from the official website.")
        print("  Please visit https://trae.ai/ to download and install.")
        return False
    
    def _install_void(self) -> bool:
        """Install VOID IDE."""
        print("  VOID IDE installation requires manual download from the official website.")
        print("  Please visit the VOID IDE website to download and install.")
        return False
    
    def _install_cline(self) -> bool:
        """Install Cline."""
        try:
            return self._run_command("pip install --force-reinstall --no-cache-dir cline")
        except Exception as e:
            print(f"  Error installing Cline: {e}")
            return False
    
    def _install_roo(self) -> bool:
        """Install Roo Code."""
        print("  Roo Code installation requires manual download from the official website.")
        print("  Please visit the Roo Code website to download and install.")
        return False
    
    def _install_aider(self) -> bool:
        """Install Aider."""
        try:
            return self._run_command("pip install --force-reinstall --no-cache-dir aider-chat")
        except Exception as e:
            print(f"  Error installing Aider: {e}")
            return False
    
    def _configure_tool(self, tool: str) -> bool:
        """Configure a specific tool."""
        try:
            if tool in ["vscode", "vscode_insiders"]:
                return self._configure_vscode(tool)
            elif tool == "trae":
                return self._configure_trae()
            elif tool == "void":
                return self._configure_void()
            elif tool == "cline":
                return self._configure_cline()
            elif tool == "roo":
                return self._configure_roo()
            elif tool == "aider":
                return self._configure_aider()
            else:
                print(f"  Unknown tool: {tool}")
                return False
        except Exception as e:
            print(f"  Error configuring {tool}: {e}")
            return False
    
    def _configure_vscode(self, tool: str) -> bool:
        """Configure Visual Studio Code or VS Code Insiders."""
        try:
            config_dir = self._get_tool_config_dir(tool)
            if not config_dir:
                print(f"  Could not determine configuration directory for {tool}")
                return False
            
            # Ensure config directory exists
            os.makedirs(config_dir, exist_ok=True)
            
            # Copy .cursorrules
            cursorrules_src = os.path.join(self.repo_base_dir, "templates", "ai_rules", ".cursorrules")
            cursorrules_dest = os.path.join(config_dir, ".cursorrules")
            
            if os.path.exists(cursorrules_src):
                os.makedirs(os.path.dirname(cursorrules_dest), exist_ok=True)
                with open(cursorrules_src, 'r') as src_file:
                    with open(cursorrules_dest, 'w') as dest_file:
                        dest_file.write(src_file.read())
                print(f"  Copied .cursorrules to {cursorrules_dest}")
            
            # Install recommended extensions
            self._install_vscode_extensions(tool)
            
            return True
        except Exception as e:
            print(f"  Error configuring {tool}: {e}")
            return False
    
    def _install_vscode_extensions(self, tool: str) -> bool:
        """Install recommended VS Code extensions."""
        try:
            # Get recommended extensions
            extensions_file = os.path.join(self.repo_base_dir, "templates", "recommended_extensions.json")
            if not os.path.exists(extensions_file):
                print("  Recommended extensions file not found")
                return False
            
            with open(extensions_file, 'r') as f:
                extensions_data = json.load(f)
            
            # Get extensions for the tool
            tool_key = "vscode" if tool == "vscode" or tool == "vscode_insiders" else tool
            if tool_key not in extensions_data:
                print(f"  No recommended extensions found for {tool}")
                return False
            
            extensions = []
            for category, exts in extensions_data[tool_key].items():
                extensions.extend([ext["id"] for ext in exts if "id" in ext])
            
            # Install extensions
            cli_cmd = "code" if tool == "vscode" else "code-insiders"
            for ext_id in extensions:
                print(f"  Installing extension: {ext_id}")
                self._run_command(f"{cli_cmd} --install-extension {ext_id}")
            
            return True
        except Exception as e:
            print(f"  Error installing extensions: {e}")
            return False
    
    def _configure_trae(self) -> bool:
        """Configure Trae IDE."""
        try:
            config_dir = self._get_tool_config_dir("trae")
            if not config_dir:
                print("  Could not determine configuration directory for Trae")
                return False
            
            # Ensure config directory exists
            os.makedirs(config_dir, exist_ok=True)
            
            # Copy .cursorrules
            cursorrules_src = os.path.join(self.repo_base_dir, "templates", "ai_rules", ".cursorrules")
            cursorrules_dest = os.path.join(config_dir, ".cursorrules")
            
            if os.path.exists(cursorrules_src):
                os.makedirs(os.path.dirname(cursorrules_dest), exist_ok=True)
                with open(cursorrules_src, 'r') as src_file:
                    with open(cursorrules_dest, 'w') as dest_file:
                        dest_file.write(src_file.read())
                print(f"  Copied .cursorrules to {cursorrules_dest}")
            
            return True
        except Exception as e:
            print(f"  Error configuring Trae: {e}")
            return False
    
    def _configure_void(self) -> bool:
        """Configure VOID IDE."""
        try:
            config_dir = self._get_tool_config_dir("void")
            if not config_dir:
                print("  Could not determine configuration directory for VOID")
                return False
            
            # Ensure config directory exists
            os.makedirs(config_dir, exist_ok=True)
            
            # Copy .cursorrules
            cursorrules_src = os.path.join(self.repo_base_dir, "templates", "ai_rules", ".cursorrules")
            cursorrules_dest = os.path.join(config_dir, ".cursorrules")
            
            if os.path.exists(cursorrules_src):
                os.makedirs(os.path.dirname(cursorrules_dest), exist_ok=True)
                with open(cursorrules_src, 'r') as src_file:
                    with open(cursorrules_dest, 'w') as dest_file:
                        dest_file.write(src_file.read())
                print(f"  Copied .cursorrules to {cursorrules_dest}")
            
            return True
        except Exception as e:
            print(f"  Error configuring VOID: {e}")
            return False
    
    def _configure_cline(self) -> bool:
        """Configure Cline."""
        try:
            config_dir = self._get_tool_config_dir("cline")
            if not config_dir:
                print("  Could not determine configuration directory for Cline")
                return False
            
            # Ensure config directory exists
            os.makedirs(config_dir, exist_ok=True)
            
            # Copy .cursorrules
            cursorrules_src = os.path.join(self.repo_base_dir, "templates", "ai_rules", ".cursorrules")
            cursorrules_dest = os.path.join(config_dir, ".cursorrules")
            
            if os.path.exists(cursorrules_src):
                os.makedirs(os.path.dirname(cursorrules_dest), exist_ok=True)
                with open(cursorrules_src, 'r') as src_file:
                    with open(cursorrules_dest, 'w') as dest_file:
                        dest_file.write(src_file.read())
                print(f"  Copied .cursorrules to {cursorrules_dest}")
            
            return True
        except Exception as e:
            print(f"  Error configuring Cline: {e}")
            return False
    
    def _configure_roo(self) -> bool:
        """Configure Roo Code."""
        try:
            config_dir = self._get_tool_config_dir("roo")
            if not config_dir:
                print("  Could not determine configuration directory for Roo")
                return False
            
            # Ensure config directory exists
            os.makedirs(config_dir, exist_ok=True)
            
            # Copy .cursorrules
            cursorrules_src = os.path.join(self.repo_base_dir, "templates", "ai_rules", ".cursorrules")
            cursorrules_dest = os.path.join(config_dir, ".cursorrules")
            
            if os.path.exists(cursorrules_src):
                os.makedirs(os.path.dirname(cursorrules_dest), exist_ok=True)
                with open(cursorrules_src, 'r') as src_file:
                    with open(cursorrules_dest, 'w') as dest_file:
                        dest_file.write(src_file.read())
                print(f"  Copied .cursorrules to {cursorrules_dest}")
            
            return True
        except Exception as e:
            print(f"  Error configuring Roo: {e}")
            return False
    
    def _configure_aider(self) -> bool:
        """Configure Aider."""
        try:
            config_dir = self._get_tool_config_dir("aider")
            if not config_dir:
                print("  Could not determine configuration directory for Aider")
                return False
            
            # Ensure config directory exists
            os.makedirs(config_dir, exist_ok=True)
            
            # Copy .cursorrules
            cursorrules_src = os.path.join(self.repo_base_dir, "templates", "ai_rules", ".cursorrules")
            cursorrules_dest = os.path.join(config_dir, ".cursorrules")
            
            if os.path.exists(cursorrules_src):
                os.makedirs(os.path.dirname(cursorrules_dest), exist_ok=True)
                with open(cursorrules_src, 'r') as src_file:
                    with open(cursorrules_dest, 'w') as dest_file:
                        dest_file.write(src_file.read())
                print(f"  Copied .cursorrules to {cursorrules_dest}")
            
            return True
        except Exception as e:
            print(f"  Error configuring Aider: {e}")
            return False
    
    def _setup_reference_structure(self) -> bool:
        """Set up reference data structure."""
        try:
            projects_dir = self._get_projects_dir()
            reference_dir = os.path.join(projects_dir, "reference")
            
            # Create reference directory structure
            os.makedirs(os.path.join(reference_dir, "org_info"), exist_ok=True)
            os.makedirs(os.path.join(reference_dir, "tech_specs"), exist_ok=True)
            os.makedirs(os.path.join(reference_dir, "security"), exist_ok=True)
            os.makedirs(os.path.join(reference_dir, "api_docs"), exist_ok=True)
            
            print(f"  Created reference structure in {reference_dir}")
            return True
        except Exception as e:
            print(f"Error setting up reference structure: {e}")
            return False
    
    def _get_repo_base_dir(self) -> Optional[str]:
        """Get the base directory of the repository."""
        try:
            # Get the directory of this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Go up one level to get the repo base directory
            return os.path.dirname(script_dir)
        except Exception:
            return None
    
    def _get_tool_config_dir(self, tool: str) -> Optional[str]:
        """Get the configuration directory for a specific tool."""
        try:
            if tool == "vscode" or tool == "vscode_insiders":
                if self.os_type == "Darwin":  # macOS
                    return os.path.join(str(Path.home()), "Library", "Application Support", 
                                       "Code" if tool == "vscode" else "Code - Insiders", "User")
                elif self.os_type == "Linux":
                    return os.path.join(str(Path.home()), ".config", 
                                       "Code" if tool == "vscode" else "Code - Insiders", "User")
                elif self.os_type == "Windows":
                    return os.path.join(str(Path.home()), "AppData", "Roaming", 
                                       "Code" if tool == "vscode" else "Code - Insiders", "User")
            elif tool == "trae":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "trae")
            elif tool == "void":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "void")
            elif tool == "cline":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "cline")
            elif tool == "roo":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "roo")
            elif tool == "aider":
                # Placeholder - would need actual config directory
                return os.path.join(str(Path.home()), ".config", "aider")
            
            return None
        except Exception:
            return None
    
    def _get_projects_dir(self) -> str:
        """Get the user's projects directory."""
        # Default to home directory
        projects_dir = str(Path.home())
        
        # Check for common project directories
        common_dirs = [
            os.path.join(str(Path.home()), "projects"),
            os.path.join(str(Path.home()), "Documents", "projects"),
            os.path.join(str(Path.home()), "dev")
        ]
        
        for dir_path in common_dirs:
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                projects_dir = dir_path
                break
        
        return projects_dir
    
    def _run_command(self, command: str) -> bool:
        """Run a shell command and return success status."""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Command failed: {command}")
                print(f"Error: {result.stderr}")
                return False
            
            return True
        except Exception as e:
            print(f"Error running command: {e}")
            return False

if __name__ == "__main__":
    # For testing purposes, create sample data
    sample_detection = {
        "os_info": {
            "system": "Darwin",
            "release": "21.6.0",
            "python_version": "3.9.7"
        },
        "ides": {
            "vscode": {"version": "1.77.0"}
        },
        "ai_tools": {
            "aider": {"version": "0.14.1"}
        }
    }
    
    sample_config = {
        "selected_tools": {
            "vscode": True,
            "aider": True
        },
        "security_level": "standard",
        "options": {
            "ai_personality": "default",
            "reference_structure": True
        }
    }
    
    # Create installer and test
    installer = ToolInstaller(sample_detection, sample_config)
    
    # Test installing missing tools
    print("Testing tool installation...")
    install_results = installer.install_missing_tools(["cline", "roo"])
    print(f"Installation results: {json.dumps(install_results, indent=2)}")
    
    # Test applying configurations
    print("\nTesting configuration application...")
    config_results = installer.apply_configurations()
    print(f"Configuration results: {json.dumps(config_results, indent=2)}")
    
    print("\nInstallation and configuration complete!")
