from fabric.api import cd, env, run

import os

env.name = 'pi'
env.localsrc = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
env.repo = 'git@github.com:aeikenberry/pi.git'
env.branch = 'master'
env.user = 'root'

env.hosts = ['192.168.1.145']
env.pi_dir = '/root/sites/Pi/'
env.pi_env = 'pyenv'
env.activate_env = '. %(pi_dir)s/%(pi_env)s/bin/activate'

def update_repo():
	"Pull the repo"
	with cd('%(pi_dir)ssrc'	 % env):
		run('git fetch')
		run('git checkout %(branch)s' % env)
		run('git reset --hard HEAD')
		run('git pull origin %(branch)s' % env)

def install():
	"install python requirements"
	run('%(activate_env)s && pip install -r %(pi_dir)s/src/requirements.txt' % env)

def update_config():
	"update the config files"
	run('rm -f /etc/nginx/nginx.conf \
			   /lib/systemd/system/gunicorn-app.service')
	run('ln -s %(pi_dir)s/src/config/nginx.conf /etc/nginx/nginx.conf' % env)
	run('ln -s %(pi_dir)s/src/config/gunicorn-app.service /lib/systemd/system/gunicorn-app.service' % env)
	
	run('systemctl stop nginx')
	run('systemctl reload nginx')
	run('systemctl start nginx')

	run('systemctl restart gunicorn-app')
