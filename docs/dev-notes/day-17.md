# Aplicar politiques de rol d'usuari al frontend

- afegits a `auth.js` els mètodes `isAdmin`, `isTeacher`, `isStudent`
- `router/index.js` modificat per afegir guardes per rol
- `AdminView.vue` accessible només per al rol admin
- `TeacherView.vue` accessible només per al rol teacher
- `AppLayout.vue` afegit els condicionals per a admin i teacher al nav
