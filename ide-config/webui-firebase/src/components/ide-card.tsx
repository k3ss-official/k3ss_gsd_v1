
import type { DetectedIDE } from "@/types";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, CheckCircle2 } from "lucide-react"; // Removed Settings2 as it wasn't used

interface IdeCardProps {
  ide: DetectedIDE;
  onSelectIde?: (ideId: string) => void;
  isSelected?: boolean;
}

export function IdeCard({ ide, onSelectIde, isSelected }: IdeCardProps) {
  const statusMap = {
    needs_config: {
      text: "Needs Configuration",
      icon: <AlertTriangle className="h-4 w-4 text-destructive" />,
      badgeVariant: "destructive" as "destructive",
    },
    configured: {
      text: "Configured",
      icon: <CheckCircle2 className="h-4 w-4 text-green-500" />,
      badgeVariant: "default" as "default",
    },
    error: {
      text: "Error",
      icon: <AlertTriangle className="h-4 w-4 text-destructive" />,
      badgeVariant: "destructive" as "destructive",
    },
  };

  const currentStatus = statusMap[ide.status] || statusMap.error;

  return (
    <Card 
      className={`transition-all duration-300 ${onSelectIde ? 'cursor-pointer card-glow-accent' : ''} ${isSelected ? 'ring-2 ring-primary shadow-[0_0_25px_3px_hsl(var(--primary)/0.6)] scale-105' : 'shadow-md hover:shadow-xl'}`}
      onClick={onSelectIde ? () => onSelectIde(ide.id) : undefined}
    >
      <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
        <div className="space-y-1">
          <CardTitle className="text-xl font-semibold flex items-center">
            {ide.icon && <ide.icon className="mr-2 h-6 w-6" />}
            {ide.name}
          </CardTitle>
          <CardDescription>Version: {ide.version}</CardDescription>
        </div>
        <Badge variant={currentStatus.badgeVariant} className="whitespace-nowrap">
          {currentStatus.icon}
          <span className="ml-1">{currentStatus.text}</span>
        </Badge>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground truncate">Path: {ide.path}</p>
        {ide.missingExtensions && ide.missingExtensions.length > 0 && (
          <div className="mt-2">
            <h4 className="text-xs font-medium text-foreground/80">Missing Critical Extensions:</h4>
            <ul className="list-disc list-inside text-xs text-muted-foreground">
              {ide.missingExtensions.slice(0, 3).map(ext => <li key={ext}>{ext}</li>)}
              {ide.missingExtensions.length > 3 && <li>...and {ide.missingExtensions.length - 3} more</li>}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
