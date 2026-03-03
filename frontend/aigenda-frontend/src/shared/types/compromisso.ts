export type Compromisso = {
  id: string;
  titulo: string;
  inicioEm: string;
  fimEm: string;
  status: "scheduled" | "cancelled" | "completed";
};
