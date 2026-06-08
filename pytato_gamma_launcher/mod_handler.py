from mod import Mod


def get_modlist(modlist_path) -> dict:
    parsed_dict: dict = dict()

    with open(modlist_path, "r") as modlist_file:
        for line in modlist_file:
            if (
                line.startswith("#")
                or "End" in line
                or "separator" in line
                or line.startswith("\n")
            ):
                continue

            modlist_folder_name: str = line[1:]

            splits: list = line[1:].split("-")

            modlist_name: str = ""

            if len(splits) == 1:
                modlist_name = splits[0].strip()
            elif len(splits) == 4:
                modlist_name = splits[1].strip() + " - " + splits[2].strip()
            else:
                modlist_name = splits[1].strip()

            parsed_dict[modlist_name] = modlist_folder_name

    return parsed_dict


def get_modpack_maker_list(modpack_maker_list_path, modlist: dict) -> list[Mod]:
    parsed_list: list[Mod] = []

    # Not needed?
    # seen_ids: list[int] = []
    mod_names: list = []

    for name in modlist:
        mod_names.append(name)

    with open(modpack_maker_list_path, "r") as maker_file:
        for line in maker_file:
            if (
                line.startswith(" ")
                or line.startswith("#")
                or line.startswith("https://github")
            ):
                continue

            splits: list[str] = line.strip().split("\t")

            name: str = splits[3].strip()

            if name not in mod_names:
                # Skip this mod, as it is not in the modlist and thus can be ignored
                # print(f"{name} not in modlist")
                continue

            url: str = splits[0].strip()
            author: str = splits[2].strip()
            folder_name: str = modlist[name].strip()

            # TODO I don't need the mod_manager_number
            # save the modlist_folder_name instead
            # mod_manager_number: int = modlist[name]

            subfolders_string: str = splits[1].strip()
            subfolders: list = list()

            if "\\" in subfolders_string:
                print("\treplacing slashes")
                subfolders_string = subfolders_string.replace("\\", "/")
                print(f"\tnew string: {subfolders_string}")

            if ":" in subfolders_string:
                subfolders = subfolders_string.split(":")
            else:
                subfolders.append(subfolders_string)

            if "github" not in line:
                mod_id: int = int(url.split("/")[-1])

            modpage_url: str = ""

            try:
                modpage_url = splits[4].strip()
            except Exception as error:
                print(f"Mod {name} has no modpage URL.")
                print(f"Original error: {error}")

            new_mod: Mod = Mod(
                mod_id,
                url,
                subfolders,
                author,
                name,
                modpage_url,
                folder_name,
            )

            parsed_list.append(new_mod)

            print(f"Adding new mod to list: {name}")

            # I think I don't need this anymore.
            # If the ID of the mod in the maker file already exists
            # a new mod should be created, as its name differs from
            # the mod with the same id

            # if mod_id not in seen_ids:
            #    new_mod: Mod = Mod(
            #   mod_id,
            #   url,
            #   subfolders,
            #   author,
            #   name,
            #   modpage_url,
            #   folder_name,
            # )
            # parsed_list.append(new_mod)
            #
            # print(f"Adding new mod to list: {name}")
            #
            # seen_ids.append(mod_id)
            # else:
            # print(f"Appending a subfolder to {name}")
            # existing_mod: Mod = next(
            #    mod for mod in parsed_list if mod.mod_id == mod_id
            # )
            # for subfolder in subfolders:
            #    existing_mod.append_subfolder(subfolder)

    return parsed_list


def _create_github_mod():
    return
