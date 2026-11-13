from __future__ import annotations

from pathlib import Path

from agno.tools import Toolkit
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.tools.shell import ShellTools

cwd = Path(__file__).parent.resolve()
tmp_dir = cwd.joinpath("tmp")
tmp_dir.mkdir(exist_ok=True, parents=True)


def get_toolkit(tool_name: str) -> Toolkit | None:
    if tool_name == "ddg_search":
        return DuckDuckGoTools(fixed_max_results=3)
    elif tool_name == "shell_tools":
        return ShellTools()
    elif tool_name == "file_tools":
        return FileTools(base_dir=cwd)

    return None
