FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    openssh-server \
    passwd \
    findutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Usuari del lab
RUN useradd -m -s /bin/bash sam && echo "sam:gamyi" | chpasswd

# Configurar SSH
RUN mkdir -p /var/run/sshd && \
    sed -i \
    -e 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' \
    -e 's/^#\?PermitRootLogin.*/PermitRootLogin no/' \
    /etc/ssh/sshd_config

# Fitxers amb informacio confidencial
RUN printf '%s\n' \
    'ls -la ~' \
    'cat ~/note.txt' \
    'pwd' \
    'cat ~/backup.txt' \
    > /home/sam/.bash_history

RUN echo "nota interna: revisar credencials antigues del sistema de comandes" > /home/sam/note.txt && \
    echo "ssh_user=sam" > /home/sam/backup.txt && \
    echo "ssh_password=gamyi" >> /home/sam/backup.txt && \
    chown -R sam:sam /home/sam && \
    chmod 755 /home/sam && \
    chmod 644 /home/sam/.bash_history /home/sam/note.txt /home/sam/backup.txt

# Flag final: no llegible per Apache/www-data, sí per sam
RUN mkdir -p /opt/secret && \
    touch /opt/secret/flag.txt && \
    chown -R sam:sam /opt/secret && \
    chmod 700 /opt/secret && \
    chmod 600 /opt/secret/flag.txt

#  Esborrar web per defecte
RUN rm -f /var/www/html/index.html

# Pagina principal vulnerable
RUN cat <<'EOF' > /var/www/html/index.php
<?php
echo '
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Tresors de la Comarca - Fruites i verdures a domicili</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f8ef;
            margin: 0;
            color: #2f3e2f;
        }
        header {
            background: #3f7d20;
            color: white;
            padding: 25px;
            text-align: center;
        }
        nav {
            background: #dfeecb;
            padding: 12px;
            text-align: center;
        }
        nav a {
            margin: 0 12px;
            color: #2f5d1e;
            text-decoration: none;
            font-weight: bold;
        }
        main {
            max-width: 900px;
            margin: 30px auto;
            padding: 20px;
        }
        .hero {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .products {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 25px;
        }
        .card {
            background: white;
            padding: 18px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .price {
            color: #3f7d20;
            font-weight: bold;
        }
        footer {
            text-align: center;
            padding: 18px;
            color: #666;
        }
        .notice {
            background: #fff8d6;
            border-left: 5px solid #d6a700;
            padding: 12px;
            margin-top: 20px;
        }
    </style>
</head>
<body>

<header>
    <h1>Tresors de la Comarca</h1>
    <p>Fruites i verdures directes del camp a casa</p>
</header>

<nav>
    <a href="/">Inici</a>
    <a href="/index.php?view=cataleg.html">Productes</a>
    <a href="/index.php?view=temporada.html">Temporada</a>
    <a href="/index.php?view=contacte.html">Contacte</a>
</nav>

<main>
    <section class="hero">
        <h2>La teva cistella saludable</h2>
        <p>
            A Tresors de la Comarca treballem amb els millors hobbits locals per portar-te
            productes frescos, de temporada i sense intermediaris.
        </p>

        <div class="notice">
            Sistema intern de visualitzacio de documents actiu.
        </div>
    </section>

    <section class="products">
        <div class="card">
            <h3>Enciams ecologics</h3>
            <p class="price">4.20 €/kg</p>
        </div>
        <div class="card">
            <h3>Pomes de temporada</h3>
            <p class="price">3.20 €/kg</p>
        </div>
        <div class="card">
            <h3>Espinacs premium</h3>
            <p class="price">0.80 €/unitat</p>
        </div>
    </section>
';

if (isset($_GET['view'])) {
    echo '<section class="hero" style="margin-top:25px;">';
    echo '<h2>Document intern</h2>';
    include($_GET['view']);
    echo '</section>';
}

echo '
</main>

<footer>
    Tresors de la Comarca &copy; 2026 - Comandes locals de fruita i verdura.
</footer>

</body>
</html>
';
?>
EOF

# Pàginas internes falses
RUN cat <<'EOF' > /var/www/html/cataleg.html
<h3>Cataleg semanal</h3>
<ul>
    <li>Pressecs blaus - 1.80 €/kg</li>
    <li>Peres classiques - 2.30 €/kg</li>
    <li>Pastanagues magiques - 5.80 €/kg</li>
    <li>Taronja energetica - 4.20 €/kg</li>
</ul>
EOF

RUN cat <<'EOF' > /var/www/html/temporada.html
<h3>Productes de temporada</h3>
<p>Aquesta setmana recomanem platans, carxofes i maduixes.</p>
EOF

RUN cat <<'EOF' > /var/www/html/contacte.html
<h3>Contacte</h3>
<p>Email: samsagazaemprenedor@comarca.local</p>
<p>Horari: dilluns a dissabte, 8:00 - 17:00</p>
EOF

RUN chown -R www-data:www-data /var/www/html

EXPOSE 80 22

CMD ["/bin/bash", "-c", "service ssh start && exec apachectl -D FOREGROUND"]