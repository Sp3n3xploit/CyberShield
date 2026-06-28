from pathlib import Path
from notifypy import Notify

from core.config import load_config


class Notification(Notify):

    def __init__(self, **kwargs) -> None:

        super().__init__(**kwargs)

        audios_config: dict[str, str] = load_config("audios")
        icons_config: dict[str, str] = load_config("icons")

        self.application_name = "CyberShield :"
        self.title = ""

        audio_path: Path = Path(audios_config["welcome"]).resolve()
        audio_path = Path(audio_path).resolve()

        icon_path: Path = Path(icons_config["app_icon"]).resolve()
        icon_path = Path(icon_path).resolve()

        self.audio = str(audio_path) if audio_path.exists() else None
        self.icon = str(icon_path) if icon_path.exists() else None

        self.message = (

            "Thank you for using CyberShield ; "
            "If you have any problems or questions, "
            "please don't hesitate to contact me !"

        )

        self.send()
