from pathlib import Path
import zipfile
import os

archive: Path = "C:/Users/Jan/Documents/pytato_gamma_launcher/tests/downloads/Quieter_Wood_Breaking.1.zip"
install_path: Path = Path(
    "C:/Users/Jan/Documents/pytato_gamma_launcher/tests/mods/13- Quieter Wood Boxes Breaking - cringeybabey"
)
target_folder = "Desman's Horror Overhaul v1.3"

all_files: list = []
files_to_extract: list = []

with py7zr.ZipFile(archive, "r") as archive_ref:
    for member in archive_ref.infolist():
        if "gamedata" in member.filename:
            gamedata_index: int = member.filename.index("gamedata")

            new_path: str = member.filename[gamedata_index:]

            new_relative_path: Path = Path(f"{install_path}/{new_path}")

            print(f"new path: {new_relative_path}")

            if member.is_dir():
                new_relative_path.mkdir(parents=True, exist_ok=True)
            else:
                new_relative_path.parent.mkdir(parents=True, exist_ok=True)

                with (
                    archive_ref.open(member) as source,
                    open(new_relative_path, "wb") as target,
                ):
                    target.write(source.read())

        # parts = member.filename.split("/")
        # try:
        #    gd_index = parts.index("gamedata")
        # except ValueError:
        #    continue

        # Construct a new path starting from 'gamedata'
        # This effectively ignores any parent folders
        # new_relative_path = os.path.join(*parts[gd_index:])

        # print(new_relative_path)

    # for file in files_to_extract:
    #    archive_ref.extract(file, path=install_path)
