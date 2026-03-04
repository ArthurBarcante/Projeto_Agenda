import { endpointsApi } from "@/shared/api/endpoints";
import { requisicaoHttp } from "@/shared/api/httpClient";

import type { CredenciaisEntrada, RespostaToken } from "@/features/autenticacao/types/autenticacao";

export async function entrar(credenciais: CredenciaisEntrada): Promise<RespostaToken> {
  return requisicaoHttp<RespostaToken>(endpointsApi.autenticacao.entrar, {
    method: "POST",
    body: {
      company_slug: credenciais.identificadorEmpresa,
      email: credenciais.email,
      password: credenciais.senha,
    },
  });
}
