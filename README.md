ESIH MAKERLAB
=============


## Configurez un envirronnement de développement

### Ubuntu 

1. Installer les dépendences du système d'exploitation:
        ` sudo apt-get install python3-dev build-essential wget libpd-dev`
1. Installer et configurer la base de donnée PostgreSQL 
        `make install-db`
1. Configurez les variables d'envirronnement: 
        - Copiez les éléments du fichier .env.template dans le fichier bashrc  
          `cd /home/<username>`
          `nano .bashrc`

          Copiez les en y ajoutant export devant chacune des variables:
            export DJANGO_SECRET_KEY='dfwgtyede6d674r667dgedh' 

1. Installer les dépendences python et executer les migrations
        `make install`

1. Faire tourner:
        `make run`