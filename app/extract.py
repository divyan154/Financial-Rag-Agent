# src/extract_html.py
from bs4 import BeautifulSoup
from pathlib import Path
import re


KEEP_TAGS = {
    "p",
    "div",
    "span",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "table",
    "tr",
    "td",
    "li",
}
ITEM_PAT = re.compile(r"^\s*Item\s+(\d+A?)([:\.\s-]|$)", re.IGNORECASE)


def extract_blocks_from_html(path):
    """
    Returns list of dicts: { 'file', 'block_id', 'tag', 'text', 'html' }
    """
    path = Path(path)
    raw = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "lxml")

    # remove scripts, style, nav, comments
    for t in soup(["script", "style", "noscript", "header", "footer", "nav", "iframe"]):
        t.decompose()

    blocks = []
    blk_id = 0
    # iterate through top-level block-ish elements (keep tag order)
    for el in soup.find_all(list(KEEP_TAGS)):
        text = el.get_text(separator=" ", strip=True)
        if not text:
            continue
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)
        blocks.append(
            {
                "file": path.name,
                "block_id": blk_id,
                "tag": el.name,
                "text": text,
                "html": str(el)[:2000],  # keep first 2k chars of raw HTML if needed
            }
        )
        blk_id += 1

    return blocks


def sectionize_blocks(blocks):
    """
    Input: list of block dicts from extract_blocks_from_html
    Output: list of sections: {file, section_name, blocks: [block_ids], text}
    """
    sections = []
    current = {"section_name": "preface", "blocks": []}
    for b in blocks:
        txt = b["text"]
        # If block looks like an "Item X" heading
        m = ITEM_PAT.match(txt)
        if m:
            # push previous
            if current["blocks"]:
                current["text"] = " ".join(current_blocks_text)
                sections.append(current)
            sec_name = f"Item {m.group(1).upper()}"
            current = {"section_name": sec_name, "blocks": [], "file": b["file"]}
            current_blocks_text = []
            continue
        # add block to current
        current["blocks"].append(b["block_id"])
        # maintain text buffer
        if "current_blocks_text" in locals():
            current_blocks_text.append(txt)
        else:
            current_blocks_text = [txt]
    # push last
    if current["blocks"]:
        current["text"] = " ".join(current_blocks_text)
        sections.append(current)
    return sections


# example
if __name__ == "__main__":
    import json

    blocks = extract_blocks_from_html("data/MSFT-2023.htm")
    # print(f"Extracted {len(blocks)} blocks")
    # print(blocks[0])
    sections = sectionize_blocks(blocks)
    print(f"Extracted {len(sections)} sections")
    print(sectionize_blocks(blocks)[1])
