export function formatarDataHora(valor: string): string {
  const dataConvertida = new Date(valor);

  if (Number.isNaN(dataConvertida.getTime())) {
    return valor;
  }

  return dataConvertida.toLocaleString("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  });
}
