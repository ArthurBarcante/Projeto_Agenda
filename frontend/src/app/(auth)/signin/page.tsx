import { SignInPage } from "@/features/auth/pages/SignInPage";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | SignIn",
  description: "Page responsible for the user authentication flow.",
};

export default function SignInRoute() {
  return <SignInPage />;
}
