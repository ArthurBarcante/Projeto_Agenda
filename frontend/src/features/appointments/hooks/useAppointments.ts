import { listAppointments } from "@/features/appointments/services/appointmentsService";
import type { AppointmentApi } from "@/features/appointments/types";
import { useEffect, useState } from "react";

export function useAppointments() {
  const [items, setItems] = useState<AppointmentApi[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let isActive = true;

    async function load() {
      try {
        const data = await listAppointments();
        if (isActive) {
          setItems(data);
        }
      } finally {
        if (isActive) {
          setLoading(false);
        }
      }
    }

    void load();

    return () => {
      isActive = false;
    };
  }, []);

  return { items, loading };
}
