# Backend - Aprenciber

Backend de la plataforma Aprenciber desenvolupada amb **FastAPI**.

### Responsabilitats

- API REST per al frontend
- Gestió d'usuaris (autenticació via Supabase)
- Gestió d'escenaris (format YAML)
- Creació i destrucció de laboratoris (contenidors Docker)
- Validació de flags
- Registre de progrés d'usuaris

# Estructura

```txt
app/
├── api/ # endpoints
├── core/ # configuració global
├── models/ # models de base de dades
├── services/ # lògica de negoci
├── repositories/ # accés a dades
├── infraestructure/ # integracions externes (Docker, YAML, db)
```

### Execució en desenvolupament

```bash
cd backend
source .venv/bin/activate
fastapi dev
```

### Endpoint de prova

```bash
GET /health
```

### Notes

- El backend s'executa directament al host durant el desenvolupament
- S'utilitza Docker per aprovisionar els laboratoris