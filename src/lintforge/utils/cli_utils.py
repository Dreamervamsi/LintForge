from typing import Annotated
from pathlib import Path
import typer

def get_folder_option(option:str, description:str):
    return Annotated[
        Path,
        typer.Option(
            option,
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            help=description
        )
    ]