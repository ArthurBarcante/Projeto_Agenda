import type { AppointmentApi } from "@/features/appointments/types";
import { endpoints, http } from "@/services/api";

export async function listAppointments(): Promise<AppointmentApi[]> {
  return http<AppointmentApi[]>(endpoints.appointments.list, {
    method: "GET",
  });
}
