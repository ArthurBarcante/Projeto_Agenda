import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "AIGENDA | Home",
  description: "Entry page for authentication and internal area navigation.",
};

export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col justify-center gap-6 px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">AIGENDA</h1>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Entry page to direct the user to authentication flows
        e area autenticada.
      </p>

      <div className="flex flex-wrap gap-3">
        <Link className="rounded-md border px-4 py-2" href="/login">
          SignIn
        </Link>
        <Link className="rounded-md border px-4 py-2" href="/dashboard">
          Dashboard
        </Link>
        <Link className="rounded-md border px-4 py-2" href="/appointments">
          Appointments
        </Link>
        <Link className="rounded-md border px-4 py-2" href="/profile">
          Profile
        </Link>
      </div>
    </main>
  );
}
