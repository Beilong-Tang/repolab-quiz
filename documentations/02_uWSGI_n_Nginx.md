# uWSGI_n_Nginx

Reference Documents:
https://uwsgi.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

## Basic Install
### Nginx (It is a web server.)
---
sudo apt install nginx # download and install
sudo /etc/init.d/nginx start # start nginx
---
**Inside the sso root directory**
---
nano deploy/sso_nginx.conf # editing text file
---
Change the part of the URL after *"server unix://"* and before *"sso/sso.sock"* to whatever directory the sso server is currently located.
Change server_name into whatever your *IP address* is (or maybe a fully qulified domian, if your machine have one).
Change the part of the URL after *"include "* and before *"sso/uwsgi_params"* to whatever directory the sso server is currently located.
**Inside the sso root directory**
---
cp deploy/sso_nginx.conf /etc/nginx/sites-available/ # copy file to desired place
sudo ln -s /etc/nginx/sites-available/sso_nginx.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx.service
---
Then, nginx will occupy and listen on port 80.
### SSO_Webserver (It is a web application.)
**Inside the sso/deploy directory**
---
./first_time.sh # executing this script installs environment
---

## Deployment
Note: **These procedure should be carried out after the Basic Install.**
**Inside the sso root directory**
---
nano deploy/sso_uWSGI.service
---
Change the part of the string after *"User="* to your username. You can look it up using:
---
whoami
---
Change the part of the string after *"ExecStart="* and before *"sso/deploy/uWSGI_startup.sh"* to whatever directory the sso server is currently loacated.
---
sudo cp deploy/sso_uWSGI.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start sso_uWSGI.service
sudo systemctl enable sso_uWSGI.service
---
Now the sso_webserver is deployed!

## Development
Note: **These procedure should be carried out after the Basic Install.**
To activate the Python environment of the sso_webserver,
**Inside the sso root directory**
---
source env/bin/activate
---
To deactivate the environment of activated environment,
---
deactivate
---
Finish!