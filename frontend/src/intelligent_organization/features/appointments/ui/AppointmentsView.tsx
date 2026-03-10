import { PaginaBase } from "@/shared/components/PaginaBase";

export function AppointmentsView() {
  return (
    <PaginaBase
      title="Appointments"
      description="Appointments list, filters, and navigation."
    >
      <section className="rounded-md border p-4 text-sm text-zinc-700 dark:text-zinc-200">
        Área reservada para listagem de appointments.
      </section>
    </PaginaBase>
  );
}
