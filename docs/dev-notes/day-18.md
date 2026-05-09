# Panell admin

- backend modificació de `repositories/profile_repository.py`per afegir un mètode get_all per llistar usuaris de la db
- nou schema per afegir UserListItem amb `is_active`
- endpoint protegit amb `require_admin` GET /api/users
- frontend reestructuració del panell Admin amb dos nou tags `AdminLayoutView.vue` `AdminUsersView.vue` `AdminScenariosView.vue`
- nova ruta a `router/index.js` `/admin` convertida amb subrutes `admin-users` i `admin-scenarios`
- verificació dels endpoints