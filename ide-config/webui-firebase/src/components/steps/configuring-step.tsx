import { useState, useEffect } from "react";
import type { ConfigurationLog } from "@/types";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ScrollArea } from "@/components/ui/scroll-area";
import { CheckCircle2, AlertTriangle, Info, Loader2, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ConfiguringStepProps {
  ideName: string;
  extensionsToInstall: string[];
  onConfigurationComplete: () => void;
}

const mockLogs: Omit<ConfigurationLog, "id" | "timestamp">[] = [
  { message: "Starting configuration process...", type: "info" },
  { message: "Validating IDE environment...", type: "info" },
  { message: "IDE validation successful.", type: "success" },
];

export function ConfiguringStep({ ideName, extensionsToInstall, onConfigurationComplete }: ConfiguringStepProps) {
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState<ConfigurationLog[]>([]);
  const [currentTask, setCurrentTask] = useState("Initializing...");
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    const totalTasks = mockLogs.length + extensionsToInstall.length + 2; // initial, validate, install each ext, finalization, completion
    let tasksCompleted = 0;

    const addLog = (message: string, type: ConfigurationLog["type"]) => {
      setLogs(prev => [...prev, { id: crypto.randomUUID(), timestamp: new Date().toLocaleTimeString(), message, type }]);
      setCurrentTask(message);
      tasksCompleted++;
      setProgress(Math.round((tasksCompleted / totalTasks) * 100));
    };

    const runConfiguration = async () => {
      for (const log of mockLogs) {
        await new Promise(resolve => setTimeout(resolve, 700));
        addLog(log.message, log.type);
      }

      if (extensionsToInstall.length > 0) {
         addLog(`Starting installation of ${extensionsToInstall.length} extension(s) for ${ideName}...`, "info");
         await new Promise(resolve => setTimeout(resolve, 1000));
        for (const ext of extensionsToInstall) {
          addLog(`Installing ${ext}...`, "info");
          await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate install time
          // Randomly succeed or fail for demo
          if (Math.random() > 0.1) {
            addLog(`${ext} installed successfully.`, "success");
          } else {
            addLog(`Failed to install ${ext}. Skipping.`, "error");
          }
        }
      } else {
        addLog("No extensions selected for installation.", "info");
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      addLog("Finalizing setup...", "info");
      await new Promise(resolve => setTimeout(resolve, 1200));
      addLog("Configuration complete for " + ideName + "!", "success");
      setIsComplete(true);
      setProgress(100);
    };

    runConfiguration();
  }, [ideName, extensionsToInstall]);

  const LogIcon = ({ type }: { type: ConfigurationLog["type"] }) => {
    switch (type) {
      case "success": return <CheckCircle2 className="h-4 w-4 text-green-500" />;
      case "error": return <AlertTriangle className="h-4 w-4 text-destructive" />;
      case "warning": return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      case "info":
      default: return <Info className="h-4 w-4 text-blue-500" />;
    }
  };

  return (
    <Card className="w-full shadow-xl">
      <CardHeader>
        <CardTitle className="text-3xl font-semibold flex items-center">
          {isComplete ? <CheckCircle2 className="mr-3 h-8 w-8 text-green-500" /> : <Settings className="mr-3 h-8 w-8 text-primary animate-spin-slow" />}
          {isComplete ? `Configuration Complete for ${ideName}` : `Configuring ${ideName}`}
        </CardTitle>
        <CardDescription>
          {isComplete ? "Your IDE has been enhanced. See details below." : "Please wait while we set up your IDE with the selected configurations."}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <div className="flex justify-between text-sm font-medium text-muted-foreground">
            <span>Overall Progress</span>
            <span>{progress}%</span>
          </div>
          <Progress value={progress} className="w-full h-3" />
          <p className="text-sm text-primary text-center mt-2 min-h-[1.25rem]">{currentTask}</p>
        </div>

        <div className="space-y-2">
          <h4 className="text-lg font-medium">Configuration Log:</h4>
          <ScrollArea className="h-64 w-full rounded-md border bg-muted/30 p-4 shadow-inner">
            {logs.length === 0 && <p className="text-sm text-muted-foreground">Waiting for logs...</p>}
            {logs.map((log) => (
              <div key={log.id} className="mb-2 flex items-start space-x-2 text-sm last:mb-0">
                <LogIcon type={log.type} />
                <span className="font-mono text-xs text-muted-foreground w-20 shrink-0">{log.timestamp}</span>
                <p className={cn(
                  "flex-1",
                  log.type === "error" && "text-destructive",
                  log.type === "success" && "text-green-600 dark:text-green-400"
                )}>{log.message}</p>
              </div>
            ))}
             {!isComplete && logs.length > 0 && (
              <div className="flex items-center space-x-2 text-sm text-muted-foreground animate-pulse mt-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Processing...</span>
              </div>
            )}
          </ScrollArea>
        </div>
      </CardContent>
      {isComplete && (
         <CardFooter className="flex justify-end">
            <Button size="lg" onClick={onConfigurationComplete} className="bg-gradient-to-r from-primary to-accent text-primary-foreground hover:opacity-90 transition-opacity duration-300 shadow-lg">
              Go to Summary
            </Button>
         </CardFooter>
      )}
    </Card>
  );
}

// Add this to your tailwind.config.js if you want a slower spin:
// animation: {
//   'spin-slow': 'spin 3s linear infinite',
// }
// For now, default spin speed is fine.
