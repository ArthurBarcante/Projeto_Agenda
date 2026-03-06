import { endpointsApi } from "@/shared/api/endpoints";
import { requisicaoHttp } from "@/shared/api/httpClient";

import type { CompromissoApi } from "@/features/compromissos/types/compromisso";

export async function listAppointments(): Promise<CompromissoApi[]> {
  return requisicaoHttp<CompromissoApi[]>(endpointsApi.appointments.list, {
    method: "GET",
  });
}

export const listarCompromissos = listAppointments;
