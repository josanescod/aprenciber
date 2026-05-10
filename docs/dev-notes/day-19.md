# Modificar rol d'usuari

- modificació al backend de `api/routes/user.py` `app/repositories/profile_repository.py` `app/schemas/user.py` per actualitzar el rol d'usuari.
- proves per verificar que només l'admin pot modificar el rol. La resta error 403.
- admins a la vista poden modificar el rol a la resta d'usuaris.
- admins no veuen el selector, no poden canviar el rol d'admin.
- `AdminUsersView` frontend actualitza el selector sense carregar