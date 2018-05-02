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


