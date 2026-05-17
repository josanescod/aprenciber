FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    iproute2 \
    iputils-ping \
    netcat-openbsd \
    nmap \
    ffuf \
    openssh-client \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN printf '%s\n' \
    'id' \
    'page' \
    'file' \
    'item' \
    'doc' \
    'document' \
    'template' \
    'path' \
    'url' \
    'load' \
    'include' \
    'content' \
    'debug' \
    'view' \
    'section' \
    > /root/params.txt

RUN echo "set -g status off" > /root/.tmux.conf

WORKDIR /root

CMD ["/bin/bash"]