Dependencies:
 - Python 3.8
 - Vagrant v2.2.6

Project setup errors:
 - No/invalid vagrant provider
	run `vagrant up --provider=PROVIDER` where PROVIDER is either virtualbox (windows) or parallels (macOS)
	https://stackoverflow.com/questions/21840883/specify-default-provider-in-vagrantfile
 - Installing Python3.8
	point `python3` to python3.8
		https://tech.serhatteker.com/post/2019-12/upgrade-python38-on-ubuntu/
	install python3.8
		https://tech.serhatteker.com/post/2019-12/how-to-install-python38-on-ubuntu/
 - Python pip3 is not installed
	run `sudo apt install python3-pip
 - pip install error: locale.Error: unsupported locale setting
	run `export LC_ALL=C`
	https://stackoverflow.com/questions/36394101/pip-install-locale-error-unsupported-locale-setting
 - ImportError: cannot import name 'sysconfig' from 'distutils' with python3/pip3
	
 - Error: pg_config executable not found
	run `sudo apt install libpq-dev` in vagrant
	https://stackoverflow.com/questions/11618898/pg-config-executable-not-found
 - Node Version Manager (nvm) is not installed
	run `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash` in vagrant, then restart your terminal session by exiting vagrant and logging in again
	https://ostechnix.com/install-node-js-linux/
 - Node or Node Package Manager (npm) is not installed
	run `nvm install node` in vagrant

ToDo:
 - Pick project name and update `name` and `description` fields in package.json
 - Add other team members to admins list in base.py
 - create an email acct for the program after we pick a project name, set SERVER_EMAIL in production.py