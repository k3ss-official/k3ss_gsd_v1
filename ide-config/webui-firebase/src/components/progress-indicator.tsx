import type { Step } from "@/types";
import { cn } from "@/lib/utils";
import { Check } from "lucide-react";

interface ProgressIndicatorProps {
  currentStep: Step;
  steps: readonly Step[];
}

const stepLabels: Record<Step, string> = {
  welcome: "Welcome",
  scanning: "Scanning",
  results: "Results & Recommendations",
  configuring: "Configuration",
  complete: "Complete",
};

export function ProgressIndicator({ currentStep, steps }: ProgressIndicatorProps) {
  const currentIndex = steps.indexOf(currentStep);

  return (
    <nav aria-label="Progress" className="mb-12">
      <ol role="list" className="flex items-center space-x-2 sm:space-x-4">
        {steps.map((step, index) => (
          <li key={step} className="flex-1">
            <div
              className={cn(
                "flex flex-col items-center border-t-4 pt-2 text-center sm:pt-3",
                index <= currentIndex ? "border-primary" : "border-border",
                index < currentIndex ? "cursor-default" : "cursor-default" // Could allow navigation to previous steps
              )}
            >
              <div className="flex items-center justify-center">
                 {index < currentIndex ? (
                  <span className="flex h-6 w-6 sm:h-8 sm:w-8 items-center justify-center rounded-full bg-primary">
                    <Check className="h-4 w-4 text-primary-foreground sm:h-5 sm:w-5" />
                  </span>
                ) : index === currentIndex ? (
                  <span className="relative flex h-6 w-6 sm:h-8 sm:w-8 items-center justify-center rounded-full border-2 border-primary bg-primary/20">
                    <span className="h-2 w-2 sm:h-2.5 sm:w-2.5 rounded-full bg-primary" />
                  </span>
                ) : (
                  <span className="flex h-6 w-6 sm:h-8 sm:w-8 items-center justify-center rounded-full border-2 border-border bg-background" />
                )}
              </div>
              <p
                className={cn(
                  "mt-2 text-xs font-medium sm:text-sm",
                  index <= currentIndex ? "text-primary" : "text-muted-foreground"
                )}
              >
                {stepLabels[step]}
              </p>
            </div>
          </li>
        ))}
      </ol>
    </nav>
  );
}
