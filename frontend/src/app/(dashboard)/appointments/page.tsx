import { AppointmentsPage } from "@/features/appointments/pages/AppointmentsPage";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Appointments",
  description: "Page responsible for appointments listing and navigation.",
};

export default function AppointmentsRoute() {
  return <AppointmentsPage />;
}
