# Autenticació amb Supabase

- configuració dels fitxers aprenciber/.env i aprenciber/frontend/.env amb url i api_key de Supabase
- instal·lació de `pip install supabase` al backend
- fluxe supabase autentica -> frontend rep jwt -> crida a /api/users/me amb Bearer <token>-> backend valida i retorna perfil
- instal·lació del paquet al frontend `pnpm add @supabase/supabase-js`