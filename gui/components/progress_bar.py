import customtkinter as ctk


class ProgressBar(ctk.CTkProgressBar):

    def __init__(self, master, **kwargs) -> None:

        super().__init__(

            master,
            width=15,
            height=20,
            corner_radius=10,
            progress_color="#8FBC8F",
            orientation="vertical",
            **kwargs

        )
