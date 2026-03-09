import { PaginaBase } from "@/shared/components/PaginaBase";

export function SignInView() {
  return (
    <PaginaBase
      title="SignIn"
      description="Authentication by company, email, and password."
    >
      <section className="rounded-md border p-4 text-sm text-zinc-700 dark:text-zinc-200">
        Area reserved for the authentication form.
      </section>
    </PaginaBase>
  );
}
