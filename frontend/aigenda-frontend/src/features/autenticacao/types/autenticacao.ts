export type CredenciaisEntrada = {
  identificadorEmpresa: string;
  email: string;
  senha: string;
};

export type RespostaToken = {
  access_token: string;
  token_type: string;
};
