from app.models.appointment import Appointment, AppointmentStatus


class StatusCompromisso:
    agendado = AppointmentStatus.scheduled
    cancelado = AppointmentStatus.cancelled
    concluido = AppointmentStatus.completed


Compromisso = Appointment
