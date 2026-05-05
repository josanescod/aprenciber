# Registre d'usuaris

- Qualsevol usuari es pot registrar a la url /register 
- Rep un correu electronic amb un link de registre via Gmail SMTP
- El link de registre redirigeix a /auth/callback que redirigeix al dashboard
- El backend crea automaticament el registre a potsgres amb el rol per defecte 'student'
- El login segueix igual
- L'enllaç de registre apareix a sota de Login i al de Registre un cap a Login