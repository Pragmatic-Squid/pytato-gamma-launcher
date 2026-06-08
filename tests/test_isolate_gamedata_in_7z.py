from pathlib import Path
import shutil
import py7zr

# extract archive to temporary folder
# create real folder with name from modlist
#
# move gamedata folder to real folder

archive_name: str = "Desmans_Horror_Overhaul_v1.3.7z"
archive: Path = "C:/Games/Stalker-Gamma/Downloads/Desmans_Horror_Overhaul_v1.3.7z"
# archive: Path = "C:/Games/Stalker-Gamma/Downloads/ExoServoSounds-v.2.0.7z"

install_path: Path = Path(
    "C:/Users/Jan/Documents/pytato_gamma_launcher/tests/mods/13- Quieter Wood Boxes Breaking - cringeybabey"
)
# install_path: Path = Path(
#     "C:/Games/Stalker-Gamma/Mods/9- Exo Servomotor Sounds - HarukaSai"
# )
temp_directory: Path = Path("C:/Users/Jan/Documents/pytato_gamma_launcher/tests/temp/")

mods_folder: Path = Path("C:/Games/Stalker-Gamma/Mods/")

subfolder: str = "Desman's Horror Overhaul v1.3"

# target_folder = "9- Exo Servomotor Sounds - HarukaSai"
target_folder = "13- Quieter Wood Boxes Breaking - cringeybabey"


def check_gamedata_depth(file_list: list) -> dict:
    splits: list = [file.split("/") for file in file_list]

    new_file_dict: dict = {}

    gamedata_folder = next([item for item in file_list if "gamedata" in item])
    print(gamedata_folder)
    return

    for split in splits:
        if "gamedata" in split[0]:
            return

        else:
            # path_items: list = split[1:]
            #
            # old_path: Path = "/".join(split)
            # new_path: Path = "/".join(path_items)
            #
            # new_file_dict[old_path] = new_path

            print(" ".join(split))

            try:
                gamedata_index: int = split.index("gamedata")
                print(split[gamedata_index])
            except:
                print("No index for 'gamedata' found")

    return new_file_dict


def get_gamedata_folders(path_to_check: list) -> list:
    gamedata_folders: list = []

    for path in path_to_check.rglob("*"):
        if not path.is_dir() or "gamedata" not in str(path):
            continue

        splits: list = str(path).split("\\")

        if splits[-1] == "gamedata":
            gamedata_folders.append(path)

    return gamedata_folders


def move_gamedata_below_root(file_dict: dict) -> None:
    for file in file_dict:
        old_path: Path = file
        new_path: Path = file_dict[file]

        old_path.move(new_path)


def move_gamdata_to_mod_folder(gamedata_folders: list, mod_folder: Path) -> None:
    try:
        for folder in gamedata_folders:
            folder.move_into(mod_folder)
    except:
        print("-> Gamedata folder already exists")


# Create temp folder
temp_extract_folder: Path = temp_directory / archive_name


with py7zr.SevenZipFile(archive, mode="r") as archive:
    all_files = archive.getnames()

    targets = [file for file in all_files if file.startswith(subfolder)]

    # new_file_dict = check_gamedata_depth(targets)

    archive.extract(targets=targets, path=temp_extract_folder)

gamedata_folders: list = get_gamedata_folders(temp_extract_folder)

# Create final folder
mod_folder: Path = mods_folder / target_folder
mod_folder.mkdir(exist_ok=True)

# Move gamedata folder to final folder

move_gamdata_to_mod_folder(gamedata_folders, mod_folder)

# Remove temp folder
shutil.rmtree(temp_extract_folder)
