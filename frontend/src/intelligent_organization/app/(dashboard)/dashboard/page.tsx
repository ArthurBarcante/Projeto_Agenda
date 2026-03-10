import { DashboardView } from "@/features/appointments/ui/DashboardView";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Dashboard",
  description: "Page responsible for the authenticated area overview.",
};

export default function DashboardPage() {
  return <DashboardView />;
}
