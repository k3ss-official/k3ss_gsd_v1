#!/usr/bin/env python3
"""
detector.py - Environment detection for Dev Environment Readyifier

This script handles the detection of installed development environments,
tools, and extensions.
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

class EnvironmentDetector:
    """Detects installed development environments, tools, and extensions."""
    
    def __init__(self):
        """Initialize the environment detector."""
        self.os_type = platform.system()
        self.os_release = platform.release()
        self.python_version = platform.python_version()
    
    def detect_environments(self) -> Dict[str, Any]:
        """Detect all installed development environments and tools."""
        results = {
            "os_info": {
                "system": self.os_type,
                "release": self.os_release,
                "python_version": self.python_version
            },
            "ides": {},
            "ai_tools": {},
            "conda_environments": self._detect_conda_environments(),
            "vscode_extensions": []
        }
        
        # Detect IDEs
        vscode_path = self._detect_vscode()
        if vscode_path:
            results["ides"]["vscode"] = {
                "version": self._get_vscode_version("vscode"),
                "path": vscode_path
            }
            results["vscode_extensions"] = self._detect_vscode_extensions("vscode")
        
        vscode_insiders_path = self._detect_vscode_insiders()
        if vscode_insiders_path:
            results["ides"]["vscode_insiders"] = {
                "version": self._get_vscode_version("vscode_insiders"),
                "path": vscode_insiders_path
            }
        
        trae_path = self._detect_trae()
        if trae_path:
            results["ides"]["trae"] = {
                "version": "Unknown",  # Would need specific version detection
                "path": trae_path
            }
        
        void_path = self._detect_void()
        if void_path:
            results["ides"]["void"] = {
                "version": "Unknown",  # Would need specific version detection
                "path": void_path
            }
        
        # Detect AI tools
        cline_path = self._detect_cline()
        if cline_path:
            results["ai_tools"]["cline"] = {
                "version": self._get_tool_version("cline"),
                "path": cline_path
            }
        
        roo_path = self._detect_roo()
        if roo_path:
            results["ai_tools"]["roo"] = {
                "version": "Unknown",  # Would need specific version detection
                "path": roo_path
            }
        
        aider_path = self._detect_aider()
        if aider_path:
            results["ai_tools"]["aider"] = {
                "version": self._get_tool_version("aider"),
                "path": aider_path
            }
        
        return results
    
    def _detect_vscode(self) -> Optional[str]:
        """Detect if Visual Studio Code is installed."""
        try:
            if self.os_type == "Darwin":  # macOS
                app_path = "/Applications/Visual Studio Code.app"
                if os.path.exists(app_path):
                    return app_path
                
                # Check if installed via Homebrew
                result = subprocess.run(
                    "which code", 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            elif self.os_type == "Linux":
                result = subprocess.run(
                    "which code", 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            elif self.os_type == "Windows":
                # Check common installation paths
                paths = [
                    os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Microsoft VS Code", "Code.exe"),
                    os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Microsoft VS Code", "Code.exe"),
                    os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\User\\AppData\\Local"), "Programs", "Microsoft VS Code", "Code.exe")
                ]
                for path in paths:
                    if os.path.exists(path):
                        return path
            
            return None
        except Exception:
            return None
    
    def _detect_vscode_insiders(self) -> Optional[str]:
        """Detect if Visual Studio Code Insiders is installed."""
        try:
            if self.os_type == "Darwin":  # macOS
                app_path = "/Applications/Visual Studio Code - Insiders.app"
                if os.path.exists(app_path):
                    return app_path
                
                # Check if installed via Homebrew
                result = subprocess.run(
                    "which code-insiders", 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            elif self.os_type == "Linux":
                result = subprocess.run(
                    "which code-insiders", 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            elif self.os_type == "Windows":
                # Check common installation paths
                paths = [
                    os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Microsoft VS Code Insiders", "Code - Insiders.exe"),
                    os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Microsoft VS Code Insiders", "Code - Insiders.exe"),
                    os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\User\\AppData\\Local"), "Programs", "Microsoft VS Code Insiders", "Code - Insiders.exe")
                ]
                for path in paths:
                    if os.path.exists(path):
                        return path
            
            return None
        except Exception:
            return None
    
    def _detect_trae(self) -> Optional[str]:
        """Detect if Trae IDE is installed."""
        try:
            if self.os_type == "Darwin":  # macOS
                app_path = "/Applications/Trae.app"
                if os.path.exists(app_path):
                    return app_path
            elif self.os_type == "Linux":
                # Check common installation paths
                paths = [
                    "/usr/bin/trae",
                    "/usr/local/bin/trae",
                    os.path.join(str(Path.home()), ".local", "bin", "trae")
                ]
                for path in paths:
                    if os.path.exists(path):
                        return path
            elif self.os_type == "Windows":
                # Check common installation paths
                paths = [
                    os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Trae", "Trae.exe"),
                    os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Trae", "Trae.exe"),
                    os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\User\\AppData\\Local"), "Programs", "Trae", "Trae.exe")
                ]
                for path in paths:
                    if os.path.exists(path):
                        return path
            
            return None
        except Exception:
            return None
    
    def _detect_void(self) -> Optional[str]:
        """Detect if VOID IDE is installed."""
        try:
            if self.os_type == "Darwin":  # macOS
                app_path = "/Applications/VOID.app"
                if os.path.exists(app_path):
                    return app_path
            elif self.os_type == "Linux":
                # Check common installation paths
                paths = [
                    "/usr/bin/void",
                    "/usr/local/bin/void",
                    os.path.join(str(Path.home()), ".local", "bin", "void")
                ]
                for path in paths:
                    if os.path.exists(path):
                        return path
            elif self.os_type == "Windows":
                # Check common installation paths
                paths = [
                    os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "VOID", "VOID.exe"),
                    os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "VOID", "VOID.exe"),
                    os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\User\\AppData\\Local"), "Programs", "VOID", "VOID.exe")
                ]
                for path in paths:
                    if os.path.exists(path):
                        return path
            
            return None
        except Exception:
            return None
    
    def _detect_cline(self) -> Optional[str]:
        """Detect if Cline is installed."""
        try:
            result = subprocess.run(
                "pip show cline", 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return "pip:cline"
            
            return None
        except Exception:
            return None
    
    def _detect_roo(self) -> Optional[str]:
        """Detect if Roo Code is installed."""
        try:
            if self.os_type == "Darwin":  # macOS
                app_path = "/Applications/Roo.app"
                if os.path.exists(app_path):
                    return app_path
            elif self.os_type == "Linux":
                # Check common installation paths
                paths = [
                    "/usr/bin/roo",
                    "/usr/local/bin/roo",
                    os.path.join(str(Path.home()), ".local", "bin", "roo")
                ]
                for path in paths:
                    if os.path.exists(path):
                        return path
            elif self.os_type == "Windows":
                # Check common installation paths
                paths = [
                    os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Roo", "Roo.exe"),
                    os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Roo", "Roo.exe"),
                    os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\User\\AppData\\Local"), "Programs", "Roo", "Roo.exe")
                ]
                for path in paths:
                    if os.path.exists(path):
                        return path
            
            return None
        except Exception:
            return None
    
    def _detect_aider(self) -> Optional[str]:
        """Detect if Aider is installed."""
        try:
            result = subprocess.run(
                "pip show aider-chat", 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return "pip:aider-chat"
            
            return None
        except Exception:
            return None
    
    def _get_vscode_version(self, tool: str) -> str:
        """Get the version of Visual Studio Code or VS Code Insiders."""
        try:
            cmd = "code --version" if tool == "vscode" else "code-insiders --version"
            result = subprocess.run(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                # First line of output is the version
                return result.stdout.strip().split("\n")[0]
            
            return "Unknown"
        except Exception:
            return "Unknown"
    
    def _get_tool_version(self, tool: str) -> str:
        """Get the version of a tool."""
        try:
            cmd = f"pip show {tool}"
            result = subprocess.run(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                # Extract version from pip show output
                for line in result.stdout.strip().split("\n"):
                    if line.startswith("Version:"):
                        return line.split("Version:")[1].strip()
            
            return "Unknown"
        except Exception:
            return "Unknown"
    
    def _detect_conda_environments(self) -> List[Dict[str, str]]:
        """Detect Conda environments."""
        environments = []
        
        try:
            # Check if conda is installed
            result = subprocess.run(
                "conda info --envs --json", 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                try:
                    conda_info = json.loads(result.stdout)
                    for env in conda_info.get("envs", []):
                        env_name = os.path.basename(env)
                        environments.append({
                            "name": env_name,
                            "path": env
                        })
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass
        
        return environments
    
    def _detect_vscode_extensions(self, tool: str) -> List[Dict[str, str]]:
        """Detect installed VS Code extensions."""
        extensions = []
        
        try:
            cmd = "code --list-extensions --show-versions" if tool == "vscode" else "code-insiders --list-extensions --show-versions"
            result = subprocess.run(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        parts = line.split("@")
                        if len(parts) == 2:
                            extensions.append({
                                "id": parts[0],
                                "version": parts[1],
                                "name": parts[0].split(".")[-1]
                            })
                        else:
                            extensions.append({
                                "id": line,
                                "version": "Unknown",
                                "name": line.split(".")[-1]
                            })
        except Exception:
            pass
        
        return extensions

if __name__ == "__main__":
    # For testing purposes
    detector = EnvironmentDetector()
    results = detector.detect_environments()
    print(json.dumps(results, indent=2))
