FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openssh-server \
    tftpd-hpa \
    sudo \
    nano \
    bash \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Usuario del repte
RUN useradd -m -s /bin/bash gabriel

# Configurar SSH port 2222
RUN mkdir -p /var/run/sshd && \
    sed -i \
      -e 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' \
      -e 's/^#\?PermitRootLogin.*/PermitRootLogin no/' \
      -e 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' \
      /etc/ssh/sshd_config && \
    echo "Port 2222" >> /etc/ssh/sshd_config

# Directori TFTP
RUN mkdir -p /srv/tftp/.ssh

# Generar clae SSH filtrada
RUN ssh-keygen -t rsa -b 2048 -f /srv/tftp/.ssh/id_rsa -N "" -C "gabriel@target"

# Instalar cl upública per a usuari gabriel
RUN mkdir -p /home/gabriel/.ssh && \
    cp /srv/tftp/.ssh/id_rsa.pub /home/gabriel/.ssh/authorized_keys && \
    chown -R gabriel:gabriel /home/gabriel/.ssh && \
    chmod 700 /home/gabriel/.ssh && \
    chmod 600 /home/gabriel/.ssh/authorized_keys

# README visible per TFTP
RUN printf '%s\n' \
    'Copia de seguretat obsoleta.' \
    '' \
    'Es possible que encara hi hagi antics fitxers interessants.' \
    > /srv/tftp/README.txt

# Historial filtrat per TFTP
RUN printf '%s\n' \
    'whoami' \
    'id' \
    'ssh gabriel@localhost -p 2222' \
    'cat ~/note.txt' \
    'sudo -l' \
    > /srv/tftp/.bash_history

# Nota usuari
RUN printf '%s\n' \
    'Nota interna:' \
    '' \
    'Aquest servidor utilitza nano per a tasques de manteniment.' \
    '' \
    'Consulteu GTFObins si els permisos sudo resulten sospitosos.' \
    > /home/gabriel/note.txt

RUN chown gabriel:gabriel /home/gabriel/note.txt && \
    chmod 644 /home/gabriel/note.txt

# Escalada de privilegis amb nano
RUN echo 'gabriel ALL=(root) NOPASSWD: /usr/bin/nano' > /etc/sudoers.d/gabriel-nano && \
    chmod 440 /etc/sudoers.d/gabriel-nano

# Permisos TFTP
RUN chmod 755 /srv/tftp && \
    chmod 755 /srv/tftp/.ssh && \
    chmod 644 /srv/tftp/README.txt && \
    chmod 644 /srv/tftp/.bash_history && \
    chmod 644 /srv/tftp/.ssh/id_rsa && \
    chmod 644 /srv/tftp/.ssh/id_rsa.pub

EXPOSE 69/udp 2222

CMD ["/bin/bash", "-c", "service ssh start && exec /usr/sbin/in.tftpd --foreground --listen --user root --address 0.0.0.0:69 --secure /srv/tftp"]