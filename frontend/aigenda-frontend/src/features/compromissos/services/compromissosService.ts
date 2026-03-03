import { endpointsApi } from "@/shared/api/endpoints";
import { requisicaoHttp } from "@/shared/api/httpClient";

import type { CompromissoApi } from "@/features/compromissos/types/compromisso";

export async function listarCompromissos(): Promise<CompromissoApi[]> {
  return requisicaoHttp<CompromissoApi[]>(endpointsApi.compromissos.listar, {
    method: "GET",
  });
}
