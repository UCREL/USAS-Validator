# USAS-Validator

Validates USAS semantic tags and loads through the Python package a USAS mapper of USAS tags to their descriptions.

## Installation

``` bash
pip install -e .
```

## Quick guide

If you have a a list of USAS semantic tags in a String like so it will validate that they follow the USAS semantic tag schema and return them as a `list[USASTagGroup]`:

``` python
from usas_validator import utils
usas_tag_string = "Z2/S2mf E3-"
usas_tag_groups = utils.parse_usas_token_group(usas_tag_string)
for usas_token_group in usas_tag_groups:
  print(usas_token_group)
  print()
```

Output:
``` bash
tags=[USASTag(tag='Z2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False), USASTag(tag='S2', number_positive_markers=0, number_negative_markers=0, rarity_marker_1=False, rarity_marker_2=False, female=True, male=True, antecedents=False, neuter=False, idiom=False)]

tags=[USASTag(tag='E3', number_positive_markers=0, number_negative_markers=1, rarity_marker_1=False, rarity_marker_2=False, female=False, male=False, antecedents=False, neuter=False, idiom=False)]
```

You can also load all the USAS tags and their descriptions like so:
``` python
from usas_validator import utils
for usas_tag, tag_description in utils.load_usas_mapper(None, None).items():
  print(f"Tag: {usas_tag}   Description: {tag_description}")
```

The output is long thus only showing the first 5 tags:

``` bash
Tag: A1.1.1   Description: title: General actions, making etc. description: General/abstract terms relating to an activity/action (e.g. act, adventure, approach, arise); a characteristic/feature (e.g. absorb, attacking, automatically); aconstruction/craft and/or the action of constructing/crafting (e.g. arrange, assemble, bolts, boring, break)
Tag: A1.1.2   Description: title: Damaging and destroying description: General/abstract terms depicting damage/destruction/demolition/pollution, etc
Tag: A1.2   Description: title: Suitability description: General/abstract terms relating to appropriateness, suitability, aptness, etc
Tag: A1.3   Description: title: Caution description: General/abstract terms relating to vigilance/care/prudence, or the lack of.
Tag: A1.4   Description: title: Chance, luck description: General/abstract terms depicting likelihood/probability/providence, or the lack of.
```

## Setup

You can either use the dev container with your favourite editor, e.g. VSCode. Or you can create your setup locally below we demonstrate both.

In both cases they share the same tools, of which these tools are:
* [uv](https://docs.astral.sh/uv/) for Python packaging and development
* [make](https://www.gnu.org/software/make/) (OPTIONAL) for automation of tasks, not strictly required but makes life easier.

### Dev Container

A [dev container](https://containers.dev/) uses a docker container to create the required development environment, the Dockerfile we use for this dev container can be found at [./.devcontainer/Dockerfile](./.devcontainer/Dockerfile). To run it locally it requires docker to be installed, you can also run it in a cloud based code editor, for a list of supported editors/cloud editors see [the following webpage.](https://containers.dev/supporting)

To run for the first time on a local VSCode editor (a slightly more detailed and better guide on the [VSCode website](https://code.visualstudio.com/docs/devcontainers/tutorial)):
1. Ensure docker is running.
2. Ensure the VSCode [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension is installed in your VSCode editor.
3. Open the command pallete `CMD + SHIFT + P` and then select `Dev Containers: Rebuild and Reopen in Container`

You should now have everything you need to develop, `uv`, `make`, for VSCode various extensions like `Pylance`, etc.

If you have any trouble see the [VSCode website.](https://code.visualstudio.com/docs/devcontainers/tutorial).

### Local

To run locally first ensure you have the following tools installted locally:
* [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python packaging and development. (version `0.9.6`)
* [make](https://www.gnu.org/software/make/) (OPTIONAL) for automation of tasks, not strictly required but makes life easier.
  * Ubuntu: `apt-get install make`
  * Mac: [Xcode command line tools](https://mac.install.guide/commandlinetools/4) includes `make` else you can use [brew.](https://formulae.brew.sh/formula/make)
  * Windows: Various solutions proposed in this [blog post](https://earthly.dev/blog/makefiles-on-windows/) on how to install on Windows, inclduing `Cygwin`, and `Windows Subsystem for Linux`.

When developing on the project you will want to install the Python package locally in editable format with all the extra requirements, this can be done like so:

```bash
uv sync
```

### Linting

Linting and formatting with [ruff](https://docs.astral.sh/ruff/) it is a replacement for tools like Flake8, isort, Black etc, and we us [ty](https://github.com/astral-sh/ty) for type checking.

To run the linting:

``` bash
make lint
```

### Tests

To run the tests (uses pytest and coverage) and generate a coverage report:

``` bash
make test
```