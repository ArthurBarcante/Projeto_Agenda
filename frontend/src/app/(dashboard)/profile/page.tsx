import { ProfileView } from "@/features/users/ui/ProfileView";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Profile",
  description: "Page responsible for authenticated user data and preferences.",
};

export default function ProfilePage() {
  return <ProfileView />;
}
