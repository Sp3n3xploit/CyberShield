import threading

from collections.abc import KeysView
from tkinter import messagebox
from typing import TypedDict

import customtkinter as ctk
import requests

from core.config import load_config

from gui.components.button import Button
from gui.components.icon import Icon
from gui.components.label import Label
from gui.components.notification import Notification
from gui.components.progress_bar import ProgressBar
from gui.components.result import Result


class Internet:

    @staticmethod
    def _connection_verification() -> bool:

        try:

            response: requests.Response = requests.get(

                "https://clients3.google.com/generate_204",
                timeout=5

            )

            return response.status_code == 204

        except requests.exceptions.RequestException:

            return False


class Layout:

    NO_INTERNET: str = (

        "To use CyberShield, "
        "please connect to a network with Internet access !"

    )

    WINDOW_SIZE: str = "900x370"

    GRID_ROWS: int = 10

    ROW_TOP: int = 0
    ROW_PROGRESS: int = 1
    ROWSPAN_PROGRESS: int = 10

    COLUMN_LEFT: int = 0
    COLUMN_MIDDLE: int = 1
    COLUMN_RIGHT: int = 2

    WEIGHT_HIGH: int = 1
    WEIGHT_LOW: int = 0

    PADX_PROGRESS: int = 10
    PADY_PROGRESS: int = 10
    PADDY_WIDGET: tuple[int, int] = (5, 0)

    NETWORK_WIDGETS: dict[str, tuple[int, int]] = {

        "contact": (0, 40),
        "github": (0, 5)

    }

    STICKY_WIDGET: str = "ne"
    STICKY_PROGRESS: str = "ns"


class Widget(TypedDict):

    has_icon: bool
    widget_class: type[Button] | type[Label]
    widget_name: KeysView[str]


class CyberShield(ctk.CTk):

    def __init__(self, **kwargs: str | int | bool) -> None:

        super().__init__(**kwargs)

        self._configure_grid()

        config_names: list[str] = ["buttons", "icons", "labels"]
        loaded_configs: dict[str, dict[str, str]] = {

            name: load_config(name) for name in config_names

        }

        self._configure_window(loaded_configs)

        self._build_widgets(loaded_configs)
        self._create_progress()

        Result(self)

    def _configure_grid(self) -> None:

        self.grid_columnconfigure(

            Layout.COLUMN_LEFT,
            weight=Layout.WEIGHT_HIGH

        )

        self.grid_columnconfigure(

            Layout.COLUMN_MIDDLE,
            weight=Layout.WEIGHT_LOW

        )

        self.grid_columnconfigure(

            Layout.COLUMN_RIGHT,
            weight=Layout.WEIGHT_HIGH

        )

    def _configure_window(

            self, loaded_configs: dict[str, dict[str, str]]) -> None:

        self.geometry(Layout.WINDOW_SIZE)
        self.iconbitmap(loaded_configs["icons"]["app_icon"])
        self.resizable(False, False)
        self.title("CyberShield :")

    def _configure_rows(self) -> None:

        for row_idx in range(Layout.GRID_ROWS):

            self.grid_rowconfigure(row_idx, weight=Layout.WEIGHT_LOW)

    def _build_widgets(

            self, loaded_configs: dict[str, dict[str, str]]) -> None:

        widget_configs: list[Widget] = [

            {
                "has_icon": True,
                "widget_class": Button,
                "widget_name": loaded_configs["buttons"].keys(),
            },

            {
                "has_icon": False,
                "widget_class": Label,
                "widget_name": loaded_configs["labels"].keys(),
            },

        ]

        for widget_config in widget_configs:

            widget_class: type[Button] | type[Label] = widget_config["widget_class"]

            for widget_id  in widget_config["widget_name"]:

                image: ctk.CTkImage | None = Icon.load(

                    widget_id) if widget_config["has_icon"] else None

                widget: Button | Label = widget_class(

                    self,
                    widget_id,
                    image=image

                )

                padx: tuple[int,

                            int] | None = Layout.NETWORK_WIDGETS.get(widget_id)

                if padx is not None:

                    widget.grid(

                        row=Layout.ROW_TOP,
                        column=Layout.COLUMN_RIGHT,
                        padx=padx,
                        pady=Layout.PADDY_WIDGET,
                        sticky=Layout.STICKY_WIDGET

                    )

    def _create_progress(self) -> None:

        self.progress_bar: ProgressBar = ProgressBar(self)

        self.progress_bar.grid(

            row=Layout.ROW_PROGRESS,
            column=Layout.COLUMN_RIGHT,
            rowspan=Layout.ROWSPAN_PROGRESS,
            padx=Layout.PADX_PROGRESS,
            pady=Layout.PADY_PROGRESS,
            sticky=Layout.STICKY_PROGRESS,

        )

        self.progress_bar.set(0.0)


def main() -> None:

    app = CyberShield()
    app.attributes("-alpha", 0.0)

    def show_window() -> None:

        app.attributes("-alpha", 1.0)
        Notification()

    def internet_error() -> None:

        messagebox.showwarning(

            title="CyberShield - Connection :",
            message=Layout.NO_INTERNET,

        )

        app.destroy()

    def internet_acces() -> None:

        if Internet._connection_verification():

            app.after(1500, show_window)

        else:

            app.after(0, internet_error)

    threading.Thread(target=internet_acces, daemon=True).start()
    app.mainloop()


if __name__ == "__main__":

    main()