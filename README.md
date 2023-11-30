# allthevaccines

Human vaccine tracker.

## Development

This is a [Django](https://www.djangoproject.com/) codebase. Check out the
[Django docs](https://docs.djangoproject.com/) for general technical
documentation.

### Structure

The Django project is `allthevaccines`. There is one Django app, `main`, with
all business logic. Application CLI commands are generally divided into two
categories, those under `python manage.py` and those under `make`.

```
├── Makefile
├── allthevaccines/  # django project directory
│   ├── asgi.py
│   ├── settings.py  # django settings
│   ├── urls.py  # root urls module
│   └── wsgi.py
├── allthevaccines.org.conf  # nginx configuration
├── default.nix  # nix environment
├── deploy.sh  # deployment script
├── emperor.ini  # uwsgi emperor config
├── emperor.uwsgi.service  # uwsgi systemd config
├── main/  # django main app directory
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py  # all database models
│   ├── static/
│   │   └── style.css  # CSS stylesheet — there is only this one
│   ├── templates/  # django templates
│   │   └── main/
│   │       ├── about.html  # static about page
│   │       ├── disease_detail.html
│   │       ├── disease_list.html
│   │       ├── index.html  # aka vaccine list template
│   │       ├── layout.html  # all templates inherit this one
│   │       └── vaccine_detail.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.in  # manually edited requirements file
├── requirements.txt  # pip-compile generated file
├── requirements_dev.txt  # manually edited dev requiremenets
├── static/  # generated static directory
└── uwsgi.ini  # uwsgi vassal configuration
```

### Set up

```sh
cp .envrc.example .envrc

# add SMPT credentials (optional) in .envrc
vim .envrc

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Database

This project uses SQLite. To create the database and schema and apply
migrations, run:

```sh
python manage.py migrate
```

### Data

Production vaccine and disease data are serialised and committed to the
repository, file name is [`vaccine-disease-data.json`](vaccine-disease-data.json).

To load all vaccine and disease data, run:

```sh
python manage.py loaddata --app main vaccine-disease-data.json
```

Note: The above command needs to run after the migration command.

To dump/serialise all vaccine and disease data, run:

```sh
python manage.py dumpdata main.Vaccine main.Disease > vaccine-disease-data.json
```

### Serve

To run the Django development server:

```sh
python manage.py runserver
```

## Testing

Using the Django test runner:

```sh
python manage.py test
```

For coverage, run:

```sh
make cov
```

## Code linting & formatting

The following tools are used for code linting and formatting:

* [black](https://github.com/psf/black) for code formatting.
* [isort](https://github.com/pycqa/isort) for imports order consistency.
* [flake8](https://gitlab.com/pycqa/flake8) for code linting.

To use:

```sh
make format
make lint
```

## Deployment

Deployment is configured with nginx as a reverse proxy and uWSGI in
[Emperor mode](https://uwsgi.readthedocs.io/en/latest/Emperor.html).
Configuration files:

* [`allthevaccines.org.conf`](allthevaccines.org.conf): nginx reverse proxy configuration
* [`emperor.ini`](emperor.ini): uWSGI main configuration, enables emperor mode
* [`uwsgi.ini`](uwsgi.ini): uWSGI vassal configuration

Also, uWSGI can be configured as a
[systemd service](https://uwsgi.readthedocs.io/en/latest/Systemd.html).
See [`emperor.uwsgi.service`](emperor.uwsgi.service). To follow logs, run:

```sh
journalctl -u emperor.uwsgi.service -fb
```

## License

This software is licensed under the MIT license. For more information, read the
[LICENSE](LICENSE) file.
