import { AppointmentsView } from "@/features/appointments/ui/AppointmentsView";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Appointments",
  description: "Page responsible for appointments listing and navigation.",
};

export default function AppointmentsPage() {
  return <AppointmentsView />;
}
