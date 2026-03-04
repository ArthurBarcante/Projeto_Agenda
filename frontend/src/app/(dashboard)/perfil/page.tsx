import { PerfilView } from "@/features/usuarios/ui/PerfilView";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Perfil",
  description: "Página responsável por dados e preferências do usuário autenticado.",
};

export default function PerfilPage() {
  return <PerfilView />;
}
