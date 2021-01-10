FROM python:3

# copy files to the container
ADD source_code/ /usr/src/app

# set a working directory for the app
WORKDIR /usr/src/app

# install dependencies
RUN pip install --no-cache-dir flask
RUN pip install --no-cache-dir pymongo

# define the port number the container should expose
EXPOSE 5000

# run the web app
CMD ["python3", "./webify.py"]