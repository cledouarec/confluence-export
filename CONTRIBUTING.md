# Contribution guidelines

First off, thank you for considering contributing to Confluence exporter.

If your contribution is not straightforward, please first discuss the change you
wish to make by creating a new issue before making the change.

## Reporting issues

Before reporting an issue on the
[issue tracker](https://github.com/cledouarec/confluence-export/issues),
please check that it has not already been reported by searching for some related
keywords.

## Pull requests

Try to do one pull request per change.

## Commit Message Format

*This specification is inspired by the [Angular commit message format](https://github.com/angular/angular/blob/main/contributing-docs/commit-message-guidelines.md).*

We have very precise rules over how our Git commit messages must be formatted.
This format leads to **easier to read commit history**.

The commit message must respect the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard.

To facilitate its usage, we use [commitizen](https://commitizen-tools.github.io/commitizen/).
The commit messages can be written interactively with :
```shell
uv run cz commit
```

Each commit message consists of a **header**, a **body**, and a **footer**.

```
<header>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The `header` is mandatory and must conform to the [Commit Message Header](#commit-message-header) format.

The `body` is preferred for all commits except for those of type "docs".

The `footer` is optional. The [Commit Message Footer](#commit-message-footer) format describes what the footer is used for and the structure it must have.

### Commit Message Header

```
<type>(<scope>): <short summary>
  │       │             │
  │       │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       │
  │       └─⫸ Commit Scope: cli|client|config|export
  │
  └─⫸ Commit Type: build|ci|docs|feat|fix|perf|refactor|test
```

The `<type>` and `<summary>` fields are mandatory, the `(<scope>)` field is optional.

#### Type

Must be one of the following:

* **build**: Changes that affect the build system or external dependencies (examples: pyproject.toml, uv.lock)
* **ci**: Changes to our CI configuration files and scripts (examples: GitHub Actions, Dependabot)
* **docs**: Documentation only changes
* **feat**: A new feature
* **fix**: A bug fix
* **perf**: A code change that improves performance
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **test**: Adding missing tests or correcting existing tests

### Commit Message Footer

The footer can contain information about breaking changes and is also the place
to reference GitHub issues and other pull requests that this commit closes or is
related to. For example:

```
BREAKING CHANGE: <breaking change summary>
<BLANK LINE>
<breaking change description + migration instructions>
<BLANK LINE>
<BLANK LINE>
Fixes #<issue number>
```

A breaking change can also be marked with a `!` after the type or the scope, for
example `feat(config)!: <short summary>`.

### Updating the changelog

There is no need to update the [CHANGELOG](CHANGELOG.md) file.

The changelog is updated automatically by the GitHub actions when the commits
are pushed on `main`. They also bump the version, create the release on GitHub
and publish the package on PyPI. The new version depends on the commit types :
* **feat**: minor version
* **fix**, **perf** and **refactor**: patch version
* breaking change: major version

The other types don't produce a new version.

## Developing

### Set up

The project is managed with [uv](https://docs.astral.sh/uv/). To install the
module, the main script and the extra tools in a virtual environment, simply
do :
```shell
uv sync
```
The Git hook checking the commit messages can be installed with :
```shell
uv run pre-commit install
```

### Linting and testing

The code can be linted and formatted at any time :
```shell
uv run ruff check
uv run ruff format
```
The unit tests can be run with :
```shell
uv run pytest
```
