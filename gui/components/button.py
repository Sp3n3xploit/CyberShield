import customtkinter as ctk

from core.config import load_config


class Button(ctk.CTkButton):

    def __init__(self, master, button: str, **kwargs) -> None:

        config: dict[str, dict[str, int | str]] = load_config("buttons")
        self.button_config = config[button].copy()

        corner_radius = kwargs.pop(

            "corner_radius", self.button_config.pop("corner_radius", 0)

        )

        row = kwargs.pop("row", self.button_config.pop("row"))
        text = kwargs.pop("text", self.button_config.pop("text"))

        super().__init__(

            master,
            corner_radius=corner_radius,
            font=self._button_font(),
            text=text,
            **self.button_config,
            **kwargs,

        )

        self.grid(column=0, padx=5, pady=5, row=row, sticky="nw")

    def _button_font(self) -> tuple[str, int, str]:

        font_config: dict[str, str | int] = load_config("font")
        font: dict[str, str | int] = font_config

        return (str(font["family"]), int(font["size"]), str(font["bold"]))
