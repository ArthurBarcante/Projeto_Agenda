import { endpointsApi } from "@/shared/api/endpoints";
import { requisicaoHttp } from "@/shared/api/httpClient";

import type { CredenciaisEntrada, RespostaToken } from "@/features/autenticacao/types/autenticacao";

export async function login(credentials: CredenciaisEntrada): Promise<RespostaToken> {
  return requisicaoHttp<RespostaToken>(endpointsApi.auth.login, {
    method: "POST",
    body: {
      company_slug: credentials.identificadorEmpresa,
      email: credentials.email,
      password: credentials.senha,
    },
  });
}

export const entrar = login;
