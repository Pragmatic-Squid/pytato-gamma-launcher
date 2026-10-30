from pathlib import Path
from bs4 import BeautifulSoup, Tag, PageElement
from typing import Optional
from tqdm import tqdm
import re


# Use a regular desktop Firefox user agent. This identifies the HTTP client;
# it does not bypass ModDB's access controls or guarantee a successful download.
MODDB_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) "
        "Gecko/20100101 Firefox/131.0"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Referer": "https://www.moddb.com/",
}


def _log_redirects(response) -> None:
    """Print the HTTP redirect chain and final response URL."""
    for index, redirect in enumerate(response.history, start=1):
        print(
            f"-> Redirect {index}: "
            f"{redirect.status_code} {redirect.url} -> {redirect.headers.get('Location', '')}"
        )

    print(f"-> Final response: {response.status_code} {response.url}")


def _get_download_info(session, url: str) -> tuple[str, str]:
    response = session.get(
        url,
        allow_redirects=True,
        headers=MODDB_HEADERS,
        timeout=30,
    )
    _log_redirects(response)

    if response.status_code != 200:
        raise ConnectionError(
            f"No response from URL {url}. Status code: {response.status_code}"
        )

    soup: BeautifulSoup = BeautifulSoup(response.text, "lxml")
    download_tag: Optional[Tag] = soup.find(
        "a", href=re.compile("^/downloads/mirror/")
    )

    if download_tag is None:
        raise ConnectionError(
            "Couldn't find download link. "
            "ModDB may have returned a bot check, an error page, or a changed page layout."
        )

    download_tag_content: PageElement = download_tag.contents[0]

    parsed_filename: str = (
        download_tag_content.translate({ord(char): None for char in "']"})
        .split(" ")[-1]
        .strip()
    )
    parsed_url: str = "https://www.moddb.com" + str(download_tag["href"])

    print(f"-> ModDB download endpoint: {parsed_url}")
    return parsed_filename, parsed_url


def _download_file(session, url: str, download_path: Path, filename: str) -> None:
    temp_path: Path = download_path / (filename + ".part")
    full_path: Path = download_path / filename

    try:
        with session.get(
            url,
            stream=True,
            timeout=30,
            allow_redirects=True,
            headers=MODDB_HEADERS,
        ) as file_stream:
            _log_redirects(file_stream)
            file_stream.raise_for_status()

            download_path.mkdir(parents=True, exist_ok=True)
            total_size = int(file_stream.headers.get("Content-Length", 0))
            print(
                f"-> Downloading {filename}"
                + (f" ({total_size / 1024 / 1024:.1f} MiB)" if total_size else "")
            )

            with open(temp_path, "wb") as file:
                for chunk in tqdm(
                    file_stream.iter_content(chunk_size=1024 * 1024),
                    unit="MiB",
                ):
                    if chunk:
                        file.write(chunk)
    except Exception as error:
        raise ConnectionError(f"Download of {filename} failed.\n{error}") from error

    temp_path.rename(full_path)
    print(f"-> Saved: {full_path}")


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
