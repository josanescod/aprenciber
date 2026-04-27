import os
import signal
import socket
import subprocess


class TtydManager:

    def start_terminal(self, container_name: str) -> tuple[int, int]:
        """
        Arranca un proceso ttyd con límite de 1 cliente.
        Devuelve (port, pid).
        """
        port = self._get_free_port()

        process = subprocess.Popen(
            [
                "ttyd",
                "--writable",
                "-i",
                "127.0.0.1",
                "-p",
                str(port),
                "--max-clients",
                "1",
                "--client-option",
                "fontSize=16",
                "--",
                "docker",
                "exec",
                "-it",
                container_name,
                "tmux",
                "new-session",
                "-A",
                "-s",
                "main",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return port, process.pid

    def stop_terminal(self, pid: int) -> None:
        try:
            os.kill(pid, signal.SIGTERM)
            try:
                os.waitpid(pid, 0)
            except ChildProcessError:
                pass
        except ProcessLookupError:
            pass
        except OSError as exc:
            print(f"[TtydManager] Warning: could not stop ttyd pid {pid}: {exc}")

    def _get_free_port(self) -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
