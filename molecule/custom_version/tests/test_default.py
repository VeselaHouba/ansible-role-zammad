import os

import testinfra.utils.ansible_runner

import yaml

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_docker_is_running(host):
    cmd = host.service('docker')
    assert cmd.is_running
    assert cmd.is_enabled


def test_services_running(host):
    c = host.run('docker ps')
    assert 'zammad-test_zammad-backup_1' in c.stdout
    assert 'zammad-test_zammad-elasticsearch_1' in c.stdout
    assert 'zammad-test_zammad-memcached_1' in c.stdout
    assert 'zammad-test_zammad-nginx_1' in c.stdout
    assert 'zammad-test_zammad-postgresql_1' in c.stdout
    assert 'zammad-test_zammad-railsserver_1' in c.stdout
    assert 'zammad-test_zammad-scheduler_1' in c.stdout
    assert 'zammad-test_zammad-websocket_1' in c.stdout
    assert 'zammad-test_zammad-redis_1' in c.stdout
    assert c.rc == 0


def test_custom_version_running(host):
    stream = host.file('/tmp/ansible-vars.yml').content
    ansible_vars = yaml.load(stream, Loader=yaml.FullLoader)
    version = ansible_vars['zammad_instances'][0]['zammad_version']
    c = host.run('docker ps')
    assert 'zammad/zammad-docker-compose:zammad-' + version in c.stdout
    assert c.rc == 0


def test_curl(host):
    c = host.run("curl -k -H Host:your_fqdn https://localhost")
    assert c.rc == 0
    assert '<title>Zammad Helpdesk</title>' in c.stdout


def test_custom_settings_in_compose(host):
    stream = host.file('/tmp/ansible-vars.yml').content
    ansible_vars = yaml.load(stream, Loader=yaml.FullLoader)
    hold_days = ansible_vars['zammad_instances'][0]['zammad_backup_hold_days']
    compose = host.file("/opt/docker/zammad-test/docker-compose.override.yml")
    assert compose.contains('HOLD_DAYS=' + str(hold_days))
