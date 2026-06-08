from pathlib import Path
from bs4 import BeautifulSoup, Tag, PageElement
from typing import Optional
from tqdm import tqdm
import re


def _get_download_info(session, url: str) -> tuple[str, str]:

    response = session.get(
        url, allow_redirects=True, headers={"Referer": "https://moddb.com"}
    )

    if not response.status_code == 200:
        raise ConnectionError(
            f"No response from URL {url}. Status code: {response.status_code}"
        )

    soup: BeautifulSoup = BeautifulSoup(response.text, "lxml")
    download_tag: Optional[Tag] = soup.find("a", href=re.compile("^/downloads/mirror/"))

    if download_tag is None:
        raise ConnectionError("Couldn't find download link")

    download_tag_content: PageElement = download_tag.contents[0]

    parsed_filename: str = (
        download_tag_content.translate({ord(char): None for char in "']"})
        .split(" ")[-1]
        .strip()
    )
    parsed_url: str = "https://moddb.com" + str(download_tag["href"])

    return parsed_filename, parsed_url


def _download_file(session, url: str, download_path: Path, filename: str) -> None:
    temp_path: str = download_path / (filename + ".part")
    full_path: str = download_path / filename

    try:
        with session.get(
            url, stream=True, timeout=10, headers={"Referer": "https://moddb.com"}
        ) as file_stream:
            file_stream.raise_for_status()

            with open(temp_path, "wb") as file:
                for chunk in tqdm(file_stream.iter_content(chunk_size=1024 * 1024)):
                    file.write(chunk)
    except Exception as error:
        raise ConnectionError(f"Download of {filename} failed.\n{error}") from error

    temp_path.rename(full_path)


def download(session, url: str, download_path: Path):
    download_info: tuple[str, str] = _get_download_info(session, url)

    filename: str = download_info[0]
    download_url: str = download_info[1]

    output_file: Path = download_path / filename

    if output_file.exists():
        print("-> Mod archive already exists. Skipping Download")
        return filename

    try:
        _download_file(session, download_url, download_path, filename)
    except Exception as error:
        print(error)
        return None

    return filename
