__version__ = "0.2.0"


import shutil
from pathlib import Path
from zipfile import ZipFile

import pytest
import requests

MINECRAFT_VERSIONS = "https://launchermeta.mojang.com/mc/game/version_manifest.json"


def pytest_addoption(parser):
    group = parser.getgroup("minecraft")
    group.addoption(
        "--minecraft-latest",
        action="store_true",
        help="run tests against the latest minecraft release",
    )
    group.addoption(
        "--minecraft-snapshot",
        action="store_true",
        help="run tests against the latest minecraft snapshot",
    )


def pytest_generate_tests(metafunc):
    if "minecraft" not in metafunc.fixturenames:
        return

    params = []
    option = metafunc.config.option

    if option.minecraft_latest:
        params.append("release")
    if option.minecraft_snapshot:
        params.append("snapshot")

    metafunc.parametrize("minecraft", params)


@pytest.fixture
def minecraft_cache_directory(request, minecraft):
    directory = Path(request.config.cache.makedir("minecraft"), minecraft)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


@pytest.fixture
def minecraft_client_jar(minecraft_cache_directory, minecraft):
    path = minecraft_cache_directory / "client.jar"
    if path.is_file():
        return path

    manifest = requests.get(MINECRAFT_VERSIONS).json()
    latest = manifest["latest"]

    version_url = next(
        version_info["url"]
        for version_info in manifest["versions"]
        if version_info["id"] == latest[minecraft]
    )

    client_url = requests.get(version_url).json()["downloads"]["client"]["url"]

    with path.open("wb") as fileobj:
        shutil.copyfileobj(requests.get(client_url, stream=True).raw, fileobj)

    return path


def _extract_pack(jar, prefix, destination):
    if destination.is_dir():
        return

    with ZipFile(jar) as client_jar:
        for filename in client_jar.namelist():
            if filename.startswith(prefix):
                client_jar.extract(filename, destination)

    mcmeta = destination / "pack.mcmeta"
    mcmeta.write_text('{"pack": {"pack_format": 6, "description": ""}}')


@pytest.fixture
def minecraft_resource_pack(minecraft_cache_directory, minecraft_client_jar):
    path = minecraft_cache_directory / "resource_pack"
    _extract_pack(minecraft_client_jar, "assets/", path)
    return path


@pytest.fixture
def minecraft_data_pack(minecraft_cache_directory, minecraft_client_jar):
    path = minecraft_cache_directory / "data_pack"
    _extract_pack(minecraft_client_jar, "data/", path)
    return path
