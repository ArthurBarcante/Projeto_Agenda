import { endpointsApi } from "@/shared/api/endpoints";
import { requisicaoHttp } from "@/shared/api/httpClient";

import type { AppointmentApi } from "@/features/appointments/types/appointment";

export async function listAppointments(): Promise<AppointmentApi[]> {
  return requisicaoHttp<AppointmentApi[]>(endpointsApi.appointments.list, {
    method: "GET",
  });
}

export const listAppointments = listAppointments;
