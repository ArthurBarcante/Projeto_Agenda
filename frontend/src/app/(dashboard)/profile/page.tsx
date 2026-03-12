import { ProfilePage } from "@/features/users/pages/ProfilePage";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Profile",
  description: "Page responsible for authenticated user data and preferences.",
};

export default function ProfileRoute() {
  return <ProfilePage />;
}
