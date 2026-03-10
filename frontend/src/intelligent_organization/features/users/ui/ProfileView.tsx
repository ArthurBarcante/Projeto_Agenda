import { PaginaBase } from "@/shared/components/PaginaBase";

export function ProfileView() {
  return (
    <PaginaBase
      title="Profile"
      description="Authenticated user data and basic preferences."
    >
      <section className="rounded-md border p-4 text-sm text-zinc-700 dark:text-zinc-200">
        Área reservada para profile do user.
      </section>
    </PaginaBase>
  );
}
