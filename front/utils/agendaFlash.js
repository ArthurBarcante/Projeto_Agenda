export const AGENDA_FLASH_STORAGE_KEY = "agendaFlashMessage";

export function consumeAgendaFlashMessage() {
  try {
    const rawMessage = window.sessionStorage.getItem(AGENDA_FLASH_STORAGE_KEY);
    if (!rawMessage) return null;
    window.sessionStorage.removeItem(AGENDA_FLASH_STORAGE_KEY);
    return JSON.parse(rawMessage);
  } catch {
    window.sessionStorage.removeItem(AGENDA_FLASH_STORAGE_KEY);
    return null;
  }
}

export function saveAgendaFlashMessage(message) {
  try {
    window.sessionStorage.setItem(
      AGENDA_FLASH_STORAGE_KEY,
      JSON.stringify({ type: "success", message }),
    );
  } catch (error) {
    console.warn("Nao foi possivel salvar a mensagem de retorno da agenda.", error);
  }
}
