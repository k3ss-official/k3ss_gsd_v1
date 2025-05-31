import type React from 'react';

interface AppContainerProps {
  children: React.ReactNode;
}

export function AppContainer({ children }: AppContainerProps) {
  return (
    <div className="flex min-h-screen flex-col items-center bg-background text-foreground">
      <main className="container mx-auto flex w-full max-w-4xl flex-1 flex-col px-4 py-8 sm:py-12 md:py-16">
        {children}
      </main>
      <footer className="py-6 text-center text-sm text-muted-foreground">
        © {new Date().getFullYear()} Vibe Coder. All rights reserved.
      </footer>
    </div>
  );
}
