# Actions effectuées sur le serveur de CTFd

Le serveur est un docker, mis en place par vous-savez-pas-qui.


## Connexion

Le VPN, comme d'hab'.

Portainer.
http://192.168.240.8:9000/#/auth

login et mot de passe comme d'hab'.


## Installation open_ssl

    ~/pouet # wget http://github.com/tamuctf/CTFd-multi-question-plugin/archive/master.zip
    Connecting to github.com (192.30.253.112:80)
    Connecting to github.com (192.30.253.113:443)
    wget: can't execute 'ssl_helper': No such file or directory
    wget: error getting response: Connection reset by peer

https://github.com/google/cadvisor/issues/1131

    ~/pouet # apk
        apk-tools 2.6.9, compiled for x86_64.
    usage: apk COMMAND [-h|--help] [-p|--root DIR] [-X|--repository REPO] [-q|--quiet] [-v|--verbose] [-i|--interactive]
               [-V|--version] [-f|--force] [-U|--update-cache] [--progress] [--progress-fd FD] [--no-progress] [--purge]
               [--allow-untrusted] [--wait TIME] [--keys-dir KEYSDIR] [--repositories-file REPOFILE] [--no-network]
               [--no-cache] [--arch ARCH] [--print-arch] [ARGS]...
    (etc...)

    ~/pouet # apt-get
    sh: apt-get: not found

    ~/pouet # apk update
    fetch http://dl-cdn.alpinelinux.org/alpine/v3.4/main/x86_64/APKINDEX.tar.gz
    fetch http://dl-cdn.alpinelinux.org/alpine/v3.4/community/x86_64/APKINDEX.tar.gz
    v3.4.6-298-gf1dfff5 [http://dl-cdn.alpinelinux.org/alpine/v3.4/main]
    v3.4.6-160-g14ad2a3 [http://dl-cdn.alpinelinux.org/alpine/v3.4/community]
    OK: 5980 distinct packages available

    ~/pouet # apk add ca-certificates
    0% [
    OK: 197 MiB in 56 packages

    ~/pouet # apk update ca-certificates
    fetch http://dl-cdn.alpinelinux.org/alpine/v3.4/main/x86_64/APKINDEX.tar.gz
    fetch http://dl-cdn.alpinelinux.org/alpine/v3.4/community/x86_64/APKINDEX.tar.gz
    v3.4.6-298-gf1dfff5 [http://dl-cdn.alpinelinux.org/alpine/v3.4/main]
    v3.4.6-160-g14ad2a3 [http://dl-cdn.alpinelinux.org/alpine/v3.4/community]
    OK: 5980 distinct packages available

    ~/pouet # apk add openssl
    (1/1) Installing openssl (1.0.2n-r0)
    0% [
    1% [#
    2% [###
    3% [###
    4% [####
    4% [#####
    6% [#######
    8% [##########
    100% [##############################################################################################################
    Executing busybox-1.24.2-r14.trigger
    Executing ca-certificates-20161130-r0.trigger
    OK: 197 MiB in 57 packages

    ~/pouet # apk update openssl
    fetch http://dl-cdn.alpinelinux.org/alpine/v3.4/main/x86_64/APKINDEX.tar.gz
    fetch http://dl-cdn.alpinelinux.org/alpine/v3.4/community/x86_64/APKINDEX.tar.gz
    v3.4.6-298-gf1dfff5 [http://dl-cdn.alpinelinux.org/alpine/v3.4/main]
    v3.4.6-160-g14ad2a3 [http://dl-cdn.alpinelinux.org/alpine/v3.4/community]
    OK: 5980 distinct packages available


## Récupération du plugin CTFd-multi-question-plugin

    ~/pouet # wget https://github.com/tamuctf/CTFd-multi-question-plugin/archive/master.zip
    Connecting to github.com (192.30.253.112:443)
    Connecting to codeload.github.com (192.30.253.121:443)
    master.zip            89% |*****************************************************************         | 40240   0:00:
    master.zip           100% |**************************************************************************| 45124   0:00:00 ETA

    ~/pouet # unzip master.zip
    Archive:  master.zip
       creating: CTFd-multi-question-plugin-master/
      inflating: CTFd-multi-question-plugin-master/.gitignore
      inflating: CTFd-multi-question-plugin-master/README.md
      inflating: CTFd-multi-question-plugin-master/__init__.py
       creating: CTFd-multi-question-plugin-master/challenge-assets/
      inflating: CTFd-multi-question-plugin-master/challenge-assets/multi-challenge-create.js
      inflating: CTFd-multi-question-plugin-master/challenge-assets/multi-challenge-create.njk
      inflating: CTFd-multi-question-plugin-master/challenge-assets/multi-challenge-modal.js
      inflating: CTFd-multi-question-plugin-master/challenge-assets/multi-challenge-modal.njk
      inflating: CTFd-multi-question-plugin-master/challenge-assets/multi-challenge-update.js
      inflating: CTFd-multi-question-plugin-master/challenge-assets/multi-challenge-update.njk
      inflating: CTFd-multi-question-plugin-master/multiquestioncreate.png
      inflating: CTFd-multi-question-plugin-master/multiquestionview.png
       creating: CTFd-multi-question-plugin-master/pics/
      inflating: CTFd-multi-question-plugin-master/pics/multiquestioncreate.png
      inflating: CTFd-multi-question-plugin-master/pics/multiquestionview.png

    ~/pouet # ll /opt/CTFd/CTFd/plugins/
    total 24
    -rw-r--r--    1 root     root          4898 Apr  5 17:14 __init__.py
    -rw-r--r--    1 root     root          6139 Apr  5 17:19 __init__.pyc
    drwxr-xr-x    3 root     root          4096 Apr  5 17:19 challenges
    drwxr-xr-x    3 root     root          4096 Apr  5 17:19 keys

    ~/pouet # cp -R CTFd-multi-question-plugin-master /opt/CTFd/CTFd/plugins/

    ~/pouet # ll /opt/CTFd/CTFd/plugins/
    total 28
    drwxr-xr-x    4 root     root          4096 May  1 21:46 CTFd-multi-question-plugin-master
    -rw-r--r--    1 root     root          4898 Apr  5 17:14 __init__.py
    -rw-r--r--    1 root     root          6139 Apr  5 17:19 __init__.pyc
    drwxr-xr-x    3 root     root          4096 Apr  5 17:19 challenges
    drwxr-xr-x    3 root     root          4096 Apr  5 17:19 keys


## Un peu d'alias

    ~/pouet # alias ll='ls -l'


## Activation du plugin

Test avec le compte admin, sur l'interface web de CTFd.

Le plug-in ne semble pas être pris en compte. On ne peut toujours que créer des challenges de type "standard".

Apparement, il y a un moyen à peu près propre de faire en sorte que gunicorn (le serveur web de CTFd) recharge le code python : http://docs.gunicorn.org/en/latest/faq.html#server-stuff

Il faut envoyer des signaux 'HUP' aux processus gunicorn.

    ~/pouet # ps -edf | grep python
        5 root       4:39 {gunicorn} /usr/local/bin/python /usr/local/bin/gunicorn CTFd:create_app() --bind 0.0.0.0:8000 --workers 1 --worker-class gevent --access-logfile /opt/CTFd/CTFd/logs/access.log --error-logfile /opt/CTFd/CTFd/logs/error.log
       15 root       8:05 {gunicorn} /usr/local/bin/python /usr/local/bin/gunicorn CTFd:create_app() --bind 0.0.0.0:8000 --workers 1 --worker-class gevent --access-logfile /opt/CTFd/CTFd/logs/access.log --error-logfile /opt/CTFd/CTFd/logs/error.log
      175 root       0:00 grep python

    ~/pouet # ps aux
    PID   USER     TIME   COMMAND
        1 root       0:00 {docker-entrypoi} /bin/sh /opt/CTFd/docker-entrypoint.sh
        5 root       4:40 {gunicorn} /usr/local/bin/python /usr/local/bin/gunicorn CTFd:create_app() --bind 0.0.0.0:8000 --worke
       15 root       8:11 {gunicorn} /usr/local/bin/python /usr/local/bin/gunicorn CTFd:create_app() --bind 0.0.0.0:8000 --worke
       38 root       0:00 sh
       82 root       0:00 sh
      119 root       0:00 sh
      168 root       0:00 sh
      204 root       0:00 ps aux

(la ligne de commande est coupée, mais ça doit être à cause de la console du portainer qui gère mal les lignes trop longues).

    ~/pouet # kill -HUP 5

    ~/pouet # kill -HUP 15
    sh: can't kill pid 15: No such process

    ~/pouet # ps aux
    PID   USER     TIME   COMMAND
        1 root       0:00 {docker-entrypoi} /bin/sh /opt/CTFd/docker-entrypoint.sh
        5 root       4:40 {gunicorn} /usr/local/bin/python /usr/local/bin/gunicorn CTFd:create_app() --bind 0.0.0.0:8000 --worke
       38 root       0:00 sh
       82 root       0:00 sh
      119 root       0:00 sh
      168 root       0:00 sh
      205 root       0:00 {gunicorn} /usr/local/bin/python /usr/local/bin/gunicorn CTFd:create_app() --bind 0.0.0.0:8000 --worke
      220 root       0:00 ps aux

Quand on envoie le signal 'HUP' au processus gunicorn principal (à priori le premier de la liste), il semblerait que celui-ci détruise les processus gunicorn secondaire pour les recréer ensuite. C'est pourquoi le processus secondaire a changé de PID (il est passé de 15 à 205).

    ~/pouet # kill -HUP 205
    ~/pouet # ps aux
    PID   USER     TIME   COMMAND
        1 root       0:00 {docker-entrypoi} /bin/sh /opt/CTFd/docker-entrypoint.sh
        5 root       4:40 {gunicorn} /usr/local/bin/python /usr/local/bin/gunicorn CTFd:create_app() --bind 0.0.0.0:8000 --worke
       38 root       0:00 sh
       82 root       0:00 sh
      119 root       0:00 sh
      168 root       0:00 sh
      221 root       0:01 {gunicorn} /usr/local/bin/python /usr/local/bin/gunicorn CTFd:create_app() --bind 0.0.0.0:8000 --worke
      236 root       0:00 ps aux
    ~/pouet #

À tester pour la prochaine fois : on ne devrait avoir besoin d'envoyer le signal HUP que au processus gunicorn principal.

Test dans l'interface web : ça marche !

Dans l'admin, lorsqu'on veut en créer un nouveau challenge, on a le choix entre deux types : standard et multiquestionchallenge

Test de création d'un premier challenge : OK.

Test de résolution du challenge, avec le compte admin : OK. (test non détaillé, on verra ça plus tard).


## Test du plugin, découvert d'un bug

Dans l'interface web : suppression du challenge créé lors du chapitre précédent.

Test de création d'un second challenge de type multiquestionchallenge.

Après remplissage des champs, au moment de valider la création : affichage d'une page web "Internal server error".

Second test après s'être déconnecté-reconnecté : même bug.

    ~/pouet # cat /opt/CTFd/CTFd/logs/error.log

Récupération de la fin du fichier de log d'erreur, voir : `error_log_2018_05_02.txt`

REC TODO : analyser ces logs. Mais y'a des choses intéressantes. (Notamment, la réception des signaux 'HUP').

Retour à l'interface web. Test de création, validation, suppression d'un challenge standard. OK.

Donc la plate-forme CTFd marche toujours, c'est juste le plug-in qui ne va pas bien.


## Récupération de la base de données du serveur CTFd

Apparemment, tout est dans une base SQLite : `/opt/CTFd/CTFd/ctfd.db`

Je n'ai pas les moyens (ni les connaissances) pour sortir un fichier du serveur, car il est dans un docker/portainer/etc.

Donc on envoie le fichier sur un serveur de stockage et on le récupère après.

Le site https://transfer.sh permet cela.

Tests d'envoi du fichier via l'instruction `wget`, mais je ne parviens pas à le faire.

Donc : installation de curl.

    ~/pouet # apk add curl
    (1/3) Installing libssh2 (1.7.0-r0)
      0% [(2/3) Installing libcurl (7.59.0-r0)
     21% [#########################(3/3) Installing curl (7.59.0-r0)
     73% [#######################################################################################100% [################################################################################################################Executing busybox-1.24.2-r14.trigger
    OK: 198 MiB in 60 packages

    ~/pouet # curl -version
    curl: no URL specified!
    curl: try 'curl --help' or 'curl --manual' for more information

    ~/pouet # curl --version
    curl 7.59.0 (x86_64-alpine-linux-musl) libcurl/7.59.0 OpenSSL/1.0.2n zlib/1.2.11 libssh2/1.7.0
    Release-Date: 2018-03-14
    Protocols: dict file ftp ftps gopher http https imap imaps pop3 pop3s rtsp scp sftp smb smbs smtp smtps telnet tftp
    Features: AsynchDNS IPv6 Largefile NTLM NTLM_WB SSL libz TLS-SRP UnixSockets HTTPS-proxy

    ~/pouet # curl --upload-file ./test.txt https://transfer.sh/test.txt
    https://transfer.sh/kHpWb/test.txt

Test, via un navigateur web, de l'url : "https://transfer.sh/kHpWb/test.txt"

Ça marche, on retrouve le fichier texte avec ce que j'ai mis dedans au préalable.

    ~/pouet # curl --upload-file /opt/CTFd/CTFd/ctfd.db https://transfer.sh/ctfd.db
    https://transfer.sh/ {{info supprimée}} /ctfd.db

Récupération du fichier `ctfd.db` via l'url de https://transfer.sh

Vérification de la taille du fichier récupéré et du fichier dans le serveur CTFd. C'est la même. À priori, le transfert c'est bien passé.

Le fichier `ctfd.db` n'est pas versionné dans ce repository.

Dans la mesure du possible, j'aimerais éviter d'avoir à le faire, car il y a les flags des challenges existants. C'est pas les challenges du siècle, mais bon...

REC TODO : analyser le contenu de ctfd.db.

Analyse partielle : apparemment, les tables de DB spécifiques au plugin : `multi_question_challenge_model` et `partialsolve` n'ont pas été correctement nettoyée. Du coup ça met le bazar au niveau des clés primaires.

À suivre.


## Installation de sqlite3

Le serveur web arrive à manipuler des bases sqlite, mais ça ne marche pas en ligne de commande (`sqlite3` indique : "not found").

Donc on va l'installer et puis c'est tout.

    ~/pouet # apk add sqlite3
    ERROR: unsatisfiable constraints:
      sqlite3 (missing):
        required by: world[sqlite3]

Boooon, d'accord...

    ~/pouet # apk add sqlite
    (1/1) Installing sqlite (3.13.0-r1)
    Executing busybox-1.24.2-r14.trigger
    OK: 199 MiB in 61 packages

    ~/pouet # sqlite3
    SQLite version 3.13.0 2016-05-18 10:57:30
    Enter ".help" for usage hints.
    Connected to a transient in-memory database.
    Use ".open FILENAME" to reopen on a persistent database.

    sqlite> .exit

    ~/pouet # ll
    total 56
    drwxrwxrwx    4 root     root          4096 May  1 21:44 CTFd-multi-question-plugin-master
    -rw-r--r--    1 root     root         45124 Apr 30 12:14 master.zip
    -rw-r--r--    1 root     root            12 May  1 22:44 test.txt


## Réparation manuelle de la base de données

    ~/pouet # cp /opt/CTFd/CTFd/ctfd.db .

    ~/pouet # ll
    total 140
    drwxrwxrwx    4 root     root          4096 May  1 21:44 CTFd-multi-question-plugin-master
    -rw-r--r--    1 root     root         86016 May  4 10:21 ctfd.db
    -rw-r--r--    1 root     root         45124 Apr 30 12:14 master.zip
    -rw-r--r--    1 root     root            12 May  1 22:44 test.txt

    ~/pouet # sqlite3
    SQLite version 3.13.0 2016-05-18 10:57:30
    Enter ".help" for usage hints.
    Connected to a transient in-memory database.
    Use ".open FILENAME" to reopen on a persistent database.
    sqlite> .open ctfd.db
    sqlite> select * from multi_question_challenge_model;
    5
    sqlite> select * from partialsolve;
    1|5|1|192.168.199.23|{"Pourquoi ?": true, "Qu'est-ce qui est jaune et qui attend ?": true, "2+3 ?": true}|2018-05-01 22:24:59.658593
    sqlite> .exit

On garde cette copie de la base comme sauvegarde.

    ~/pouet # mv ctfd.db ctfd_00.db

Et on va essayer de nettoyer la base du serveur, pour corriger le bug.

    ~/pouet # cd /opt/CTFd/CTFd/

    /opt/CTFd/CTFd # sqlite3
    SQLite version 3.13.0 2016-05-18 10:57:30
    Enter ".help" for usage hints.
    Connected to a transient in-memory database.
    Use ".open FILENAME" to reopen on a persistent database.
    sqlite> .open ctfd.db
    sqlite> delete from partialsolve;
    sqlite> commit;
    Error: cannot commit - no transaction is active
    sqlite> delete from multi_question_challenge_model;
    sqlite> select * from multi_question_challenge_model;
    sqlite> select * from partialsolve;
    sqlite> .exit
    /opt/CTFd/CTFd #

Test dans le navigateur web. Création d'un nouveau plug-in de type multiquestionchallenge.

Ça marche.

Donc le problème, c'est juste qu'il faut bien nettoyer les tables quand on supprime un challenge.

