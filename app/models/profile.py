from dataclasses import dataclass, field

from app.core.utils import clean_domains


@dataclass
class Profile:
    name: str
    interface: str = ''
    dns: str = '1.1.1.1'
    mode: str = 'normal'
    timeout: int = 30
    autostart: bool = False
    command: str = ''
    domains: list[str] = field(default_factory=list)

    def validate(self):
        if not self.name.strip():
            raise ValueError('имя профиля пустое')
        if self.timeout < 1:
            raise ValueError('таймаут должен быть больше 0')

    def to_dict(self):
        return {
            'name': self.name,
            'interface': self.interface,
            'dns': self.dns,
            'mode': self.mode,
            'timeout': self.timeout,
            'autostart': self.autostart,
            'command': self.command,
            'domains': clean_domains(self.domains),
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            name=d.get('name', ''),
            interface=d.get('interface', ''),
            dns=d.get('dns', '1.1.1.1'),
            mode=d.get('mode', 'normal'),
            timeout=int(d.get('timeout', 30)),
            autostart=bool(d.get('autostart', False)),
            command=d.get('command', ''),
            domains=clean_domains(d.get('domains', [])),
        )
