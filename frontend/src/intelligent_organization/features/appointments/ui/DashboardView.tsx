import Link from "next/link";

import { PaginaBase } from "@/shared/components/PaginaBase";

export function DashboardView() {
  return (
    <PaginaBase
      title="Dashboard"
      description="Resumo operacional com atalhos para os fluxos principais."
    >
      <section className="flex flex-wrap gap-3">
        <Link className="rounded-md border px-4 py-2" href="/appointments">
          Ver appointments
        </Link>
        <Link className="rounded-md border px-4 py-2" href="/profile">
          Ver profile
        </Link>
      </section>
    </PaginaBase>
  );
}
