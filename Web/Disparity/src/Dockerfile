FROM php:8.2-apache

WORKDIR /var/www/html

# Installation des dépendances
RUN apt-get update && apt-get install -y supervisor

# Configuration d'Apache
COPY ./apache.conf /etc/apache2/sites-available/000-default.conf
RUN a2enmod proxy proxy_http

# Copie des fichiers
COPY ./front /var/www/html/front
COPY ./back /var/www/html/back

# Configuration de Supervisor
COPY ./supervisor.conf /etc/supervisor/conf.d/

EXPOSE 80 8080

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
