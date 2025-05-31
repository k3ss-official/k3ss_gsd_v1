
import type React from 'react';
import { useForm, type SubmitHandler, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import type { DetectedIDE, RecommendationRequestInput, UserPreferences as UserPreferencesType, ProjectType } from "@/types";
import { PROJECT_TYPES } from "@/types";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Brain, Sparkles } from 'lucide-react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

const userPreferencesSchema = z.object({
  testing: z.array(z.string()).optional(),
  lintingFormatters: z.array(z.string()).optional(),
  aiAssistance: z.array(z.string()).optional(),
  security: z.array(z.string()).optional(),
  versionControl: z.array(z.string()).optional(),
  collaboration: z.array(z.string()).optional(),
});

const recommendationSchema = z.object({
  ideName: z.string().min(1, "Please select an IDE."),
  projectType: z.enum(PROJECT_TYPES, { required_error: "Please select a project type." }),
  projectTypeOther: z.string().optional(),
  preferences: userPreferencesSchema.default({}),
  userNotes: z.string().optional().describe("Any other specific requests or details you want to add."),
}).refine(data => data.projectType !== "Other" || (data.projectType === "Other" && data.projectTypeOther && data.projectTypeOther.trim().length > 0), {
  message: "Please specify your project type if 'Other' is selected.",
  path: ["projectTypeOther"],
});

export type RecommendationFormData = z.infer<typeof recommendationSchema>;

interface RecommendationFormProps {
  detectedIdes: DetectedIDE[];
  onSubmit: (data: RecommendationFormData) => void;
  isLoading: boolean;
  defaultValues?: Partial<RecommendationFormData>;
}

const preferenceOptions = {
  testing: ["Unit Testing (e.g., Jest, Vitest)", "Integration Testing", "E2E Testing (e.g., Cypress, Playwright)"],
  lintingFormatters: ["Strict Linting Rules", "Auto-formatting on Save (e.g., Prettier)", "Style Guides Enforcement"],
  aiAssistance: ["Advanced Code Completion", "AI-Powered Code Generation", "AI-Assisted Debugging", "Inline Chat with AI"],
  security: ["Static Application Security Testing (SAST)", "Software Composition Analysis (SCA - dependency scanning)", "Secrets Detection", "Infrastructure as Code (IaC) Security"],
  versionControl: ["Enhanced GitLens-like features", "Issue Tracker Integration (Jira, GitHub Issues)", "Commit Message Assistance"],
  collaboration: ["Live Share / Pair Programming", "Real-time Commenting", "Team-based Snippet Libraries"],
};

export function RecommendationForm({ detectedIdes, onSubmit, isLoading, defaultValues }: RecommendationFormProps) {
  const form = useForm<RecommendationFormData>({
    resolver: zodResolver(recommendationSchema),
    defaultValues: {
      ideName: defaultValues?.ideName || (detectedIdes.length > 0 ? detectedIdes[0].name : ""),
      projectType: defaultValues?.projectType,
      projectTypeOther: defaultValues?.projectTypeOther || "",
      preferences: defaultValues?.preferences || {
        testing: [],
        lintingFormatters: [],
        aiAssistance: [],
        security: [],
        versionControl: [],
        collaboration: [],
      },
      userNotes: defaultValues?.userNotes || "",
    },
  });

  const watchedProjectType = form.watch("projectType");

  const handleSubmit: SubmitHandler<RecommendationFormData> = (data) => {
    onSubmit(data);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-8 p-1">
        <FormField
          control={form.control}
          name="ideName"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="text-lg font-semibold">Target IDE</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger className="focus:shadow-[0_0_10px_2px_hsl(var(--accent)/0.4)]">
                    <SelectValue placeholder="Select an IDE to configure" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {detectedIdes.map((ide) => (
                    <SelectItem key={ide.id} value={ide.name}>
                      <div className="flex items-center">
                        {ide.icon && <ide.icon className="mr-2 h-4 w-4" />}
                        {ide.name}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormDescription>
                Choose the IDE you want Vibe Coder to enhance.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="projectType"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="text-lg font-semibold">Project Type</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger className="focus:shadow-[0_0_10px_2px_hsl(var(--accent)/0.4)]">
                    <SelectValue placeholder="What kind of project are you building?" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {PROJECT_TYPES.map((type) => (
                    <SelectItem key={type} value={type}>{type}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {watchedProjectType === "Other" && (
          <FormField
            control={form.control}
            name="projectTypeOther"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Specify Project Type</FormLabel>
                <FormControl>
                  <Input placeholder="e.g., Blockchain dApp, Embedded System" {...field} className="focus:shadow-[0_0_10px_2px_hsl(var(--accent)/0.4)]" />
                </FormControl>
                <FormDescription>
                  Tell us more about your unique project.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />
        )}

        <FormItem>
          <FormLabel className="text-lg font-semibold">Preferences & Tooling Vibe</FormLabel>
          <FormDescription className="mb-2">
            Select areas you'd like to focus on for enhancement. Vibe Coder will use these to suggest the best setup.
          </FormDescription>
          <Accordion type="multiple" className="w-full" defaultValue={["testing", "aiAssistance"]}>
            {Object.entries(preferenceOptions).map(([key, options]) => (
              <AccordionItem value={key} key={key}>
                <AccordionTrigger className="text-base hover:text-accent capitalize focus:shadow-[0_0_10px_2px_hsl(var(--accent)/0.4)] rounded-md px-2">
                  {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                </AccordionTrigger>
                <AccordionContent className="pt-2 pb-0">
                  <div className="space-y-2 pl-4 pr-2">
                    {options.map((option) => (
                      <FormField
                        key={option}
                        control={form.control}
                        name={`preferences.${key as keyof UserPreferencesType}`}
                        render={({ field }) => {
                          return (
                            <FormItem className="flex flex-row items-center space-x-3 space-y-0 p-2 hover:bg-muted/50 rounded-md transition-colors">
                              <FormControl>
                                <Checkbox
                                  checked={field.value?.includes(option)}
                                  onCheckedChange={(checked) => {
                                    return checked
                                      ? field.onChange([...(field.value || []), option])
                                      : field.onChange(
                                          (field.value || []).filter(
                                            (value) => value !== option
                                          )
                                        );
                                  }}
                                />
                              </FormControl>
                              <FormLabel className="font-normal cursor-pointer">
                                {option}
                              </FormLabel>
                            </FormItem>
                          );
                        }}
                      />
                    ))}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </FormItem>

        <FormField
          control={form.control}
          name="userNotes"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="text-lg font-semibold">Anything specific you want to add?</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="e.g., 'I need strong support for Python and Django', 'Focus on accessibility tools', 'Make it look like a cyberpunk terminal!'"
                  className="resize-y min-h-[100px] focus:shadow-[0_0_10px_2px_hsl(var(--accent)/0.4)]"
                  rows={4}
                  {...field}
                />
              </FormControl>
              <FormDescription>
                Your specific instructions or wishes for Vibe Coder.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button 
          type="submit" 
          disabled={isLoading} 
          className="w-full text-lg py-6 bg-gradient-to-r from-primary to-accent text-primary-foreground hover:opacity-90 transition-opacity duration-300 shadow-lg hover:shadow-[0_0_15px_5px_hsl(var(--accent)/0.5)] focus:shadow-[0_0_20px_8px_hsl(var(--accent)/0.7)] active:shadow-[0_0_25px_10px_hsl(var(--accent)/0.8)]"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Summoning AI Vibe Code...
            </>
          ) : (
            <>
              <Sparkles className="mr-2 h-6 w-6" />
              Get Vibe Coder Recommendations
            </>
          )}
        </Button>
      </form>
    </Form>
  );
}
