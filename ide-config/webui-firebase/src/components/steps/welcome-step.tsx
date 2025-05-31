import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Rocket } from "lucide-react";

interface WelcomeStepProps {
  onStartScanning: () => void;
}

export function WelcomeStep({ onStartScanning }: WelcomeStepProps) {
  return (
    <div className="flex flex-col items-center justify-center text-center">
      <Card className="w-full shadow-xl">
        <CardHeader>
          <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary">
            <Rocket className="h-8 w-8" />
          </div>
          <CardTitle className="text-4xl font-bold tracking-tight">Welcome to Vibe Coder</CardTitle>
          <CardDescription className="text-lg text-muted-foreground">
            Transform your vanilla IDE installations into fully-configured, security-hardened, AI-enhanced development environments.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="mb-8 text-foreground/80">
            Ready to elevate your coding experience? We'll scan your system, detect installed IDEs,
            analyze missing extensions & configurations, and apply best practices with AI-powered insights.
          </p>
        </CardContent>
        <CardFooter className="flex justify-center">
          <Button
            size="lg"
            onClick={onStartScanning}
            className="bg-gradient-to-r from-primary to-accent text-primary-foreground hover:opacity-90 transition-opacity duration-300 shadow-lg"
          >
            <Rocket className="mr-2 h-5 w-5" />
            Start Scanning
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
