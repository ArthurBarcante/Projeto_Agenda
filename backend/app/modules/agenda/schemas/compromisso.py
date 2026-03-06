from app.modules.schedule.schemas.appointment import AppointmentCreate
from app.modules.schedule.schemas.appointment import AppointmentResponse
from app.modules.schedule.schemas.appointment import AppointmentUpdate
from app.modules.schedule.schemas.appointment import LegacyAppointmentCreate
from app.modules.schedule.schemas.appointment import LegacyAppointmentResponse
from app.modules.schedule.schemas.appointment import LegacyAppointmentUpdate


CompromissoCriacao = AppointmentCreate
CompromissoAtualizacao = AppointmentUpdate
CompromissoResposta = AppointmentResponse

CriacaoCompromissoLegado = LegacyAppointmentCreate
AtualizacaoCompromissoLegado = LegacyAppointmentUpdate
RespostaCompromissoLegado = LegacyAppointmentResponse
