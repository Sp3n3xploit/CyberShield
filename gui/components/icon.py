from functools import cache

import customtkinter as ctk

from PIL import Image
from PIL.ImageFile import ImageFile

from core.config import load_config


class Icon(ctk.CTkImage):

    def __init__(self, path: str, size: tuple) -> None:

        image: ImageFile = Image.open(path)
        super().__init__(light_image=image, dark_image=image, size=size)

    @classmethod
    @cache
    def load(

            cls,
            icon_name: str,
            size: tuple = (20, 20)) -> ctk.CTkImage | None:

        config: dict[str, str] = load_config("icons")
        icon_path: str | None = config.get(icon_name)

        if icon_path:

            return cls(icon_path, size)

        return None
