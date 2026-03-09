import { useEffect, useState } from "react";

import { listAppointments } from "@/features/appointments/services/appointments_service";
import type { AppointmentApi } from "@/features/appointments/types/appointment";

export function useAppointments() {
  const [itens, setItens] = useState<AppointmentApi[]>([]);
  const [carregando, setCarregando] = useState<boolean>(true);

  useEffect(() => {
    let is_active = true;

    async function loadAppointments() {
      try {
        const resposta = await listAppointments();
        if (is_active) {
          setItens(resposta);
        }
      } finally {
        if (is_active) {
          setCarregando(false);
        }
      }
    }

    void loadAppointments();

    return () => {
      is_active = false;
    };
  }, []);

  return { itens, carregando };
}
