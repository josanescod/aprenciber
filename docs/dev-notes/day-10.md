# Integració del terminal web amb ttyd

- configuració de `ttyd_manager.py`, `ttyd_process_registry`, `lab_cleanup`
- configuració de `labs.py`
- NOTA: tenir present que els terminals ttyd son accessibles sense autenticació mitjançant URL directa. (problema de seguretat? Nginx en producció?)
- en producció el problema de les urls accessibles es podria solucionar amb un reverse proxy que validi JWT? 
- verificació que dos usuaris diferents accedeixin a dos laboratoris diferents.
- verificació que ttyd elimina els processos
- xarxes docker per defecte amb mida molt gran que no les fan ideals per escanejos de xarxa amb `nmap`

