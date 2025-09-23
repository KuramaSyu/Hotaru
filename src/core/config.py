from dataclasses import dataclass, field, asdict
import yaml
from typing import Dict, Any
import logging

@dataclass
class BotConfig:
    secret: str = "YOUR_API_KEY_HERE"

@dataclass
class MALConfig:
    id: str = "YOUR_MAL_CLIENT_ID_HERE"
    secret: str = "YOUR_MAL_SECRET_HERE"

@dataclass
class Config:
    bot: BotConfig = field(default_factory=BotConfig)
    mal: MALConfig = field(default_factory=MALConfig)

    @staticmethod
    def from_path(path: str) -> "Config":
        try:
            with open(path, "r") as f:
                data: Any = yaml.safe_load(f)
        except FileNotFoundError:
            default_config = Config()
            default_config.write_template(path)
            raise FileNotFoundError(f"Config file not found. A template has been created at {path}. Please fill it out and restart the application.")

        # Merge with default template
        bot_data = data.get("bot", {})
        return Config(
            bot=BotConfig(**bot_data),
            mal=MALConfig(**data.get("mal", {}))
        )

    def write_template(self, path: str) -> None:
        """Write the default config structure to a YAML file."""
        with open(path, "w") as f:
            yaml.safe_dump(asdict(self), f, sort_keys=False)

    def as_dict(self) -> Dict[str, Any]:
        """Return config as a dictionary."""
        return asdict(self)
