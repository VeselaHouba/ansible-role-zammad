import os

import testinfra.utils.ansible_runner

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
    c = host.run('docker ps')
    assert 'zammad/zammad-docker-compose:zammad-4.1.0-6' in c.stdout
    assert c.rc == 0


def test_curl(host):
    c = host.run("curl -k -H Host:your_fqdn https://localhost")
    assert c.rc == 0
    assert '<title>Zammad Helpdesk</title>' in c.stdout
