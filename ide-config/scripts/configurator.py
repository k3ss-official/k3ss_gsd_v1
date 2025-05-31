#!/usr/bin/env python3
"""
configurator.py - Configuration management for Dev Environment Readyifier

This script handles the configuration of development environments, including
IDE settings, extensions, and AI assistant rules.
"""

import os
import sys
import json
from pathlib import Path

class EnvironmentConfigurator:
    """Manages the configuration of development environments."""
    
    def __init__(self, detection_results=None):
        """Initialize the configuration manager with detection results."""
        self.detection_results = detection_results or {}
        self.selected_tools = {}
        self.security_level = "standard"
        self.config_options = {}
    
    def run_interactive_setup(self):
        """Run the interactive setup process."""
        print("\n" + "="*60)
        print("  DEVELOPMENT ENVIRONMENT CONFIGURATION")
        print("="*60)
        
        self._select_tools_to_configure()
        self._configure_security_level()
        self._configure_ai_personality()
        self._confirm_selections()
        
        # Return the configuration
        return {
            "selected_tools": self.selected_tools,
            "security_level": self.security_level,
            "options": self.config_options
        }
    
    def _select_tools_to_configure(self):
        """Select which tools to configure."""
        print("\nSelect tools to configure:")
        
        # Configure IDEs
        if "ides" in self.detection_results:
            print("\nDetected IDEs:")
            for ide, info in self.detection_results["ides"].items():
                while True:
                    response = input(f"  Configure {ide.upper()}? (y/n): ").lower()
                    if response in ['y', 'n']:
                        self.selected_tools[ide] = (response == 'y')
                        break
                    print("  Please enter 'y' or 'n'")
        
        # Configure AI tools
        if "ai_tools" in self.detection_results:
            print("\nDetected AI tools:")
            for tool in self.detection_results['ai_tools'].keys():
                while True:
                    response = input(f"  Configure {tool.upper()}? (y/n): ").lower()
                    if response in ['y', 'n']:
                        self.selected_tools[tool] = (response == 'y')
                        break
                    print("  Please enter 'y' or 'n'")
        
        # Ask about reference structure
        print("\nReference Data:")
        while True:
            response = input("  Create reference data structure? (y/n): ").lower()
            if response in ['y', 'n']:
                self.config_options["reference_structure"] = (response == 'y')
                break
            print("  Please enter 'y' or 'n'")
    
    def _configure_security_level(self):
        """Configure security level."""
        print("\n" + "="*60)
        print("  SECURITY CONFIGURATION")
        print("="*60)
        print("\nSelect security level:")
        print("  1. Standard - Recommended security practices")
        print("  2. Enhanced - Additional security measures and hardening")
        
        while True:
            response = input("\nSelect security level (1/2): ")
            if response in ['1', '2']:
                self.security_level = "standard" if response == '1' else "enhanced"
                break
            print("  Please enter '1' or '2'")
    
    def _configure_ai_personality(self):
        """Configure AI assistant personality."""
        print("\n" + "="*60)
        print("  AI ASSISTANT CONFIGURATION")
        print("="*60)
        print("\nSelect AI assistant personality profile:")
        print("  1. Default - Based on provided personality profile")
        print("  2. Custom - Modify personality traits")
        
        while True:
            response = input("\nSelect personality profile (1/2): ")
            if response in ['1', '2']:
                if response == '1':
                    self.config_options["ai_personality"] = "default"
                else:
                    self._customize_ai_personality()
                break
            print("  Please enter '1' or '2'")
    
    def _customize_ai_personality(self):
        """Allow customization of AI personality traits."""
        print("\nCustomize AI personality traits:")
        print("  This will create a custom personality profile.")
        
        # Placeholder for actual customization
        # In a real implementation, this would allow detailed customization
        print("  Using default personality profile for now.")
        print("  (Full customization will be implemented in a future version)")
        
        self.config_options["ai_personality"] = "default"
    
    def _confirm_selections(self):
        """Confirm all selections before proceeding."""
        print("\n" + "="*60)
        print("  CONFIGURATION SUMMARY")
        print("="*60)
        
        print("\nSelected tools to configure:")
        for tool, selected in self.selected_tools.items():
            if selected:
                print(f"  ✓ {tool.upper()}")
        
        print(f"\nSecurity level: {self.security_level.upper()}")
        print(f"AI personality: {self.config_options.get('ai_personality', 'default').upper()}")
        print(f"Reference structure: {'Yes' if self.config_options.get('reference_structure', True) else 'No'}")
        
        print("\nReady to apply these configurations?")
        while True:
            response = input("Proceed with configuration? (y/n): ").lower()
            if response == 'y':
                print("\nProceeding with configuration...")
                return
            elif response == 'n':
                print("\nConfiguration cancelled. Exiting...")
                sys.exit(0)
            else:
                print("  Please enter 'y' or 'n'")

# For backward compatibility
ConfigurationManager = EnvironmentConfigurator

if __name__ == "__main__":
    # For testing purposes, create a sample detection result
    sample_detection = {
        "os_info": {
            "system": "Darwin",
            "release": "21.6.0",
            "python_version": "3.9.7"
        },
        "ides": {
            "vscode": {"version": "1.77.0"},
            "vscode_insiders": {"version": "1.78.0-insider"}
        },
        "ai_tools": {
            "cline": {"version": "0.5.2"},
            "aider": {"version": "0.14.1"}
        },
        "conda_environments": [
            {"name": "base", "path": "/opt/conda"},
            {"name": "project1", "path": "/opt/conda/envs/project1"}
        ],
        "vscode_extensions": [
            {"id": "ms-python.python", "name": "python"},
            {"id": "github.copilot", "name": "copilot"}
        ]
    }
    
    # Run the configuration manager with sample data
    config_manager = EnvironmentConfigurator(sample_detection)
    config = config_manager.run_interactive_setup()
    
    print("\nConfiguration complete!")
    print(f"Configuration: {json.dumps(config, indent=2)}")
