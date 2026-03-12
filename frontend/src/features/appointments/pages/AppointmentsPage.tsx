import { DashboardLayout } from "@/app/layout/DashboardLayout";

export function AppointmentsPage() {
  return (
    <DashboardLayout
      title="Appointments"
      description="Appointments list, filters, and navigation."
    >
      <section className="rounded-md border p-4 text-sm text-zinc-700 dark:text-zinc-200">
        Área reservada para listagem de appointments.
      </section>
    </DashboardLayout>
  );
}
