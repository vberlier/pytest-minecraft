from zipfile import ZipFile

import pytest


@pytest.mark.parametrize(
    "flags, passed, failed, skipped",
    [
        ([], 0, 0, 2),
        (["--minecraft-latest"], 2, 0, 0),
        (["--minecraft-snapshot"], 1, 1, 0),
        (["--minecraft-latest", "--minecraft-snapshot"], 3, 1, 0),
    ],
)
def test_options(testdir, flags, passed, failed, skipped):
    testdir.makepyfile(
        """
        def test_minecraft_is_either_release_or_snapshot(minecraft):
            assert minecraft in {"release", "snapshot"}

        def test_minecraft_is_release(minecraft):
            assert minecraft == "release"
        """
    )

    result = testdir.runpytest(*flags)
    result.assert_outcomes(passed=passed, failed=failed, skipped=skipped)


def test_client_jar(minecraft_client_jar):
    assert minecraft_client_jar.suffix == ".jar"


def test_resource_pack(minecraft_resource_pack):
    assert minecraft_resource_pack.is_dir()

    namespace = minecraft_resource_pack / "assets" / "minecraft"

    assert (namespace / "blockstates").is_dir()
    assert (namespace / "font").is_dir()
    assert (namespace / "lang").is_dir()
    assert (namespace / "models").is_dir()
    assert (namespace / "particles").is_dir()
    assert (namespace / "shaders").is_dir()
    assert (namespace / "texts").is_dir()
    assert (namespace / "textures").is_dir()


def test_data_pack(minecraft_data_pack):
    assert minecraft_data_pack.is_dir()

    namespace = minecraft_data_pack / "data" / "minecraft"

    assert (namespace / "advancements").is_dir()
    assert (namespace / "loot_tables").is_dir()
    assert (namespace / "recipes").is_dir()
    assert (namespace / "structures").is_dir()
    assert (namespace / "tags").is_dir()


def test_with_client(minecraft_client_jar):
    assert minecraft_client_jar.name == "client.jar"

    with ZipFile(minecraft_client_jar) as client:
        assert len(client.namelist()) > 10_000


def test_with_resource_pack(minecraft_resource_pack):
    assert minecraft_resource_pack.name == "resource_pack"
    assert (minecraft_resource_pack / "assets" / "minecraft" / "textures").is_dir()


def test_with_data_pack(minecraft_data_pack):
    assert minecraft_data_pack.name == "data_pack"
    assert (minecraft_data_pack / "data" / "minecraft" / "loot_tables").is_dir()
