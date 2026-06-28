import customtkinter as ctk

from core.config import load_config


class Label(ctk.CTkLabel):

    def __init__(self, master, label_name: str, **kwargs) -> None:

        config: dict[str, dict[str, int | str]] = load_config("labels")
        self.label_config = config[label_name].copy()

        self.label_config.pop("font", None)

        row = kwargs.pop("row", self.label_config.pop("row", 0))
        text = kwargs.pop("text", self.label_config.pop("text", ""))

        super().__init__(

            master,
            font=self._label_font(),
            text=text,
            **self.label_config,
            **kwargs,

        )

        self.grid(column=0, padx=10, pady=5, row=row, sticky="nw")

    def _label_font(self) -> tuple[str, int, str]:

        font_config: dict[str, str | int] = load_config("font")
        font: dict[str, str | int] = font_config

        return (str(font["family"]), int(font["size"]), str(font["bold"]))
