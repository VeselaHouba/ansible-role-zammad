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
    assert 'zammad-test_grafana_1' in c.stdout
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


def test_config_present(host):
    f = host.file("/etc/nginx/sites-enabled/your_fqdn.conf")
    assert f.exists
    assert f.contains("snakeoil")
    assert f.contains("grafana")


def test_curl(host):
    c = host.run("curl -k -H Host:your_fqdn https://localhost")
    assert c.rc == 0
    assert '<title>Zammad Helpdesk</title>' in c.stdout


def test_grafana_config_presence(host):
    f = host.file("/opt/docker/zammad-test/grafana")
    assert f.exists


def test_backup_script(host):
    testfile = "/opt/docker/backup_zammad-test.sh"
    f = host.file(testfile)
    c = host.run(testfile)
    assert f.exists
    assert '/opt/docker/zammad-test_backup_full_' in c.stdout
    assert c.rc == 0


def test_custom_settings_env_file(host):
    zammad_env = host.file("/opt/docker/zammad-test/.env")
    assert zammad_env.contains('POSTGRES_USER=zammad')
    assert zammad_env.contains('POSTGRES_PASS=zammad')


def test_custom_settings_not_in_compose(host):
    compose = host.file("/opt/docker/zammad-test/docker-compose.override.yml")
    assert not compose.contains('HOLD_DAYS=')
    assert not compose.contains('NO_FILE_BACKUP=')
