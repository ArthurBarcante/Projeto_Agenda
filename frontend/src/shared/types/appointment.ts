export type AppointmentAlias = {
  id: string;
  title: string;
  inicioEm: string;
  fimEm: string;
  status: "scheduled" | "cancelled" | "completed";
};
