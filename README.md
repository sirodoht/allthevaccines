# allthevaccines

Human vaccine tracker.

## Data

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

## Development

This is a standard [Django](https://docs.djangoproject.com/) application with
[uv](https://github.com/astral-sh/uv).

1. Create database tables with:

```sh
uv run manage.py migrate
```

2. Run development server with:

```sh
uv run manage.py runserver
```

## Format and lint

Run Python formatting with:

```sh
uv run ruff format
```

Run Python linting with:

```sh
uv run ruff check --fix
```

## Deploy

Every commit on branch `main` auto-deploys using GitHub Actions. To deploy manually:

```sh
cd ansible/
cp .envrc.example .envrc
uv run ansible-playbook playbook.yaml -v
```
## License

This software is licensed under the MIT license. For more information, read the
[LICENSE](LICENSE) file.
