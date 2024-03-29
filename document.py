# document.py
import os
from pathlib import Path
from base import validate_requirement
def generate_html(
        package: str,
        destination: str = None,
        reload: bool = False,
        show: bool = False
) -> None:
    """
    Generates the documentation for the package.
    :param reload: The value to rewrite the documentation.
    :param show: The value to show the documentation.
    :param package: The package to document.
    :param destination: The documentation destination.
    """
    validate_requirement("pdoc", path="pdoc3")
    from pdoc.cli import main as document, parser
    if destination is None:
        destination = "docs"
    main_index_file = Path(destination) / Path(package) / Path("index.html")
    if reload or not main_index_file.is_dir():
        document(
            parser.parse_args(
                [
                    "--html", "--force", "--output-dir",
                    str(destination), str(package)
                ]
            )
        )
    if show:
        os.system(f'start {main_index_file}')
