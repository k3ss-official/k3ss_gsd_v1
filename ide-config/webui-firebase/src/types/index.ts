
import type React from 'react';

export const STEPS = [
  "welcome",
  "scanning",
  "results",
  "configuring",
  "complete",
] as const;

export type Step = typeof STEPS[number];

export interface DetectedIDE {
  id: string;
  name: string;
  version: string;
  path: string;
  status: "configured" | "needs_config" | "error";
  icon?: React.ComponentType<{ className?: string }>;
  missingExtensions?: string[];
  recommendedConfig?: string;
}

export interface RecommendedExtension {
  id: string;
  name: string;
  description: string;
  reasoning?: string;
}

export interface ConfigurationLog {
  id: string;
  timestamp: string;
  message: string;
  type: "info" | "success" | "error" | "warning";
}

export const PROJECT_TYPES = [
  "Web Application (Frontend/Fullstack)",
  "Backend Services / APIs",
  "Mobile Application (Native/Cross-platform)",
  "Data Science / Machine Learning",
  "Game Development",
  "DevOps / Cloud Infrastructure",
  "Desktop Application",
  "Other",
] as const;
export type ProjectType = typeof PROJECT_TYPES[number];

export interface UserPreferences {
  testing?: string[];
  lintingFormatters?: string[];
  aiAssistance?: string[];
  security?: string[];
  versionControl?: string[];
  collaboration?: string[];
}

// This will be the comprehensive data gathered from the form for AI processing
export interface RecommendationRequestInput {
  ideName: string;
  projectType: ProjectType;
  projectTypeOther?: string; // If "Other" is selected for projectType
  preferences: UserPreferences;
  userNotes?: string; // From "Anything you want to add"
}
