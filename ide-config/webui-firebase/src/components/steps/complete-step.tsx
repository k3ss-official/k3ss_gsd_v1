import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle, PartyPopper, RotateCcw } from "lucide-react"; // PartyPopper for celebration

interface CompleteStepProps {
  configuredIdeName: string;
  configuredExtensionsCount: number;
  onRestart: () => void;
}

export function CompleteStep({ configuredIdeName, configuredExtensionsCount, onRestart }: CompleteStepProps) {
  return (
    <div className="flex flex-col items-center justify-center text-center">
      <Card className="w-full shadow-xl">
        <CardHeader>
          <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-green-500/10 text-green-500">
            <PartyPopper className="h-8 w-8" />
          </div>
          <CardTitle className="text-4xl font-bold tracking-tight text-green-600 dark:text-green-400">Configuration Successful!</CardTitle>
          <CardDescription className="text-lg text-muted-foreground">
            Your <span className="font-semibold text-primary">{configuredIdeName}</span> is now a Vibe Coder powerhouse.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="rounded-md border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/30 p-6 shadow-sm">
            <div className="flex items-center space-x-3">
              <CheckCircle className="h-10 w-10 text-green-500" />
              <div>
                <h3 className="text-xl font-semibold text-green-700 dark:text-green-300">All Set!</h3>
                <p className="text-green-600 dark:text-green-400">
                  {configuredExtensionsCount > 0 
                    ? `${configuredExtensionsCount} enhancement(s) have been applied to ${configuredIdeName}.`
                    : `${configuredIdeName} has been checked and configured.`}
                </p>
              </div>
            </div>
          </div>
          
          <div className="text-left space-y-3 text-foreground/80">
            <h4 className="text-lg font-semibold text-primary">Next Steps:</h4>
            <ul className="list-disc list-inside space-y-1 pl-4">
              <li>Open {configuredIdeName} and explore the new features.</li>
              <li>Refer to any extension-specific documentation for advanced usage.</li>
              <li>Enjoy your supercharged development workflow!</li>
            </ul>
          </div>
          
          <p className="text-sm text-muted-foreground pt-4">
            If you encounter any issues or want to configure another IDE, feel free to start over.
          </p>
        </CardContent>
        <CardFooter className="flex flex-col sm:flex-row justify-center items-center gap-4">
          <Button
            size="lg"
            variant="outline"
            onClick={onRestart}
            className="shadow-md hover:bg-muted/50 transition-colors"
          >
            <RotateCcw className="mr-2 h-5 w-5" />
            Configure Another IDE
          </Button>
          <Button
            size="lg"
            onClick={() => alert("Happy Coding! This would typically close the app or redirect.")}
            className="bg-gradient-to-r from-green-500 to-green-600 text-white hover:opacity-90 transition-opacity duration-300 shadow-lg"
          >
            <PartyPopper className="mr-2 h-5 w-5" />
            Finish & Start Coding
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
