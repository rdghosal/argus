import abc
import typing as t


class BaseParser(abc.ABC):
    def __init__(self, path: str) -> None:
        with open(path, "r") as f:
            self.lines = f.readlines()

    @abc.abstractmethod
    def parse(self) -> list[str]:
        ...


class RequirementsParser(BaseParser):
    DELIMS: t.ClassVar[tuple[str, ...]] = (
        ">=",
        "==",
        "<=",
    )

    def parse(self) -> t.Iterable[str]:
        for line in self.lines:
            pkg = line.strip()
            for delim in self.DELIMS:
                if (pos := line.find(delim)) > -1:
                    pkg, _ = line[:pos].strip(), line[pos + 2:].strip()
                    break
            yield pkg
