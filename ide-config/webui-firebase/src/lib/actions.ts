
"use server";

import { recommendExtensions, type RecommendExtensionsInput, type RecommendExtensionsOutput } from "@/ai/flows/recommend-extensions";
import { PROJECT_TYPES, type UserPreferences } from "@/types";
import { z } from "zod";

// Matches the Genkit flow input schema
const UserPreferencesSchema = z.object({
  testing: z.array(z.string()).optional(),
  lintingFormatters: z.array(z.string()).optional(),
  aiAssistance: z.array(z.string()).optional(),
  security: z.array(z.string()).optional(),
  versionControl: z.array(z.string()).optional(),
  collaboration: z.array(z.string()).optional(),
});

const RecommendActionInputSchema = z.object({
  ideName: z.string().min(1, "IDE name is required."),
  projectType: z.enum(PROJECT_TYPES),
  projectTypeOther: z.string().optional(),
  preferences: UserPreferencesSchema,
  userNotes: z.string().optional(),
});

export type RecommendActionState = {
  data?: RecommendExtensionsOutput;
  input?: RecommendExtensionsInput; // To repopulate form or show in summary
  error?: string;
  fieldErrors?: Record<string, string[] | undefined> | Partial<Record<keyof RecommendExtensionsInput, string[] | undefined>>;
};

export async function getAIRecommendations(
  input: RecommendExtensionsInput
): Promise<RecommendActionState> {
  try {
    const validatedInput = RecommendActionInputSchema.safeParse(input);
    if (!validatedInput.success) {
      console.error("Validation errors:", validatedInput.error.flatten().fieldErrors);
      return {
        error: "Invalid input. Please check the fields.",
        fieldErrors: validatedInput.error.flatten().fieldErrors,
        input, // Send back original input to repopulate form
      };
    }

    const result = await recommendExtensions(validatedInput.data);
    return { data: result, input: validatedInput.data };
  } catch (error) {
    console.error("Error getting AI recommendations:", error);
    // It's good practice to avoid exposing raw error messages to the client
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
    return { error: `Failed to get recommendations. ${errorMessage} Please try again.`, input };
  }
}
