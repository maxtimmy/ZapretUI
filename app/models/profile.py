from dataclasses import dataclass, field

from app.core.constants import DEFAULT_DNS, DEFAULT_MODE
from app.core.utils import is_blank, normalize_domains


@dataclass
class Profile:
    name: str
    interface: str = ""
    dns: str = DEFAULT_DNS
    mode: str = DEFAULT_MODE
    timeout: int = 30
    autostart: bool = False
    command: str = ""
    domains: list[str] = field(default_factory=list)

    def validate(self, *, require_command: bool = False) -> tuple[bool, str]:
        if is_blank(self.name):
            return False, "profile name is empty"
        if self.timeout <= 0:
            return False, "timeout must be > 0"
        if require_command and is_blank(self.command):
            return False, "command is empty"
        if not isinstance(self.domains, list):
            return False, "domains must be list"
        return True, ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "interface": self.interface,
            "dns": self.dns,
            "mode": self.mode,
            "timeout": self.timeout,
            "autostart": self.autostart,
            "command": self.command,
            "domains": normalize_domains(self.domains),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        return cls(
            name=str(data.get("name", "")).strip(),
            interface=str(data.get("interface", "")).strip(),
            dns=str(data.get("dns", DEFAULT_DNS)).strip(),
            mode=str(data.get("mode", DEFAULT_MODE)).strip(),
            timeout=int(data.get("timeout", 30) or 30),
            autostart=bool(data.get("autostart", False)),
            command=str(data.get("command", "")).strip(),
            domains=normalize_domains(data.get("domains", [])),
        )
