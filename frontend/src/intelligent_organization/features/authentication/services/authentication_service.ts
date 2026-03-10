import { endpointsApi } from "@/shared/api/endpoints";
import { requisicaoHttp } from "@/shared/api/httpClient";

import type { CredentialsEntrada, TokenResponse } from "@/features/authentication/types/authentication";

export async function login(credentials: CredentialsEntrada): Promise<TokenResponse> {
  return requisicaoHttp<TokenResponse>(endpointsApi.auth.login, {
    method: "POST",
    body: {
      company_slug: credentials.companyIdentifier,
      email: credentials.email,
      password: credentials.senha,
    },
  });
}

export const login = login;
