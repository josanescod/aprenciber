# Frontend - Aprenciber

Frontend de la plataforma Aprenciber desenvolupada amb:

- Vue3
- Vite
- Tailwind CSS v4
- pnpm

### Responsabilitats

- Interfície d'usuari (UI)
- Autenticació (Supabase)
- Visualització d'escenaris
- Gestió de laboratoris
- Enviament de flags
- Visualització de progrés

### Estructura

```txt
src/
├── assets/
├── components/
├── App.vue
├── main.js
├── style.css
├── views/ # pàgines
├── services/ # crides a la API
└── router/ # rutes
```

### Execució en desenvolupament

```bash
cd frontend
pnpm install
pnpm dev
```

Aplicació disponible a:

```txt
http://localhost:5173
```

### Estils

S'utilitza Tailwind CSS v4 integrat mitjançant Vite

### Notes

- El frontend s'executa en el host durant el desenvolupament
- En producció es servirà com aplicació estàtica en un servidor web

