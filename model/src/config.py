import pathlib
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath
from tomlkit import parse


root_dir = pathlib.Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    models: DirectoryPath = root_dir / "./models/"
    data: DirectoryPath = root_dir / "./data/"
    static: DirectoryPath = root_dir / "./"
    docker: bool = False

    class Config:
        env_prefix = "demucs_"


settings = Settings()

settings_file = root_dir / Path("settings.toml")
if settings_file.exists():
    file_settings = parse(settings_file.read_text())
    settings = Settings.parse_obj(file_settings)
