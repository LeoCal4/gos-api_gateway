import os
import sys
import signal
import logging

import docker
import jinja2 as jin

# constants
APIGW_CONF_TEMPLATE = 'api_gateway.conf.tpl'

# reading the environments variables
NGINX_CONF_URI = os.getenv('NGINX_CONF_URI', '/etc/nginx/conf.d/api_gateway.conf')
NGINX_LABEL = os.getenv('NGINX_LABEL', default='gooutsafe.nginx_lb')
WORKER_LABEL = os.getenv('WORKER_LABEL', default='gooutsafe.api_gateway_worker')
WORKER_PORT = os.getenv('WORKER_PORT', default=5000)
LOG_LEVEL = os.getenv('NGINX_ORCHESTRATOR_LOG_LEVEL', 'INFO')

# logging
logger = logging.getLogger('Nginx Orchestrator')
logger.setLevel(LOG_LEVEL.upper())
handler = logging.StreamHandler(sys.stdout)
handler.setLevel((LOG_LEVEL.upper()))
handler.setFormatter(logging.Formatter('%(asctime)s - Go Out Safe - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Jinja engine
template_loader = jin.FileSystemLoader(searchpath='./templates')
template_env = jin.Environment(loader=template_loader)


def signal_handler(_signo, _stack_frame):
    """
    Signal handler for orchestrator.

    :param _signo: signal number
    :param _stack_frame: current stack grame
    :return: None
    """
    logger.info('Received a signal %s, stopping orchestrator...' % signal.Signals(_signo).name)
    sys.exit(0)


def reload_nginx(client, api_gateways):
    """
    It sends a SIGUP signal to all containers marked with label nginx_label
    :param client: docker client
    :param api_gateways: the list of web servers
    :return: None
    """
    web_server_ips = []

    for container in api_gateways.values():
        container_networks = container.attrs['NetworkSettings']['Networks']
        for network in container_networks.values():
            web_server_ips.append(network['IPAddress'])
            logger.debug('IP Address of worker is %s' % network['IPAddress'])

    render_template(web_server_ips)

    nginx_containers = client.containers.list(filters={'label': NGINX_LABEL, 'status': 'running'})
    for container in nginx_containers:
        logger.debug('Sending SIGHUP signal to container %s' % container)
        container.kill(signal='SIGHUP')


def render_template(ips):
    """
    This function renders the template of nginx configuration file and write it to mounted volume.
    :param ips: a list of api gateways ips
    :return: None
    """
    logger.debug('Rendering the template file for nginx...')
    template = template_env.get_template(APIGW_CONF_TEMPLATE)

    # creating main dict and parsing the template
    context = {
        'upstreams': [
            dict(ip=ip, port=WORKER_PORT) for ip in ips
        ]
    }
    parsed_template = template.render(context)

    # writing config file
    with open(NGINX_CONF_URI, 'w') as fp:
        fp.write(parsed_template)

    logger.debug('New configuration file are now available to nginx!')

    # done!


def get_currently_running_web_servers(client):
    web_containers = client.containers.list(filters={'label': WORKER_LABEL, 'status': 'running'})
    return dict([(c.id, c) for c in web_containers])


def update_already_running_containers(client):
    web_servers = get_currently_running_web_servers(client)
    if web_servers:
        reload_nginx(client, web_servers)
    return web_servers


def listen_for_events(client, web_servers):
    event_filters = {'type': 'container', 'label': WORKER_LABEL}
    for event in client.events(filters=event_filters, decode=True):
        if event['status'] == 'start':
            web_servers[event['id']] = client.containers.get(event['id'])
        elif event['status'] == 'stop':
            del web_servers[event['id']]
        else:
            continue
        logger.info("Detected container {} with {} status".format(event['id'], event['status']))
        reload_nginx(client, web_servers)


def main():
    client = docker.from_env()
    web_servers = update_already_running_containers(client)
    logger.info('Orchestrator started...')
    listen_for_events(client, web_servers)
    logger.info('Orchestrator stopped')


if __name__ == '__main__':
    # registering the signal handler for sigterm
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    main()
