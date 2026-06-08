from dataclasses import dataclass


@dataclass
class Mod:
    mod_id: int
    url: str
    subdirs: list
    author: str
    name: str
    modpage_url: str
    dir_name: int

    filename: str = None
    download_url: str = None

    def add_download_url(self, download_url: str):
        self.download_url = download_url

    def add_filename(self, filename: str):
        self.filename = filename

    def append_subdirs(self, subdir: str):
        self.subdirs.append(subdir)

    def print(self):
        print(f"ID: {self.mod_id}")
        print(f"URL: {self.url}")
        print(f"Subfolders: {self.subfolders}")
        print(f"Author: {self.author}")
        print(f"Name: {self.name}")
        print(f"Mod Page: {self.mod_url}")

    def to_dict(self) -> dict:
        return {
            "id": self.mod_id,
            "url": self.url,
            "subfolders": self.subfolders,
            "author": self.author,
            "name": self.name,
            "mod_url": self.mod_url,
            "filename": self.filename,
        }
