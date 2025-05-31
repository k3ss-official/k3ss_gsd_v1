import { useState, useEffect } from "react";
import type { DetectedIDE } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Search, Settings, Brain } from "lucide-react"; // Using Brain for AI
import Image from "next/image";


// Mock IDE icons (simple placeholders, ideally SVGs)
const VSCodeIcon = () => <Image src="https://placehold.co/40x40.png?text=VS" alt="VS Code" width={24} height={24} data-ai-hint="code editor" className="rounded-sm"/>;
const IntelliJIcon = () => <Image src="https://placehold.co/40x40.png?text=IJ" alt="IntelliJ" width={24} height={24} data-ai-hint="code editor" className="rounded-sm"/>;


const scanSteps = [
  { text: "Initializing scan...", icon: Search, duration: 1500 },
  { text: "Scanning filesystem for IDEs...", icon: Search, duration: 2500 },
  { text: "Detected Visual Studio Code...", icon: VSCodeIcon, duration: 1000 },
  { text: "Detected IntelliJ IDEA...", icon: IntelliJIcon, duration: 1000 },
  { text: "Analyzing configurations...", icon: Settings, duration: 2000 },
  { text: "Consulting AI for enhancements...", icon: Brain, duration: 2000 },
];

interface ScanningStepProps {
  onScanComplete: (detectedIdes: DetectedIDE[]) => void;
}

export function ScanningStep({ onScanComplete }: ScanningStepProps) {
  const [progress, setProgress] = useState(0);
  const [currentScanStep, setCurrentScanStep] = useState(0);
  const [displayedText, setDisplayedText] = useState(scanSteps[0].text);
  const [CurrentIcon, setCurrentIcon] = useState(() => scanSteps[0].icon);

  useEffect(() => {
    let overallProgress = 0;
    const totalDuration = scanSteps.reduce((sum, step) => sum + step.duration, 0);
    
    let stepTimeout: NodeJS.Timeout;
    let progressInterval: NodeJS.Timeout;

    const advanceStep = (stepIndex: number) => {
      if (stepIndex >= scanSteps.length) {
        setProgress(100);
        // Simulate detected IDEs
        const mockIdes: DetectedIDE[] = [
          { id: "vscode", name: "Visual Studio Code", version: "1.89.1", path: "/Applications/Visual Studio Code.app", status: "needs_config", icon: VSCodeIcon },
          { id: "intellij", name: "IntelliJ IDEA Ultimate", version: "2024.1.2", path: "/Applications/IntelliJ IDEA.app", status: "needs_config", icon: IntelliJIcon },
        ];
        onScanComplete(mockIdes);
        return;
      }

      setCurrentScanStep(stepIndex);
      setDisplayedText(scanSteps[stepIndex].text);
      setCurrentIcon(() => scanSteps[stepIndex].icon); // Update icon state

      const stepDuration = scanSteps[stepIndex].duration;
      let currentStepProgress = 0;

      progressInterval = setInterval(() => {
        currentStepProgress += 50; // Update interval for smoother progress
        overallProgress += (50 / totalDuration) * 100 * (stepDuration / 50); // Approximate progress based on step's contribution
        setProgress(Math.min(overallProgress, 100));
         if (currentStepProgress >= stepDuration) {
           clearInterval(progressInterval);
         }
      }, 50);
      
      stepTimeout = setTimeout(() => {
        clearInterval(progressInterval);
        advanceStep(stepIndex + 1);
      }, stepDuration);
    };

    advanceStep(0);

    return () => {
      clearTimeout(stepTimeout);
      clearInterval(progressInterval);
    };
  }, [onScanComplete]);

  return (
    <div className="flex flex-col items-center justify-center text-center">
      <Card className="w-full shadow-xl">
        <CardHeader>
          <CardTitle className="text-3xl font-semibold">Scanning System</CardTitle>
        </CardHeader>
        <CardContent className="space-y-8">
          <div className="flex items-center justify-center space-x-3 text-lg text-foreground/80">
            <CurrentIcon className="h-6 w-6 animate-pulse text-primary" />
            <span>{displayedText}</span>
          </div>
          <Progress value={progress} className="w-full h-3" />
           <div className="w-full h-40 bg-muted rounded-lg overflow-hidden relative">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
            </div>
            {scanSteps.map((step, index) => (
              <div
                key={index}
                className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 transition-all duration-500 ease-in-out ${
                  index === currentScanStep ? 'opacity-100 scale-100' : 'opacity-0 scale-90'
                }`}
              >
                {index === currentScanStep && <step.icon className="h-10 w-10 text-primary" />}
              </div>
            ))}
          </div>
          <p className="text-sm text-muted-foreground">Please wait while we analyze your development environment...</p>
        </CardContent>
      </Card>
    </div>
  );
}
