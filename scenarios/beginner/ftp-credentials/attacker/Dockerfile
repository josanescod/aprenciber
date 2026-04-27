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
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN echo "set -g status off" > /root/.tmux.conf

WORKDIR /root

CMD ["/bin/bash"]