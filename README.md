# allthevaccines

Human vaccine tracker.

## Contributing

Feel free to open a PR on [GitHub](https://github.com/sirodoht/allthevaccines)
or send an email patch to
[~sirodoht/public-inbox@lists.sr.ht](mailto:~sirodoht/public-inbox@lists.sr.ht).

On how to contribute using email patches see
[git-send-email.io](https://git-send-email.io/).

## Development

This is a [Django](https://www.djangoproject.com/) codebase. Check out the
[Django docs](https://docs.djangoproject.com/) for general technical
documentation.

### Structure

The Django project is `allthevaccines`. There is one Django app, `main`, with
all business logic. Application CLI commands are generally divided into two
categories, those under `python manage.py` and those under `make`.

```
├── [Makefile](./Makefile)
├── [allthevaccines/](allthevaccines)  # django project directory
│   ├── [asgi.py](asgi.py)
│   ├── [settings.py](settings.py)  # django settings
│   ├── [urls.py](urls.py)  # root urls module
│   └── [wsgi.py](wsgi.py)
├── [allthevaccines.org.conf](allthevaccines.org.conf)  # nginx configuration
├── [default.nix](default.nix)  # nix environment
├── [deploy.sh](deploy.sh)  # deployment script
├── [emperor.ini](emperor.ini)  # uwsgi emperor config
├── [emperor.uwsgi.service](emperor.uwsgi.service)  # uwsgi systemd config
├── [main/](main)  # django main app directory
│   ├── [admin.py](admin.py)
│   ├── [apps.py](apps.py)
│   ├── [migrations/](migrations)
│   ├── [models.py](models.py)  # all database models
│   ├── [static/](static/)
│   │   └── [style.css](style.css)  # CSS stylesheet — there is only this one
│   ├── [templates/](templates)  # django templates
│   │   └── [main/](main)
│   │       ├── [about.html](about.html)  # static about page
│   │       ├── [disease_detail.html](disease_detail.html)
│   │       ├── [disease_list.html](disease_list.html)
│   │       ├── [index.html](index.html)  # aka vaccine list template
│   │       ├── [layout.html](layout.html)  # all templates inherit this one
│   │       └── [vaccine_detail.html](vaccine_detail.html)
│   ├── [tests.py](tests.py)
│   ├── [urls.py](urls.py)
│   └── [views.py](views.py)
├── [manage.py](manage.py)
├── [requirements.in](requirements.in)  # manually edited requirements file
├── [requirements.txt](requirements.txt)  # pip-compile generated file
├── [requirements_dev.txt](requirements_dev.txt)  # manually edited dev requiremenets
├── [static/](static)  # generated static directory
└── [uwsgi.ini](uwsgi.ini)  # uwsgi vassal configuration
```

### Environment

This project uses [Nix](https://nixos.org/guides/install-nix.html) and
[direnv](https://direnv.net/) to configure its environment.

Alternatively, one can just use a [venv](https://docs.python.org/3/library/venv.html):

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_dev.txt
```

[direnv](https://direnv.net/) operates with a file named `.envrc` in the root
directory of the project. This file is git-ignored and an example of how it
is structured can be found in [`.envrc.example`](.envrc.example).

One needs to either `cp .envrc.example .envrc` if using direnv, or export the
environment variables in some other way.

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
