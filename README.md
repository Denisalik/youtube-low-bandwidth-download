# Low-Bandwidth youtube downloader web application
Simple Web application that downloads youtube videos and shares with client them.
## Installation
On the host create folders for volumes and add permissions for volume
```sh
mkdir data && cd data && mkdir files && mkdir sql && mkdir secrets && cd secrets && mkdir certbot && mkdir letsencrypt && cd ../..
sudo chown -R 1000:1000 ./data/files
sudo chmod -R 755 ./data/files
```
Create password for basic auth.
```sh
echo "your-secret-password" > ./admin_password.txt
```
Build containers and run them(you need to have docker buildx)
```sh
docker compose build
docker compose up
```
Or if you want to change secrets(admin_password.txt)
```sh
docker compose build --no-cache
```
If you need to have delete all sql+fiels
```sh
rm ./data/sql/database.db
rm ./data/files/*
```
## HTML minifier installation
Frontend uses this long time compiling image. For convenience it pushed into docker hub and frontend dockerfile uses image from docker hub. But if you need to recompile it.
```sh
cd frontend
docker build -f Dockerfile.base -t denisalik/rust-html-minifier-builder:1.88-alpine -t denisalik/rust-html-minifier-builder:latest .
docker login
docker push denisalik/rust-html-minifier-builder:1.88-alpine
docker push denisalik/rust-html-minifier-builder:latest
```
## HTTPS certificates:
```sh
docker compose up -d --build
docker compose run --rm certbot certonly --webroot -w /var/www/certbot -d yout-low-bandwidth-download-app.duckdns.org -d www.yout-low-bandwidth-download-app.duckdns.org --agree-tos -m <your-mail@mail_domain.extension> --no-eff-email
```
Add cron certificate renewal:
```sh
crontab -e
#pass this(everyday at 3:00)
0 3 * * * cd ~/youtube-low-bandwidth-download && docker compose run --rm certbot renew --webroot -w /var/www/certbot --quiet && docker compose exec frontend nginx -s reload
#check if working
crontab -l                              # list your current entries
sudo grep CRON /var/log/syslog
```

## Result
Check deployed version on [deployed site](https://yout-low-bandwidth-download-app.duckdns.org)
## Features
* Frontend doesn't use any css/js/frameworks ~1500 bytes(~3800->~1470 gzipped)
* Frontend html is minified using rust-based minifier(minify-html)
* For downloading files it uses native browser without fetch blob.
* Nginx serves directly from ./data/files
* Nginx have configured for low bandwidth with full resume support and long timeout
* Nginx using http2, without ssl
* Backend uses a low-weight video format, ideally audio, to download files.
* Backend track state of the download
* Storing information about database of files backend uses sqlite3
* Cron every day to delete files at 4:00 and 3:00 to delete rows that were deleted previously at 4:00.
## TODO
* linter for python
* make auth -> get request, non limit-except
* add test containers instead of shell simple script
## Test
Integration test for running backend container and checking if scheduler works.

1 Test runs ~2 minutes with sleeps, it downloads file with id=1, so if you want to download specific file you need to clean volumes first.

2 Test runs ~30 seconds with sleeps, it create row with state:deleted, which should be deleted by scheduler and shows get all files, which shouldn't include created file

Example:
```sh
sh test/file-scheduler.integration-test.sh 15 24
sh test/db-scheduler.integration-test.sh 13 24
```
15 24 is time when scheduler should deleted files.

13 24 is time when scheduler should delete rows.