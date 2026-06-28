import os
import winsound

from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

from core.config import load_config

BASER_DIR: Path = Path(__file__).resolve().parents[2]
UPLOAD_ICON = Path(BASER_DIR / "resources" / "assets" / "icons" / "upload.ico")


class Result(ctk.CTkTextbox):

    def __init__(self, master, **kwargs) -> None:

        config: dict[str, dict[str, int | str]] = load_config("result")
        self.textbox_config = config["textbox"].copy()

        super().__init__(

            master,
            **self.textbox_config,
            **kwargs,

        )

        self.configure(state="disabled")

        self.grid(

            column=1,
            row=0,
            rowspan=10,
            padx=(25, 15),
            pady=(15, 0),
            sticky="n",

        )

        self.upload_binary(self)

    def upload_binary(self, frame: ctk.CTkFrame) -> None:

        TkinterDnD._require(frame)

        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.drop)

        upload_container = ctk.CTkFrame(frame, fg_color="transparent")
        upload_container.place(relx=0.5, rely=0.5, anchor="center")

        upload_icon = ctk.CTkImage(Image.open(UPLOAD_ICON), size=(50, 50))

        upload_label = ctk.CTkLabel(

            upload_container,
            text="Please upload your binary.",
            image=upload_icon,
            compound="left",
            padx=10,
            font=("Calibri", 18, "bold"),

        )

        upload_label.pack()

    def drop(self, event) -> None:

        file_path = event.data.strip("{}")
        object_path = Path(file_path)

        if object_path.is_dir():

            binaries = []

            for root, _, files in os.walk(object_path):

                for file in files:

                    if file.endswith(".exe"):

                        binaries.append(os.path.join(root, file))

            if not binaries:

                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                messagebox.showwarning(

                    title="CyberShield - Upload :",
                    message="Please upload a directory containing binaries !"

                )

        elif object_path.is_file():

            if file_path.endswith(".exe"):

                pass

            if not file_path.endswith(".exe"):

                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                messagebox.showwarning(

                    title="CyberShield - Upload :",
                    message="Please upload only binaries and no other file types !"
                    
                )

    def display_result(self, text: str) -> None:

        self.configure(state="normal")
        self.insert("end", text)
        self.configure(state="disabled")

    def clear_result(self) -> None:

        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")
