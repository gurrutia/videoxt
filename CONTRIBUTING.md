# How to contribute to VideoXT

Thank you for considering contributing to VideoXT!

## Contents

- [How to contribute to VideoXT](#how-to-contribute-to-videoxt)
  - [Contents](#contents)
  - [Getting started](#getting-started)
  - [Start coding](#start-coding)
  - [Running the tests](#running-the-tests)
  - [Running test coverage](#running-test-coverage)
  - [Building the docs](#building-the-docs)
  - [What it is, is not and never will be](#what-it-is-is-not-and-never-will-be)

## Getting started

1. [Fork](https://github.com/gurrutia/videoxt/fork) VideoXT to your GitHub account.

2. Clone your fork locally, replacing `your-username` in the command below with your actual username.

    ```sh
    git clone https://github.com/your-username/videoxt
    cd videoxt
    ```

3. Create and activate a virtualenv.

    - Linux/macOS

         ```sh
         python3 -m venv .venv
         . .venv/bin/activate
         ```

    - Windows

        ```powershell
        python -m venv .venv
        .venv\Scripts\activate
         ```

4. Install the development dependencies, then install VideoXT in editable mode.

    ```sh
    python -m pip install -U pip
    pip install -r requirements-dev.txt && pip install -e .
    ```

5. Install the pre-commit hooks.

    ```sh
    pre-commit install --install-hooks
    ```

6. To reduce `pre-commit` changes, I recommend you enable Format on Save in your editor with `black` or `ruff` defaults. If you're in VS Code, `Ctrl+Shift+X` and search for [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) or [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) for instructions how to install and enable (either works).

    I use the Ruff extension and added this to my `settings.json`:

    ```json
    "[python]": {
        "editor.formatOnSave": true,
        "editor.formatOnSaveMode": "file",
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
    },
    ```

## Start coding

- Create a branch to identify the issue, feature addition or change you would like to work on.

    ```sh
    git fetch origin
    git checkout -b your-branch-name origin/main
    ```

- Using your favorite editor, make your changes, committing as you go.
  - Line length should be limited to 88 characters.
  - Use `ruff` to lint and format your code.
- Include tests that cover any code changes you make.
- Update any relevant docs pages and docstrings. To add a new page to the docs:
  - Create a `markdown.md` file in `docs/` for a navigation page or in `docs/docs/` for a documentation page.
  - Reflect the changes in `mkdocs.yml`.
- Push your commits to your fork on GitHub and create a pull request. If an issue is being addressed, link to the issue `fixes #123` in the pull request description.

    ```sh
    git push --set-upstream origin your-branch-name
    ```

## Running the tests

Run the basic test suite with `pytest`.

```sh
pytest
```

This runs the tests for the current environment, which is usually sufficient. CI will run the full suite when you submit your pull request. You can run the full test suite with `tox` if you have all the supported Python versions installed.

```sh
tox
```

Read more about [pytest](https://docs.pytest.org) and [tox](https://tox.readthedocs.io).

## Running test coverage

Generating a report of lines that do not have test coverage can indicate where to start contributing.

CI runs a test coverage report when you submit your pull request. See past [tests CI](https://github.com/gurrutia/videoxt/actions/workflows/tox.yml) runs to see the latest report, or run the report locally using `pytest` and `coverage`.

```sh
coverage erase
coverage run -m pytest tests/
coverage report
```

Read more about [coverage](https://coverage.readthedocs.io).

## Building the docs

CI will automatically build the docs, but before submitting your pull request, you should build and review the documentation locally using `mkdocs` to check for styling issues and broken links.

```sh
mkdocs serve
```

Read more about [mkdocs](https://www.mkdocs.org), [mkdocs-material](https://squidfunk.github.io/mkdocs-material), and [mkdocstrings-python](https://mkdocstrings.github.io/python/).

## What it is, is not and never will be

VideoXT is an easy-to-use, extensible video data extraction library.

It is not, and never will be, a full-featured video processing library. Consider [OpenCV](https://opencv.org/) or [FFmpeg](https://ffmpeg.org/) for that.

*If it doesn't extract, let's introspect,
VideoXT's aim, we resurrect.
Audio, frames, and gifs dissect,
Contributors, your skills perfect.
Expand the horizons, don't deflect,
In data realms, we intersect.*
