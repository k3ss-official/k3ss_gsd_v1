
import { useState, useEffect } from "react";
import type { DetectedIDE, RecommendationRequestInput, ProjectType } from "@/types";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { IdeCard } from "@/components/ide-card";
import { RecommendationForm, type RecommendationFormData } from "@/components/recommendation-form";
import { getAIRecommendations, type RecommendActionState } from "@/lib/actions";
import { Loader2, ListChecks, Wand2, Info, AlertTriangle, Sparkles, CheckSquare, Square, ThumbsUp } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

interface ResultsStepProps {
  detectedIdes: DetectedIDE[];
  onStartConfiguration: (selectedConfig: { ideId: string; extensions: string[] }) => void;
}

export function ResultsStep({ detectedIdes, onStartConfiguration }: ResultsStepProps) {
  const [selectedIdeId, setSelectedIdeId] = useState<string | null>(detectedIdes.length > 0 ? detectedIdes[0].id : null);
  const [recommendationState, setRecommendationState] = useState<RecommendActionState | null>(null);
  const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(false);
  const [selectedExtensions, setSelectedExtensions] = useState<Record<string, boolean>>({});
  const [selectAll, setSelectAll] = useState(false);

  const handleFormSubmit = async (data: RecommendationFormData) => {
    setIsLoadingRecommendations(true);
    setRecommendationState(null); // Clear previous recommendations
    setSelectedExtensions({}); // Reset selected extensions
    setSelectAll(false); // Reset select all

    // Ensure preferences is an object, even if empty
    const submissionData: RecommendationRequestInput = {
        ...data,
        preferences: data.preferences || {}, 
    };

    const result = await getAIRecommendations(submissionData);
    setRecommendationState(result);
    setIsLoadingRecommendations(false);

    // Pre-select all recommended extensions if there are any
    if (result.data && result.data.recommendedExtensions.length > 0) {
      const initialSelections: Record<string, boolean> = {};
      result.data.recommendedExtensions.forEach(extName => {
        initialSelections[extName] = true;
      });
      setSelectedExtensions(initialSelections);
      setSelectAll(true);
    }
  };

  const handleExtensionToggle = (extensionName: string) => {
    const newSelections = { ...selectedExtensions, [extensionName]: !selectedExtensions[extensionName] };
    setSelectedExtensions(newSelections);
    if (recommendationState?.data?.recommendedExtensions) {
      setSelectAll(recommendationState.data.recommendedExtensions.every(ext => newSelections[ext]));
    }
  };
  
  const handleSelectAllToggle = () => {
    const newSelectAllState = !selectAll;
    setSelectAll(newSelectAllState);
    if (recommendationState?.data?.recommendedExtensions) {
      const newSelections: Record<string, boolean> = {};
      recommendationState.data.recommendedExtensions.forEach(extName => {
        newSelections[extName] = newSelectAllState;
      });
      setSelectedExtensions(newSelections);
    }
  };

  const handleConfigure = () => {
    if (!selectedIdeId) return;
    const extensionsToInstall = Object.entries(selectedExtensions)
      .filter(([, isSelected]) => isSelected)
      .map(([name]) => name);
    onStartConfiguration({ ideId: selectedIdeId, extensions: extensionsToInstall });
  };
  
  const selectedIde = detectedIdes.find(ide => ide.id === selectedIdeId);
  const numSelectedExtensions = Object.values(selectedExtensions).filter(Boolean).length;

  return (
    <div className="space-y-8">
      <Card className="shadow-xl border-border hover:shadow-[0_0_20px_5px_hsl(var(--card)/0.1)] transition-shadow duration-300">
        <CardHeader>
          <CardTitle className="text-3xl font-semibold flex items-center">
            <ListChecks className="mr-3 h-8 w-8 text-primary" />
            Detection Results
          </CardTitle>
          <CardDescription className="text-lg">
            We've scanned your system. Select an IDE below to get AI-powered Vibe Coder enhancements.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {detectedIdes.length === 0 ? (
            <Alert variant="default" className="bg-muted/30">
              <Info className="h-4 w-4" />
              <AlertTitle>No IDEs Detected</AlertTitle>
              <AlertDescription>
                Vibe Coder couldn't find any supported IDEs. Please ensure they're installed correctly.
              </AlertDescription>
            </Alert>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {detectedIdes.map((ide) => (
                <IdeCard 
                  key={ide.id} 
                  ide={ide} 
                  onSelectIde={() => {
                    setSelectedIdeId(ide.id);
                    setRecommendationState(null); // Clear old recommendations when IDE changes
                    setSelectedExtensions({});
                    setSelectAll(false);
                  }}
                  isSelected={ide.id === selectedIdeId}
                />
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {selectedIde && (
        <Card className="shadow-xl border-border hover:shadow-[0_0_20px_5px_hsl(var(--card)/0.1)] transition-shadow duration-300">
          <CardHeader>
            <CardTitle className="text-2xl font-semibold flex items-center">
              <Sparkles className="mr-3 h-7 w-7 text-accent animate-pulse" />
              AI Vibe Configuration for {selectedIde.name}
            </CardTitle>
            <CardDescription className="text-lg">
              Share your project goals and Vibe Coder AI will tailor the perfect setup.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <RecommendationForm
              detectedIdes={detectedIdes}
              onSubmit={handleFormSubmit}
              isLoading={isLoadingRecommendations}
              defaultValues={{ 
                ideName: selectedIde.name,
                projectType: recommendationState?.input?.projectType as ProjectType | undefined, // Repopulate if validation failed
                projectTypeOther: recommendationState?.input?.projectTypeOther,
                preferences: recommendationState?.input?.preferences,
                userNotes: recommendationState?.input?.userNotes,
              }}
            />

            {isLoadingRecommendations && (
              <div className="mt-8 flex flex-col items-center justify-center text-center space-y-3 p-6 bg-muted/20 rounded-lg">
                <Loader2 className="h-12 w-12 animate-spin text-primary" />
                <p className="text-lg text-muted-foreground">Vibe Coder AI is crafting your recommendations...</p>
                <p className="text-sm text-muted-foreground/70">This might take a few moments.</p>
              </div>
            )}

            {recommendationState?.error && (
              <Alert variant="destructive" className="mt-6">
                <AlertTriangle className="h-4 w-4" />
                <AlertTitle>Oops! Vibe Coder ran into an issue.</AlertTitle>
                <AlertDescription>{recommendationState.error}</AlertDescription>
                {recommendationState.fieldErrors && (
                  <ul className="mt-2 list-disc list-inside text-sm">
                    {Object.entries(recommendationState.fieldErrors).map(([field, errors]) =>
                      errors?.map(err => <li key={`${field}-${err}`}>{`${field}: ${err}`}</li>)
                    )}
                  </ul>
                )}
              </Alert>
            )}
            
            {recommendationState?.data && recommendationState?.input && (
              <div className="mt-10 space-y-8 p-4 bg-background rounded-lg ">
                <Separator />
                <div>
                  <h3 className="text-2xl font-semibold mb-4 flex items-center text-primary">
                    <Wand2 className="mr-2 h-6 w-6" />
                    AI Recommended Enhancements
                  </h3>
                  {recommendationState.data.recommendedExtensions.length === 0 ? (
                     <Alert className="bg-muted/30">
                        <Info className="h-4 w-4" />
                        <AlertTitle>No Specific Extensions Recommended</AlertTitle>
                        <AlertDescription>Vibe Coder AI didn't pinpoint specific extensions based on your input. You can proceed with a general IDE setup or refine your preferences above and try again.</AlertDescription>
                     </Alert>
                  ) : (
                    <>
                      <div className="flex items-center space-x-3 mb-4 p-2 bg-muted/30 rounded-md">
                        {selectAll ? <CheckSquare className="h-5 w-5 text-primary cursor-pointer" onClick={handleSelectAllToggle} /> : <Square className="h-5 w-5 text-muted-foreground cursor-pointer" onClick={handleSelectAllToggle} />}
                        <Label htmlFor="select-all-toggle" className="text-sm font-medium cursor-pointer" onClick={handleSelectAllToggle}>
                          {selectAll ? "Deselect All" : "Select All"} ({recommendationState.data.recommendedExtensions.length} items)
                        </Label>
                      </div>
                      <ScrollArea className="h-64 rounded-md border p-4 bg-muted/10 shadow-inner">
                        <div className="space-y-3">
                          {recommendationState.data.recommendedExtensions.map((extName, index) => (
                            <div key={index} className="flex items-center space-x-3 p-3 rounded-md hover:bg-accent/10 transition-colors duration-150 cursor-pointer" onClick={() => handleExtensionToggle(extName)}>
                              <Checkbox
                                id={`ext-${index}`}
                                checked={selectedExtensions[extName] || false}
                                onCheckedChange={() => handleExtensionToggle(extName)}
                                className="form-checkbox h-5 w-5 text-primary focus:ring-primary border-muted-foreground"
                              />
                              <Label htmlFor={`ext-${index}`} className="text-base font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer flex-1">
                                {extName}
                              </Label>
                            </div>
                          ))}
                        </div>
                      </ScrollArea>
                    </>
                  )}
                </div>
                
                <div className="p-6 bg-muted/20 rounded-lg shadow">
                  <h3 className="text-xl font-semibold mb-3 flex items-center text-accent">
                    <Info className="mr-2 h-5 w-5" />
                    Vibe Coder AI Reasoning
                  </h3>
                  <p className="text-md text-foreground/90 leading-relaxed whitespace-pre-wrap">{recommendationState.data.reasoning}</p>
                </div>
                
                <Separator />

                <div className="p-6 bg-card border rounded-lg shadow-md">
                    <h3 className="text-xl font-semibold mb-4 flex items-center text-primary">
                        <ThumbsUp className="mr-2 h-6 w-6" />
                        Your Configuration Summary
                    </h3>
                    <div className="space-y-3 text-md">
                        <p><strong>IDE:</strong> {selectedIde.name}</p>
                        <p><strong>Project Type:</strong> {recommendationState.input.projectType}
                            {recommendationState.input.projectType === "Other" && recommendationState.input.projectTypeOther && ` (${recommendationState.input.projectTypeOther})`}
                        </p>
                        <div>
                            <strong>Selected Preferences:</strong>
                            <ul className="list-disc list-inside ml-4 mt-1 text-sm text-muted-foreground">
                                {Object.entries(recommendationState.input.preferences).map(([category, prefs]) =>
                                    Array.isArray(prefs) && prefs.length > 0 ? (
                                        <li key={category} className="capitalize">
                                            {category.replace(/([A-Z])/g, ' $1')}: {prefs.join(', ')}
                                        </li>
                                    ) : null
                                )}
                                {Object.values(recommendationState.input.preferences).every(p => !Array.isArray(p) || p.length === 0) && <li>No specific preferences selected.</li>}
                            </ul>
                        </div>
                        {recommendationState.input.userNotes && (
                            <p><strong>Your Notes:</strong> <span className="italic text-muted-foreground">"{recommendationState.input.userNotes}"</span></p>
                        )}
                        <p><strong>Extensions to be installed ({numSelectedExtensions}):</strong></p>
                        {numSelectedExtensions > 0 ? (
                            <ScrollArea className="h-32 rounded-md border p-2 text-sm bg-muted/10">
                                <ul className="list-disc list-inside">
                                {Object.entries(selectedExtensions)
                                    .filter(([,isSelected]) => isSelected)
                                    .map(([name]) => <li key={name}>{name}</li>)
                                }
                                </ul>
                            </ScrollArea>
                        ) : (
                            <p className="text-sm text-muted-foreground italic">No extensions selected for installation.</p>
                        )}
                    </div>
                </div>

              </div>
            )}
          </CardContent>
          {recommendationState?.data && (
            <CardFooter className="flex justify-end pt-8">
              <Button
                size="lg"
                onClick={handleConfigure}
                className="text-lg py-6 bg-gradient-to-r from-green-500 to-green-600 text-white hover:opacity-90 transition-opacity duration-300 shadow-lg hover:shadow-[0_0_15px_5px_hsl(var(--accent)/0.5)] focus:shadow-[0_0_20px_8px_hsl(var(--accent)/0.7)] active:shadow-[0_0_25px_10px_hsl(var(--accent)/0.8)]"
              >
                Configure {selectedIde.name} with {numSelectedExtensions} Enhancement(s)
              </Button>
            </CardFooter>
          )}
        </Card>
      )}
    </div>
  );
}
