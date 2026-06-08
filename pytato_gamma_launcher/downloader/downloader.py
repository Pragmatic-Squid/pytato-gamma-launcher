from pathlib import Path
from downloader.moddb import download


class DownloaderError(Exception):
    """Base error for downloader"""


class ProviderError(DownloaderError):
    """Raised when provider in URL not recognized"""


def download_mod(session, url: str, download_path: Path) -> str:
    filename: str = ""

    if "moddb" in url:
        filename = download(session, url, download_path)
        # ModDBDownloader.download(session, mod)
        None
    elif "github" in url:
        # TODO Create GithubDownloader
        # GitHubDownloader.download(session, mod)
        filename = None
    else:
        raise ProviderError(f"Provider in URL {url} not recognized")

    return filename
