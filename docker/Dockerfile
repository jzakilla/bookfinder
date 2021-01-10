FROM python:3

# set a working directory for the app
WORKDIR /usr/src/app

# copy files to the container
COPY ../libre_py/source_code/ .

# install dependencies
RUN pip install --no-cache-dir flask

# define the port number the container should expose
EXPOSE 5000

# run the web app
CMD ["python", "./webify.py"]