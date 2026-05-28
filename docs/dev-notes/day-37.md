# Usuaris poden modificar dades

- modificació `schemas/user.py` UserProfileUpdate
- afegit mètode update_full_name a `repositories/profile_repositories.py`
- mètode update_password a `supabase_auth_service.py`
- afegit endpoint PATCH a `api/routes/users.py`
- verificació backend amb petició curl
- implementació botó editar, modal i validació de les noves dades al frontend `Dashboard.view`
- frontend `Registerview.vue` validació de la contrassenya amb dos camps de formulari.