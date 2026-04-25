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


WORKDIR /root

CMD ["/bin/bash"]