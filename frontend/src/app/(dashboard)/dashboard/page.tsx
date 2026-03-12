import { DashboardPage } from "@/features/appointments/pages/DashboardPage";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Dashboard",
  description: "Page responsible for the authenticated area overview.",
};

export default function DashboardRoute() {
  return <DashboardPage />;
}
