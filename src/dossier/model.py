"""Result types shared by every check."""

from dataclasses import dataclass
from enum import StrEnum


class Status(StrEnum):
    """Outcome of one check. `unknown` is never a pass."""

    OK = "ok"
    FAIL = "fail"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Result:
    """One line of output: a check name, its status and a short reason."""

    check: str
    status: Status
    message: str

    def line(self) -> str:
        """Render as `status check: message`."""
        return f"{self.status.value:<7} {self.check}: {self.message}"


def exit_code(results: list[Result]) -> int:
    """0 all ok, 1 any fail, 2 no fail but an unknown (or nothing ran)."""
    if any(r.status is Status.FAIL for r in results):
        return 1
    if not results or any(r.status is Status.UNKNOWN for r in results):
        return 2
    return 0
