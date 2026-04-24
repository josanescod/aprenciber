FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    iproute2 \
    iputils-ping \
    netcat-openbsd \
    ftp \
    nmap \
    hydra \
    && rm -rf /var/lib/apt/lists/*


RUN cat > /root/passwords.txt << 'EOF'
cavall707
alfil123
reinanegra
escacmat
enrocllarg
torre789
peoblanc1
enroccurt6
escacmat
gambitdama1
EOF

WORKDIR /root

CMD ["/bin/bash"]