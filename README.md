# Zammad role role

Set of multiple roles used to deploy Zammad with docker-compose. It's possible to separate proxy and docker backend to individual servers.

It's designed as simple usage - Role will take care of installing docker, nginx, let'sencrypt (if enabled) and grafana with some pre-defined dashboards (if enabled)

## Usage

1. Setup your hosts file, decide which host to use as proxy and which as backend (can also be same host)
1. Setup hostvars according to following example

`letsencrypt_email` default e-mail when one is not defined on instance level.
`zammad_instances` is list containing multiple zammad definitions. Key-values in list:

### Mandatory variables

- `name: zammad-test` - Will be used as docker-compose project name
- `zammad_custom_port: 10080` - Docker listens on this port
- `zammad_fqdn: your_fqdn` - Used for Let'sEncrypt and nginx
- `zammad_backend_ip: 127.0.0.1` - nginx will forward requests here
- `proxy_server: your_proxy_host` - host where nginx will run. Must match host in inventory
- `docker_server: your_docker_host` - host where docker will run. Must match host in inventory

### Optional zammad variables
- `zammad_compose_version: 3` - Compose override version changed around Zammad version 5.
- `zammad_custom_image`: - You can override default Zammad image here.
- `zammad_elastic_memory: 2048m` - Memory limit for Elasticsearch
- `zammad_version: 4.1.0-6` - Will replace version in `.env` file
- `letsencrypt_email`: Contact e-mail used for Let'sEncrypt notifications
- `zammad_backup_hold_days: 10` - Number of days to keep backups.
- `zammad_postgress_user: zammad` - psql user
- `zammad_postgress_pass: zammad` - psql password

### Optional proxy & other variables
- `letsencrypt_deploy: true` - Do you wish to register let'sencrypt? Will work only when DNS is setup properly. Default `true`
- `custom_cert_path: PATH` - Path to certificate, if you don't want to use letsencrypt.
- `custom_key_path: PATH` - Path to certificate key, if you don't want to use letsencrypt.
- `grafana_port: 3000` - On which port should grafana listen. Implies enabling grafana deploy

### Minimal example
```YAML
zammad_instances:
  - name: zammad-assaabloy
    zammad_backend_ip: 127.0.0.1
    zammad_custom_port: 10080
    zammad_fqdn: your_fqdn
    proxy_server: your_proxy_host
    docker_server: your_docker_host
```

### Full example

```YAML
zammad_instances:
  - name: zammad-test
    zammad_backend_ip: 127.0.0.1
    zammad_compose_version: 3
    zammad_custom_image: veselahouba/zammad-docker-compose:zammad-legacy-ssl${VERSION}
    zammad_custom_port: 10080
    zammad_elastic_memory: 2048m
    zammad_fqdn: your_fqdn
    zammad_nginx_container_port: 8080
    zammad_version: 5.0.1-5
    proxy_server: your_proxy_host
    docker_server: your_docker_host
    letsencrypt_deploy: false
    custom_cert_path: /etc/ssl/certs/ssl-cert-snakeoil.pem
    custom_key_path: /etc/ssl/private/ssl-cert-snakeoil.key
    grafana_port: 3000
```

### Backups
Zammad takes backups of itself, but if you want to run one-shot backup of docker volumes including docker-compose config, there's small script deployed in `/opt/backup_<instance-name>.sh`

## Author Information

Jan Michalek
