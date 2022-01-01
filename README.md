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
├── main/  # django app directory
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── static/
│   │   └── style.css  # single CSS stylesheet
│   ├── templates/  # django templates
│   │   └── main/
│   │       ├── about.html  # static about page
│   │       ├── disease_detail.html
│   │       ├── disease_list.html
│   │       ├── index.html
│   │       ├── layout.html  # all templates inherit from this one
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

### Database

This project uses SQLite. To create the database and schema and apply
migrations, run:

```sh
python manage.py migrate
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

## License

This software is licensed under the MIT license. For more information, read the
[LICENSE](LICENSE) file.
