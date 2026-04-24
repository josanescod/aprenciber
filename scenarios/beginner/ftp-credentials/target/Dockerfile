FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    vsftpd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m magnus && echo "magnus:gambitdama1" | chpasswd

RUN echo "FLAG{demo_ftp_credentials}" > /home/magnus/flag.txt \
    && chown magnus:magnus /home/magnus/flag.txt \
    && chmod 644 /home/magnus/flag.txt

RUN mkdir -p /var/run/vsftpd/empty

COPY vsftpd.conf /etc/vsftpd.conf

EXPOSE 21

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]