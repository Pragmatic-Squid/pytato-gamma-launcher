from pathlib import Path
from mod import Mod
import shutil
import py7zr
import zipfile

DOWNLOADS_DIR: Path = Path("C:/Games/Stalker-Gamma/Downloads/")
MODS_DIR: Path = Path("C:/Games/Stalker-Gamma/Mods/")
TEMP_DIR: Path = Path("C:/Games/Stalker-Gamma/Temp")


class InstallerError(Exception):
    """Base error for installer"""


class ExctractionError(InstallerError):
    """Raised when BeautifulSoup can't find the link"""


def _extract_mod_archive(mod_archive: Path, mod_subdirs: list, out_dir: Path) -> None:
    # out_dir: Path = MODS_DIR / mod.dir_name
    # out_dir.mkdir(parents=True, exist_ok=True)

    # dir_name: str = f"{mod.modlist_number} - {mod.name} {mod.author}"

    # BUG: This will cause subdir to not be extracted
    # if out_dir.is_dir():
    #     print("-> dir already exists")
    #   return

    extension: str = str(mod_archive).split(".")[-1]

    if mod_subdirs[0] == "0":
        match extension:
            case "zip":
                shutil.unpack_archive(mod_archive, out_dir)
            case "7z":
                with py7zr.SevenZipFile(mod_archive, mode="r") as archive:
                    archive.extractall(path=out_dir)
            case "rar":
                # rar not supported yet
                return
    else:
        for subdir in mod_subdirs:
            target_subdir: str = subdir + "/"

            match extension:
                case "zip":
                    _extraxt_zip(mod_archive, target_subdir, out_dir)
                case "7z":
                    _extract_7zip(mod_archive, target_subdir, out_dir)
                case "rar":
                    # rar not supported yet
                    return


def _extraxt_zip(mod_archive: str, target_subdir: str, out_dir: Path) -> None:
    with zipfile.ZipFile(mod_archive, "r") as archive:
        all_files = archive.namelist()

        members = [file for file in all_files if file.startswith(target_subdir)]

        if members:
            archive.extractall(path=out_dir, members=members)
        else:
            print("-> !!! Subdirectory not found !!! 7zip")
            print("-> !!! Extracting whole archive !!! 7zip")
            archive.extractall(path=out_dir)
            return


def _extract_7zip(mod_archive: str, target_subdir: str, out_dir: Path) -> None:

    with py7zr.SevenZipFile(mod_archive, mode="r") as archive:
        all_files = archive.getnames()

        targets = [file for file in all_files if file.startswith(target_subdir)]

        if targets:
            archive.extract(targets=targets, path=out_dir)
        else:
            print("-> !!! Subdirectory not found !!! 7zip")
            print("-> !!! Extracting whole archive !!! 7zip")
            archive.extract(path=out_dir)
            return


def _get_gamedata_dirs(dir_to_check: list) -> list:
    gamedata_dirs: list = []

    for path in dir_to_check.rglob("*"):
        if not path.is_dir() or "gamedata" not in str(path):
            continue

        splits: list = str(path).split("\\")

        if splits[-1] == "gamedata":
            gamedata_dirs.append(path)

    print(gamedata_dirs)
    return gamedata_dirs


def _copy_gamedata_to_mod_dir(gamedata_dirs: list, mod_dir: Path) -> None:
    try:
        for dir in gamedata_dirs:
            shutil.copytree(dir, mod_dir, dirs_exist_ok=True)
    except Exception as error:
        print(f"\t-> Error while copying gamedata.\n{error}")


def _create_mod_dir(path: Path) -> None:
    path.mkdir(exist_ok=True)


def _remove_temp_extract_dir(temp_dir: Path):
    shutil.rmtree(temp_dir)


def install_mod(
    mod: Mod, filename: str, download_path: Path, install_path: Path, dir_name: str
) -> None:

    TEMP_DIR.mkdir(exist_ok=True)

    mod_dir: Path = MODS_DIR / dir_name
    archive_extension: str = filename.split(".")[-1]

    if archive_extension == "rar":
        print("-> Rar. Skipping")
        return

    if mod_dir.is_dir():
        return

    temp_extract_dir: Path = TEMP_DIR / filename.split(".")[0]
    mod_archive: Path = DOWNLOADS_DIR / filename
    mod_subdirs: list = mod.subdirs

    try:
        _extract_mod_archive(mod_archive, mod_subdirs, temp_extract_dir)
    except Exception as error:
        raise ExctractionError(f"ERROR: {error}")

    _create_mod_dir(mod_dir)

    # BUG: not all mods contain a gamedata folder, some only have a "db" folder
    gamedata_dirs: list = _get_gamedata_dirs(temp_extract_dir)

    # BUG: the gamedata directory itself isn't copied, only its contents
    _copy_gamedata_to_mod_dir(gamedata_dirs, mod_dir)

    try:
        _remove_temp_extract_dir(temp_extract_dir)
    except Exception as error:
        print(error)
