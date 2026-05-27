# Funcionalitat dels estudiants per eliminar el seu compte

- Els estudiants han de poder eliminar el seu compte.
- Els professors nomes els pot esborrar l'admin ja que el professor pot tenir diverses aules i alumnes i no poden quedar aules sense professor.
- Admin pot desactivar qualsevol usuari del panell
- Eliminar labs actius de l'estudiant, eliminar el seu perfil, i l'usuari de Supabase.
- funció delete_user a `supabase_auth_service.py`
- funció delete a `profile_repository.py`
- frontend botó eliminar compte `DashboardView.vue`
- admin per defecte al iniciar l'app.