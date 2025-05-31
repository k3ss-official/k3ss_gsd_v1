'use client';

import { useState, useEffect } from 'react';
import type { Step, DetectedIDE } from "@/types";
import { STEPS } from "@/types";

import { AppContainer } from "@/components/app-container";
import { ProgressIndicator } from "@/components/progress-indicator";
import { WelcomeStep } from "@/components/steps/welcome-step";
import { ScanningStep } from "@/components/steps/scanning-step";
import { ResultsStep } from "@/components/steps/results-step";
import { ConfiguringStep } from "@/components/steps/configuring-step";
import { CompleteStep } from "@/components/steps/complete-step";
import { Skeleton } from '@/components/ui/skeleton';

export default function IdeConfiguratorPage() {
  const [currentStep, setCurrentStep] = useState<Step>("welcome");
  const [detectedIdes, setDetectedIdes] = useState<DetectedIDE[]>([]);
  const [selectedConfig, setSelectedConfig] = useState<{ ideId: string; extensions: string[] } | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate initial loading if needed, or directly set to false
    const timer = setTimeout(() => setIsLoading(false), 200); // Brief delay for effect or actual check
    return () => clearTimeout(timer);
  }, []);


  const handleStartScanning = () => {
    setCurrentStep("scanning");
  };

  const handleScanComplete = (ides: DetectedIDE[]) => {
    setDetectedIdes(ides);
    setCurrentStep("results");
  };

  const handleStartConfiguration = (config: { ideId: string; extensions: string[] }) => {
    setSelectedConfig(config);
    setCurrentStep("configuring");
  };

  const handleConfigurationComplete = () => {
    setCurrentStep("complete");
  };

  const handleRestart = () => {
    setCurrentStep("welcome");
    setDetectedIdes([]);
    setSelectedConfig(null);
  };

  if (isLoading) {
    return (
      <AppContainer>
        <div className="flex flex-col items-center justify-center h-full space-y-6">
          <Skeleton className="h-16 w-1/2" />
          <Skeleton className="h-8 w-3/4" />
          <Skeleton className="h-32 w-full" />
          <Skeleton className="h-12 w-1/3" />
        </div>
      </AppContainer>
    );
  }
  
  const renderStep = () => {
    switch (currentStep) {
      case "welcome":
        return <WelcomeStep onStartScanning={handleStartScanning} />;
      case "scanning":
        return <ScanningStep onScanComplete={handleScanComplete} />;
      case "results":
        return <ResultsStep detectedIdes={detectedIdes} onStartConfiguration={handleStartConfiguration} />;
      case "configuring":
        if (!selectedConfig) {
          // Fallback if selectedConfig is somehow null, should not happen in normal flow
          setCurrentStep("results"); 
          return <p>Error: No configuration selected. Redirecting...</p>;
        }
        const ideToConfigure = detectedIdes.find(ide => ide.id === selectedConfig.ideId);
        return <ConfiguringStep 
                  ideName={ideToConfigure?.name || "Selected IDE"} 
                  extensionsToInstall={selectedConfig.extensions} 
                  onConfigurationComplete={handleConfigurationComplete} 
               />;
      case "complete":
         const configuredIde = detectedIdes.find(ide => ide.id === selectedConfig?.ideId);
        return <CompleteStep 
                  configuredIdeName={configuredIde?.name || "Your IDE"}
                  configuredExtensionsCount={selectedConfig?.extensions.length || 0}
                  onRestart={handleRestart} 
               />;
      default:
        return <WelcomeStep onStartScanning={handleStartScanning} />;
    }
  };

  return (
    <AppContainer>
      <ProgressIndicator currentStep={currentStep} steps={STEPS} />
      <div className="mt-8 w-full">
        {renderStep()}
      </div>
    </AppContainer>
  );
}
