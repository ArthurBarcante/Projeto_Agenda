import type { CredentialsInput, TokenResponse } from "@/features/auth/types";
import { endpoints, http } from "@/services/api";

export async function login(
  credentials: CredentialsInput
): Promise<TokenResponse> {
  return http<TokenResponse>(endpoints.auth.login, {
    method: "POST",
    body: {
      company_slug: credentials.companyIdentifier,
      email: credentials.email,
      password: credentials.password,
    },
  });
}
