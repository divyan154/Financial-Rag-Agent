# src/sectionize.py

ITEM_PAT = re.compile(r"^\s*Item\s+(\d+A?)([:\.\s-]|$)", re.IGNORECASE)


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

