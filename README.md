[![License: MIT](https://img.shields.io/github/license/vintasoftware/django-react-boilerplate.svg)](LICENSE.txt)

# Aggie Intelligent Schedule Builder - CSCE 482

## A quick note
Most of the readme past this point came from the [boilerplate project](https://github.com/vintasoftware/django-react-boilerplate) repo, however some adjustments have been made. Namely, the Django application was refactored to function as a RESTful API with Webpack serving the React application completely separate from the backend application. Multiple adjustments were also made to the Webpack configuration. Therefore, take everything from the 'About' section and below with a grain of salt, as some things may no longer be accurate. A section dedicated to solving potential issues during the initial setup phase ([Troubleshooting](#troubleshooting)) as well as the basic provisioning process ([Initializing the Development Environment](#initializing-the-development-environment)) has also been added for convenience.

## About
All issue tracking and task management for this project is done through Jira

A [Django](https://www.djangoproject.com/) project with lots of state of the art libraries and tools like:
- [React](https://facebook.github.io/react/), for building interactive UIs
- [django-js-reverse](https://github.com/ierror/django-js-reverse), for generating URLs on JS (not used)
- [Bootstrap 4](https://v4-alpha.getbootstrap.com/), for responsive styling
- [Webpack](https://webpack.js.org/), for bundling static assets
- [Celery](http://www.celeryproject.org/), for background worker tasks
- [WhiteNoise](http://whitenoise.evans.io/en/stable/) with [brotlipy](https://github.com/python-hyper/brotlipy), for efficient static files serving (not used)
- [prospector](https://prospector.landscape.io/en/master/) and [ESLint](https://eslint.org/) with [pre-commit](http://pre-commit.com/) for automated quality assurance (does not replace proper testing!)

For continuous integration, a [CircleCI](https://circleci.com/) configuration `.circleci/config.yml` is included, but currently not used.

Also, includes a Heroku `app.json` and a working Django `production.py` settings, enabling easy deployments with ['Deploy to Heroku' button](https://devcenter.heroku.com/articles/heroku-button). Those Heroku plugins are included in `app.json`:
- PostgreSQL, for DB
- Redis, for Celery
- Sendgrid, for e-mail sending
- Papertrail, for logs and platform errors alerts (must set them manually)

## Initializing the Development Environment
The following steps should be taken in the event you must provision your Vagrant machine by hand
- Install Vagrant version 2.2.6
- Inside the project directory (where your `Vagrantfile` is located), run `vagrant up` in the terminal
- SSH into vagrant
- run `sudo apt install libsqlite3-dev`
- install python 2.7 from source (needed for npm install) [Guide](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/)
- run `sudo ln -s /usr/src/Python-2.7.18/python python2`

*Installing Python 3.8 (optional): Django can run with python 3.6, which comes with Ubuntu 18.04 LTS, so you do not need to install python 3.8 unless you encounter issues.*
- install python 3.8 from source, run `sudo make install` instead of `sudo make altinstall` - [Guide](https://tech.serhatteker.com/post/2019-12/how-to-install-python38-on-ubuntu/)

*Please note: the following two commands will replace the link to python 3.6 with a link to python 3.8. This will result in the `python3` command using v3.8 instead of v3.6. This may result in an unpleasant side-effect where Ubuntu does not process certain commands that rely on python properly. Alternatively, you can avoid this by typing `python3.8` from here on every time you need to run python*
- run `sudo rm /usr/bin/python3`
- run `sudo ln -s python3.8 /usr/bin/python3`
- run `cd /usr/bin/`
The following command will create a link used by the terminal for the command `python` that points to python 3.8
- run `sudo ln -fs ~/tmp/Python-3.8.1/python python`
- run `sudo apt install libpq-dev`
Install Node Version Manager (nvm) and Node.js:
- run `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash`
- exit vagrant with `exit` and restart session with `vagrant ssh` to refresh shell
- verify ubuntu uses python 3.8 by default by running `python3 --version`
output should be "Python 3.8.1"
- run `pip3 install django --user`
- If on Linux:
  - run `nvm install node` 
- If on Windows, run all the following:
  - `nvm install stable`
  - `nvm alias default stable`
  - `nvm list` and make sure the arrow is pointing to the latest version
  - `npm -g install npm@latest`
  - `sudo rm /usr/bin/node`
  - `sudo ln -s /home/vagrant/.nvm/versions/node/v14.13.0/bin/node /usr/bin/node`
  - `npm config set bin-links false`

## Troubleshooting
Below are some common issues you may run into with your development environment when doing first-time set up
- No/invalid vagrant provider
	run `vagrant up --provider=PROVIDER` where PROVIDER is either virtualbox (windows) or parallels (macOS)
	[Guide](https://stackoverflow.com/questions/21840883/specify-default-provider-in-vagrantfile)
 - Installing Python3.8
	point `python3` to python3.8
	[Guide](https://tech.serhatteker.com/post/2019-12/upgrade-python38-on-ubuntu/)
	install python3.8
	[Guide](https://tech.serhatteker.com/post/2019-12/how-to-install-python38-on-ubuntu/)
 - Python pip3 is not installed
	run `sudo apt install python3-pip`
 - pip install error: locale.Error: unsupported locale setting
	run `export LC_ALL=C`
	[Guide](https://stackoverflow.com/questions/36394101/pip-install-locale-error-unsupported-locale-setting)
 - ImportError: cannot import name 'sysconfig' from 'distutils' with python3/pip3
	run `sudo apt install python3-distutils`
 - Error: pg_config executable not found
	run `sudo apt install libpq-dev` in vagrant
	[Guide](https://stackoverflow.com/questions/11618898/pg-config-executable-not-found)
 - Node Version Manager (nvm) is not installed
	run `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash` in vagrant, then restart your terminal session by exiting vagrant and logging in again
	[Guide](https://ostechnix.com/install-node-js-linux/)
 - Node or Node Package Manager (npm) is not installed
	run `nvm install node` in vagrant
 - ERROR in /frontend/.../style.scss: Module build failed
	try rebuilding sass with `npm rebuild node-sass` 


## Running
*All commands should be run inside vagrant. Use `vagrant ssh` and navigate to the project directory*
*Note: some commands specify they should be ran with `python` but you may need to run them with `python3`*
### Setup
- Make sure you have created a python virtual environment: In vagrant `~/csce482/csce482/` run `python3 -m venv csce482-venv`
  - If on Windows: use `sudo apt install virtualenv` and then `virtualenv csce482-venv --always-copy` instead.
- Run `source csce482-venv/bin/activate` to activate your virtual environment (necessary for python to recognize certain packages)
- Inside the `backend` folder, do the following:
- Create a copy of ``csce482/settings/local.py.example``:  
  `cp csce482/settings/local.py.example csce482/settings/local.py`
- Create a copy of ``.env.example``:
  `cp .env.example .env`

#### Creating migrations
- Go to the project's directory.
- For Linux machines:
  - `pip3 install -r requirements.txt && pip3 install -r dev-requirements.txt`
- For Windows machines:
  - `sudo python3 -m pip install -r requirements.txt`
  - `sudo python3 -m pip install -r dev-requirements.txt`
  - (In general, use `sudo python3 -m pip install <THINGTOINSTALL>` for any pip installs if you're on Windows.
- Then run:`npm install`
- Create the migrations by running the following:
  `python3 manage.py makemigrations`
- Run the migrations:
  `python3 manage.py migrate`

### Tools
- Setup [editorconfig](http://editorconfig.org/), [prospector](https://prospector.landscape.io/en/master/) and [ESLint](http://eslint.org/) in the text editor you will use to develop.

### Running the project
- Open a command line window and go to the project's directory.
- `pip3 install -r requirements.txt && pip3 install -r dev-requirements.txt`
- `npm install`
- If on windows: Open `package.json` in your preferred text editor, look under `"scripts":` and change `"start": babel-node server.js",` to `"start": ./node_modules/@babel/node/bin/babel-node.js server.js",`
- Now you can start node with: `npm run start`
- Open another command line window.
- `source csce482-venv/bin/activate` to activate the virtual environment.
- Go to the `backend` directory and run the following to start django.
- `python3 manage.py runserver`

### PostgreSQL set-up
- Note: For the back-end code to run correctly, make sure you use the same names, passwords, emails, etc. shown here. These will be the ones we use for the set-up on the remote server once we move from local.
- Run `sudo apt install postgresql`
- Login into the PostgreSQL shell: `sudo -u postgres psql`
- You can use `\du` to check the list of users.
- We're gonna change the root user password: `ALTER USER postgres PASSWORD 'Watermelon482';`
- Use `\q` to exit the shell
- You can now reenter the shell whenever you want by using `psql -U postgres -h localhost`
- reenter the shell
- Use `\l` to see the list of databases
- If it doesn't exist, enter `CREATE DATABASE aggieisb_db;`
- Exit the shell and update your migrations with `sudo python3 manage.py makemigrations`
- Apply the new migrations with `sudo python3 manage.py migrate`
- You will need to update migrations like this whenever you make or pull changes to Django settings or models.
- Go to `csce482/backend` and run `sudo python3 manage.py shell < api/testdata.py` to fill the database with test data.

### Django DB Admin and API Endpoints in the Browser
- Run the server with `sudo python3 manage.py runserver 0:8000`
- Visit `localhost:8080\admin` in your browser (Vagrant forwards port 8000 to 8080 on your actual machine)
- Login with aggieisb@gmail.com, password is Watermelon482.
- You can view instances of different models and manage them through this directory.
- Visit `localhost:8080\api` next.
- Here you will find links to instance lists for each model.
- You can focus on a specific instances by append `\<id>`, where `\<id>` is the id of the instance you want to focus on, to the end of the directory of a specific list.
  -Example: `localhost:8080\api\activities\3` routes to the instance of the Activity model with an id of 3.
- These `\api` directories are endpoints for the data. If you're having trouble with a GET or POST, make sure you can visit the endpoint in your browser. If not, you're probably not using the correct endpoint url.

#### Celery
- Open a command line window and go to the project's directory
- `source csce482-venv/bin/activate` to activate your virtualenv.
- `python3 manage.py celery`

### Testing
`make test`

Will run django tests using `--keepdb` and `--parallel`. You may pass a path to the desired test module in the make command. E.g.:

`make test someapp.tests.test_views`

### Adding new pypi libs
Add the libname to either requirements.in or dev-requirents.in, then either upgrade the libs with `make upgrade` or manually compile it and then,  install.
`pip-compile requirements.in > requirements.txt` or `make upgrade`
`pip install -r requirements.txt`

### Cleaning example code
Before you start creating your own apps remove the example:
- Run the command `make clean_examples` in order to clean up the example apps from the front and backend.
- Deregister the example app by removing `'exampleapp.apps.ExampleappConfig'` from ``backend/csce482/settings/base.py``.
- Adjust ``backend/csce482/urls.py`` to point to your newly created Django app and remove the path configuration that redirects to the deleted example app.

## Deployment
### Setup
This project comes with an `app.json` file, which can be used to create an app on Heroku from a GitHub repository.

After setting up the project, you can init a repository and push it on GitHub. If your repository is public, you can use the following button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

If you are in a private repository, access the following link replacing `$YOUR_REPOSITORY_LINK$` with your repository link.

- `https://heroku.com/deploy?template=$YOUR_REPOSITORY_LINK$`

Remember to fill the `ALLOWED_HOSTS` with the URL of your app, the default on heroku is `appname.herokuapp.com`. Replace `appname` with your heroku app name.

### Sentry

[Sentry](https://sentry.io) is already set up on the project. For production, add `SENTRY_DSN` environment variable on Heroku, with your Sentry DSN as the value.

You can test your Sentry configuration by deploying the boilerplate with the sample page and clicking on the corresponding button.

### Sentry source maps for JS files

The `bin/post_compile` script has a step to push Javascript source maps to Sentry, however some environment variables need to be set on Heroku.

You need to enable Heroku dyno metadata on your Heroku App. Use the following command on Heroku CLI:

- `heroku labs:enable runtime-dyno-metadata -a <app name>`

The environment variables that need to be set are:

- `SENTRY_ORG` - Name of the Sentry Organization that owns your Sentry Project.
- `SENTRY_PROJECT_NAME` - Name of the Sentry Project.
- `SENTRY_API_KEY` - Sentry API key that needs to be generated on Sentry. [You can find or create authentication tokens within Sentry](https://sentry.io/api/).

After enabling dyno metadata and setting the environment variables, your next Heroku Deploys will create a release on Sentry where the release name is the commit SHA, and it will push the source maps to it.

## Linting
- Manually with `prospector` and `npm run lint` on project root.
- During development with an editor compatible with prospector and ESLint.

## Pre-commit hooks
- Run `pre-commit install` to enable the hook into your git repo. The hook will run automatically for each commit.
- Run `git commit -m "Your message" -n` to skip the hook if you need.

## Opinionated Settings
Some settings defaults were decided based on Vinta's experiences. Here's the rationale behind them:

### `CELERY_ACKS_LATE = True`
We believe Celery tasks should be idempotent. So for us it's safe to set `CELERY_ACKS_LATE = True` to ensure tasks will be re-queued after a worker failure. Check Celery docs on ["Should I use retry or acks_late?"](https://docs.celeryproject.org/en/latest/faq.html#should-i-use-retry-or-acks-late) for more info.

[MIT License](LICENSE.txt)
