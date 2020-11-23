# Docker image

This project has the possibility to be built as
docker image.
To build the image you can launch the command

`docker build . -t gotf`

## docker-compose

If you want to run the entire project using
separate containers and using the production environment you have to:
 
- Check configuration file, that is named `env_file`. It contains
the project variables.

- Run the command `docker-compose up -d`

- Now you should see all services running and the application frontend
available at 127.0.0.1:5000 
