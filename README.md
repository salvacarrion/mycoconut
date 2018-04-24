# Coconut's Django server

This project is used to test small projects and experiements that I post online

## THIS IS SETUP NO UP-TO-DATE SO TAKE IT WITH A GRAIN OF SALT


Requirements
---

- Python 3
- pip3
- virtualenv
- mysql-client
- nginx
- supervisor


Installation
---

1. Run `ubuntu_setup.sh`
2. Add `config/.bashrc` shortchuts to `.bashrc`
3. Setup nginx
4. Setup supervisor


Basic deployment (draft)
---
1. Create gmail account
2. Create Google Cloud account (1-year free)
3. Create Compute Engine instance (small)
    1. Access from the local console
        1. Log in gcloud (gcloud auth login ...)
            1. Check default configuration (gcloud config list)
        2. If there are problems, delete previous public keys
    2. Check whether you can access
        1. Using the console
        2. Through SFTP (Cyberduck)
    3. Add shortcut to the terminal (to speed-up things)
    4. Update certificates (in the code)
    5. Install initial requirements (mysql, python, supervisor, ...)
4. Create CloudSQL instance (MySql 2nd gen) - (...Or use sqlite and f*ck it!)
    1. Authorize IP "Home" (temp)
    2. Create certificates (from the web)
        1. Add them to the project
        2. Add them to ~ / .ssh
        3. Update codes (if necessary)
    3. Check that you can access
        1. Using the console
        2. Through an IDE (DataGrip/MySQLWorkbench)
    4. Add shortcut to the terminal
    5. Import database *
5. Verify domain (bare IPs present problems with (self-signed) certificates, browsers,...)
6. Create static and media buckets (EU)
    1. Add files
    2. Check files
    3. Delete cache folder
    4. Make public bucket (Add member -> allUsers -> Storage Object Viewer)
    5. Fix CORS problem
7. Create credential API service account key (storage-auth.json)
    1. Update code
8. Run web in local - (Remote DB and buckets)
10. Add/Update Google Analytics (if you want)
11. Update Github
12. Clone code to the server (`git clone ...`)
13. Create virtual environment and install requirements
    1. Ensuring the requirements have a specific version (*PLEASE WRITE THE FUCKING DEPENDENCY VERSIONS!!!!*)
14. Update settings.py
15. Add shortcuts to .bashrc
16. Configure Nginx
17. Configure supervisor
18. Configure Let'sEncrypt
    1. Install certbot
    2. Prepare Nginx
        1. Disable routes from letsencrypt of the nginx config
    3. Allowing HTTPS Through the Firewall (Activate UFW)
    4. Obtain certificate
    5. Updating Diffie-Hellman Parameters
    6. Setting Up Auto Renewal (crontab, usually is automatic /etc/cron.d)
19. Authorize ComputeEngine instance to access the CloudSQL (external)
20. Read logs
21. Check browser console
22. Check caches and reset
23. Make static external IP


The CORS problem
---

**1. [Google Cloud] Configuring CORS on a Bucket**

    gsutil cors set cors-json-file.json gs://example

where *cors-json-file.json* is a your CORS configuration file:

```
[
    {
      "origin": ["http://example.appspot.com"],
      "responseHeader": ["Content-Type"],
      "method": ["GET", "HEAD", "DELETE"],
      "maxAgeSeconds": 3600
    }
]
```

> **More:** [https://cloud.google.com/storage/docs/cross-origin](https://cloud.google.com/storage/docs/cross-origin)

 **2. [Nginx] Force Access-Control-Allow-Origin**

Go to */etc/nginx/sites-available/[your_server_config]* and add this line into your server block:

    add_header Access-Control-Allow-Origin *;

> **More:** [https://serverfault.com/questions/162429/how-do-i-add-access-control-allow-origin-in-nginx](https://serverfault.com/questions/162429/how-do-i-add-access-control-allow-origin-in-nginx)

 **3. [Django-cors] Adds CORS headers to Django responses.**

Check this out:

 - [https://github.com/ottoyiu/django-cors-headers](https://github.com/ottoyiu/django-cors-headers)
 - [https://stackoverflow.com/questions/28046422/django-cors-headers-not-work/28834566](https://stackoverflow.com/questions/28046422/django-cors-headers-not-work/28834566)

> **More things:**
> [https://cloud.google.com/storage/docs/cross-origin](https://cloud.google.com/storage/docs/cross-origin)
> [https://stackoverflow.com/questions/26189835/cors-error-on-chrome-with-google-fonts/44855107#44855107](https://stackoverflow.com/questions/26189835/cors-error-on-chrome-with-google-fonts/44855107#44855107)
> [https://stackoverflow.com/questions/22476273/no-access-control-allow-origin-header-is-present-on-the-requested-resource-i](https://stackoverflow.com/questions/22476273/no-access-control-allow-origin-header-is-present-on-the-requested-resource-i)


Install Celery
---

**1. Install RabbitMQ outside the virtual environment**

- Ubuntu:

    sudo apt-get install rabbitmq-server

- Mac OS X:

    brew install rabbitmq

**2. Start RabbitMQ**

    sudo rabbitmq-server

**3. Start Celery using this project**

    celery -A (PROJECTS_NAME) worker --loglevel=info


**4. Demonizing Celery**

[http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/](http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/)


> **See more (First steps):** [http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html)
> **See more (Celery for Django):** [http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)


Install Redis
---

**1. Install _redis-server_ outside the virtual environment**

- Ubuntu:

    ```
    sudo apt-get install redis-server
    ```

- Mac OS X:

    ```
    brew install redis
    ```

**2. Start _redis-server_**

    ```
    redis-server
    ```

**3. Test if it is working**

After the command, _redis_ should respond with `PONG`:

```
redis-cli ping
```

> Check log permissions: `sudo chmod 777 /var/log/redis/redis-server.log`

**4. Edit Redis config**

**5. Restart Redis**

    sudo service redis-server restart

> **See more (Redis in Django): ** [https://realpython.com/blog/python/caching-in-django-with-redis/](https://realpython.com/blog/python/caching-in-django-with-redis/)
> **See more (Setting up): **  [http://michal.karzynski.pl/blog/2013/07/14/using-redis-as-django-session-store-and-cache-backend/](http://michal.karzynski.pl/blog/2013/07/14/using-redis-as-django-session-store-and-cache-backend/)


Nginx Gzip compression
---

Edit `/etc/nginx/nginx.conf` (on Ubuntu):

```
. . .
##
# `gzip` Settings
#
#
gzip on;
gzip_disable "msie6";

gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_buffers 16 8k;
gzip_http_version 1.1;
gzip_min_length 256;
gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/vnd.ms-fontobject application/x-font-ttf font/opentype image/svg+xml image/x-icon;
. . .
```

and save and restart nginx:

    sudo service nginx restart

> **See more: ** [https://www.digitalocean.com/community/tutorials/how-to-add-the-gzip-module-to-nginx-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-add-the-gzip-module-to-nginx-on-ubuntu-14-04)


Let's encrypt
---

1. Install _Certbot_
2. Prepare _Nginx_
    1. Disable _letsencrypt_ paths from _Nginx_ config file
3. Get certificate
    ```
    sudo certbot --nginx -d domain.com -d www.domain.com
    ```
4. Updating Diffie-Hellman Parameters
    ```
    sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
    ```
5. Setting Up Auto Renewal (crontab)

> **See more: ** [https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04)


Set up firewall on Ubuntu (optional)
---

> **See more:** [https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04)
