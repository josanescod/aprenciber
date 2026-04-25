FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    vsftpd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m magnus && echo "magnus:gambitdama1" | chpasswd

RUN echo "FLAG{demo_ftp_credentials}" > /home/magnus/flag.txt \
    && chown magnus:magnus /home/magnus/flag.txt \
    && chmod 644 /home/magnus/flag.txt

RUN mkdir -p /var/run/vsftpd/empty

RUN mkdir -p /var/ftp/public

RUN echo "magnus sempre reutilitza els seus passwords d'escacs" > /var/ftp/public/note.txt

RUN printf '%s\n' \
    'cavall707' \
    'alfil123' \
    'reinanegra' \
    'escacmat' \
    'enrocllarg' \
    'torre789' \
    'peoblanc1' \
    'enroccurt6' \
    'escacmat' \
    'peonegre7' \
    'alfilblanc12' \
    'reynegre' \
    'gambitdama1' \
    > /var/ftp/public/user_magnus_old.txt

RUN chown root:root /var/ftp \
    && chmod 555 /var/ftp \
    && chown -R ftp:ftp /var/ftp/public \
    && chmod -R 755 /var/ftp/public

RUN cat > /etc/vsftpd.banner << 'EOF'
#############################################
#                                           #
#      Benvingut al servidor FTP intern     #
#                                           #
#############################################


EOF

COPY vsftpd.conf /etc/vsftpd.conf

EXPOSE 21 30000-30009

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]