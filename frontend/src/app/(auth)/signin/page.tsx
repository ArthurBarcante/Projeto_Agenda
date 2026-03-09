import { SignInView } from "@/features/authentication/ui/SignInView";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | SignIn",
  description: "Page responsible for the user authentication flow.",
};

export default function SignInPage() {
  return <SignInView />;
}
