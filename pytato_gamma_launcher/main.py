import mod_handler
from mod import Mod
from pathlib import Path
import cloudscraper
from downloader import downloader
import installer

# --- init Variables ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/119.0.0.0 Safari/537.36"
}

modpack_maker_list_path: str = (
    "C:/Users/Jan/Documents/pytato_gamma_launcher/tests/modpack_maker_list.txt"
)
modlist_path: str = (
    "C:/Users/Jan/Documents/pytato_gamma_launcher/tests/modlist-dx8_edited.txt"
)
download_path: Path = Path("C:/Games/Stalker-Gamma/Downloads")
install_path: Path = Path("C:/Games/Stalker-Gamma/Mods")

scraper_session = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "desktop": True}
)
scraper_session.headers.update(HEADERS)

# --- Main execution ---
file_path = Path(modpack_maker_list_path)

if not file_path.is_file():
    print("maker list not found!")
    exit()

print("Getting mod list")
modlist: dict = mod_handler.get_modlist(modlist_path)

print("Getting modpack maker list")
modpack_maker_list: list[Mod] = mod_handler.get_modpack_maker_list(
    modpack_maker_list_path, modlist
)

for i, mod in enumerate(modpack_maker_list, start=1):
    print(f"[{i}/{len(modpack_maker_list)}] Working on {mod.name}")
    # print(f"[{i}/{len(modpack_maker_list)}] Downloading {mod.name}")
    print("\t-> Downloading...")
    filename: str = downloader.download_mod(scraper_session, mod.url, download_path)

    if filename is None:
        raise ValueError(f"No filename returned for {mod}")

    # TODO folder_name is not correctly assigned
    # I have no idea why the fuck that is...

    # print(f"[{i}/{len(modpack_maker_list)}] Installing {mod.name}")
    print("\t-> Installing...")
    installer.install_mod(mod, filename, download_path, install_path, mod.dir_name)


# TODO Initialize Mods by copying the correct subfolders and renaming them


# --- Install Gamma ---
# Download Grok's Modpack from GutHub
# Download Mod Manager from GitHub
# Patch Anomaly installation
# - copy files from .Grok's Modpack Installer\G.A.M.M.A\modpack_patches to Anomaly folder
# - check, if user config is to be preserved
# Gamma directory contains "Downloads" for downloaded mod archives and "mods" for extracted mods
# Copy .Grok's Modpack Installer\G.A.M.M.A\modpack_addons to Gamma\mods
