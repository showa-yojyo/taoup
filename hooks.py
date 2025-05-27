"""
A custom hook module for MkDocs.

Reference:
不自然な空白が表示される <https://sphinx-users.jp/reverse-dict/html/japanese.html>
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mkdocs.config.base import Config
    from mkdocs.structure.pages import Page
    from mkdocs.structure.files import Files

# CJK newline CJK
UNWANTED_SPACES_PATTERN = re.compile(r"([^\s!-~])\n([^\s!-~])", flags=re.MULTILINE)


def on_page_markdown(
    md: str,
    page: Page,
    config: Config,
    files: Files,
) -> str | None:
    """The `page_markdown` event is called after the page's markdown is loaded from file
    and can be used to alter the Markdown source text.

    See <https://www.mkdocs.org/dev-guide/plugins/#on_page_markdown>.
    """

    # CJK-0 newline CJK-1 -> CJK-0 CJK-1
    return UNWANTED_SPACES_PATTERN.sub(r"\1\2", md)
