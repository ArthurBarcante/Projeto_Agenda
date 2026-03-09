export type CredentialsEntrada = {
  companyIdentifier: string;
  email: string;
  senha: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
};
