# Go Out Safe - Nginx Orchestrator

## Introduction

When the orchestrator of API Gateway detects
that the system has to scale up, it should
inform nginx that another instance has been
added and the traffic should be sent also to the new instance.

Usually this is done by Nginx-Plus, but a business
license is required.

## Our solution

To fix this problem
we have created this docker image that listens
the events from docker and dynamically updates the nginx
upstream server list, by parsing a configuration template
with Jinja2.

## Run configuration

To run this application, you need to mount
the docker process sock file, using the argument:

`-v /var/run/docker.sock:/var/run/docker.sock`

For example:

`docker run -v /var/run/docker.sock:/var/run/docker.sock <image-name>`


## Testing the scaling

***! ! ! WARNING ! ! !***

The only service that can scale is the Application Gateway,
(WSGI with Gunicorn). In fact, the docker-compose.yml
configuration does not allow to replicate nginx and nginx-orchestrator.

If you want to test the auto-configuration you can scale up and down
the instances with this command:

`docker-compose scale api_gateway=<desidered-number-of-instances>`

## Microsoft Windows Problem <small>(Linux is better, always)</small>

To run correctly the nginx-orchestrator it need to access
to docker daemon sock file. Hence, if you use Windows you have to
fix the docker-compose.yml file.

Inside the nginx-orchestrator context you can find the volume list
that should be changed, using Winzozz path.

