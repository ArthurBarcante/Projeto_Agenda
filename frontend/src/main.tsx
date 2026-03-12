import { AuthProvider } from "@/app/providers/AuthProvider";
import { ThemeProvider } from "@/app/providers/ThemeProvider";

export function AppProviders({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <ThemeProvider>{children}</ThemeProvider>
    </AuthProvider>
  );
}

export default AppProviders;
