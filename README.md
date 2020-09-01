# pytest-minecraft

[![Build Status](https://travis-ci.com/vberlier/pytest-minecraft.svg?branch=master)](https://travis-ci.com/vberlier/pytest-minecraft)
[![PyPI](https://img.shields.io/pypi/v/pytest-minecraft.svg)](https://pypi.org/project/pytest-minecraft/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-minecraft.svg)](https://pypi.org/project/pytest-minecraft/)

> A pytest plugin for running tests against Minecraft releases.

The plugin automatically downloads the latest version of the Minecraft client into the pytest cache. The provided fixtures can also extract the vanilla [resource pack](https://minecraft.gamepedia.com/Resource_Pack) and [data pack](https://minecraft.gamepedia.com/Data_Pack) on demand.

## Installation

The package can be installed with `pip`.

```bash
$ pip install pytest-minecraft
```

## Usage

Downloading the Minecraft client takes a few seconds so the tests that use the fixtures provided by the plugin will be skipped unless explicitly enabled with a command-line flag. The `--minecraft-latest` flag will enable the tests and run them against the latest stable release.

```sh
$ pytest --minecraft-latest
```

You can also use the `--minecraft-snapshot` flag to test against the latest snapshot. Both flags can be specified at the same time to run the tests against both stable and snapshot releases.

```sh
$ pytest --minecraft-latest --minecraft-snapshot
```

### Fixtures

- The `minecraft_client_jar` fixture returns the path to the downloaded Minecraft client as a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path) instance.

  ```python
  def test_with_client(minecraft_client_jar):
      assert minecraft_client_jar.name == "client.jar"

      with ZipFile(minecraft_client_jar) as client:
          assert len(client.namelist()) > 10_000
  ```

- The `minecraft_resource_pack` fixture returns the path to the extracted vanilla resource pack as a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path) instance.

  ```python
  def test_with_resource_pack(minecraft_resource_pack):
      assert minecraft_resource_pack.name == "resource_pack"
      assert (minecraft_resource_pack / "assets" / "minecraft" / "textures").is_dir()
  ```

- The `minecraft_data_pack` fixture returns the path to the extracted vanilla data pack as a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path) instance.

  ```python
  def test_with_data_pack(minecraft_data_pack):
      assert minecraft_data_pack.name == "data_pack"
      assert (minecraft_data_pack / "data" / "minecraft" / "loot_tables").is_dir()
  ```

## Contributing

Contributions are welcome. This project uses [`poetry`](https://python-poetry.org/).

```sh
$ poetry install
```

You can run the tests with `poetry run pytest`.

```sh
$ poetry run pytest
```

The code follows the [black](https://github.com/psf/black) code style.

```sh
$ poetry run black .
```

---

License - [MIT](https://github.com/vberlier/pytest-minecraft/blob/master/LICENSE)
