FROM ubuntu:18.04

# set a working directory for the app
WORKDIR /usr/src/app

# copy files to the container
ADD source_code/ /usr/src/app
ADD source_code/bookfinder /etc/nginx/sites-available/bookfinder
ADD source_code/uwsgi /etc/init.d/uwsgi


# install python3
RUN apt-get -yqq update
RUN apt-get -yqq install nginx python3 python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

# remove default file and make our site available
RUN rm -rf /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/bookfinder /etc/nginx/sites-enabled/bookfinder

ADD source_code/ /var/www
RUN chown -R www-data:www-data /var/www

# install dependencies
RUN python3 -m pip install -r requirements.txt

# define the port numbers the container should expose
EXPOSE 80:80
EXPOSE 443:443

#start nginx service
RUN service nginx start
RUN chmod 755 /etc/init.d/uwsgi
RUN service uwsgi start

# run the web app as a daemon
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]