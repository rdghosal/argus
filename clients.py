import typing as t

import bs4
import requests


class PyPIClient:
    BASE_URL: t.ClassVar[str] = "https://pypi.org/simple/"

    @classmethod
    def _get_release_info(cls, package: str) -> str:
        res = requests.get(cls.BASE_URL + package)
        return res.text

    @staticmethod
    def _format_version(package: str, release: str) -> str:
        return release.replace(".tar.gz", "").replace(package, "").replace("-", "")

    @classmethod
    def get_latest_version(cls, package: str) -> str:
        parsed: bs4.BeautifulSoup = bs4.BeautifulSoup(
            cls._get_release_info(package), "html.parser"
        )
        releases = parsed.find_all("a")
        return cls._format_version(package, releases[-1].get_text())
