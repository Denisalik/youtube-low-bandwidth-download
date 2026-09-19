# Low-Bandwidth youtube downloader web application
## Installation
On the host create folders for volumes and add permissions for volume
```sh
mkdir data
cd data
mkdir files
mkdir sql
mkdir secrets
cd secrets
mkdir certbot
mkdir letsencrypt
cd ../..
sudo chown -R 1000:1000 ./data/files
sudo chmod -R 755 ./data/files
```
Create password for basic auth.
```sh
echo "your-secret-password" > ./admin_password.txt
```
Build containers and run them
```sh
docker compose build
docker compose up
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
