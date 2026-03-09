export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ErroHttp extends Error {
  constructor(
    message: string,
    public status: number,
    public detalhe?: unknown
  ) {
    super(message);
    this.name = "ErroHttp";
  }
}

type OpcoesRequisicao = Omit<RequestInit, "body"> & {
  body?: unknown;
};

export async function requisicaoHttp<T>(
  endpoint: string,
  opcoes: OpcoesRequisicao = {}
): Promise<T> {
  const { body, headers, ...restante } = opcoes;

  const resposta = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...restante,
    headers: {
      "Content-Type": "application/json",
      ...(headers ?? {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!resposta.ok) {
    let detalhe: unknown;

    try {
      detalhe = await resposta.json();
    } catch {
      detalhe = await resposta.text();
    }

    throw new ErroHttp("Failed to communicate with API", resposta.status, detalhe);
  }

  if (resposta.status === 204) {
    return undefined as T;
  }

  return (await resposta.json()) as T;
}
