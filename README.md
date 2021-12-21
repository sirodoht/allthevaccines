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
