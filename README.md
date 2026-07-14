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

### First authorization data

For each branded vaccine product, `first_authorized_year` records the earliest
documented regulatory authorization found anywhere in the world.
`first_authorized_region` identifies the authorizing country or region, and
`first_authorization_source_url` links directly to the evidence for that year.

- Record the authorization of the exact branded product, not its underlying
  vaccine technology or an earlier related formulation.
- Treat renamed aliases as one product and use the earliest authorization for
  that product.
- Do not substitute a WHO prequalification date for an authorization date.
- Count emergency, conditional, temporary, special-access, and restricted-use
  authorizations when they legally allowed the named product to be used.
- Do not count a WHO EUL/prequalification decision or an EMA scientific opinion
  as a national or regional authorization by itself.
- Prefer regulator records and approval letters, followed by official product
  documents, manufacturer announcements, and peer-reviewed historical sources.
- Leave all three fields empty when the year cannot yet be supported by a
  reliable source.

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
