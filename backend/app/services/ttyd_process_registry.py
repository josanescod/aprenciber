# Registre en memoria: lab_id → pid
# Aquest registre es per en reiniciar la instanciade FastAPI
# Per persistir l'estat, el PID es pot recuperar amb el valor del camp 'terminal_pid' guardat a la base de dades en iniciar l'aplicació

_registry: dict[int, int] = {}


def register(lab_id: int, pid: int) -> None:
    _registry[lab_id] = pid


def get_pid(lab_id: int) -> int | None:
    return _registry.get(lab_id)


def unregister(lab_id: int) -> None:
    _registry.pop(lab_id, None)
