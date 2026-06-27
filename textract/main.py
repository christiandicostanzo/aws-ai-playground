import sys
from pathlib import Path
import boto3
import os
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import boto_client

client = boto_client.get_boto_client("textract")

def detect_text(image_bytes: bytes) -> list[str]:
    response = client.detect_document_text(Document={"Bytes": image_bytes})
    lines = [
        block["Text"]
        for block in response["Blocks"]
        if block["BlockType"] == "LINE"
    ]
    logger.info(f"Detected {len(lines)} lines of text")
    for line in lines:
        logger.debug(f"  {line}")
    return lines


def analyze_forms(image_bytes: bytes) -> dict[str, str]:
    response = client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["FORMS"],
    )
    blocks = {block["Id"]: block for block in response["Blocks"]}

    pairs: dict[str, str] = {}
    for block in response["Blocks"]:
        if block["BlockType"] != "KEY_VALUE_SET" or "KEY" not in block.get("EntityTypes", []):
            continue
        key_text = _get_text(block, blocks)
        value_block = _find_value_block(block, blocks)
        value_text = _get_text(value_block, blocks) if value_block else ""
        if key_text:
            pairs[key_text] = value_text

    logger.info(f"Detected {len(pairs)} form fields")
    for k, v in pairs.items():
        logger.debug(f"  {k!r}: {v!r}")
    return pairs


def analyze_tables(image_bytes: bytes) -> list[list[list[str]]]:
    response = client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["TABLES"],
    )
    blocks = {block["Id"]: block for block in response["Blocks"]}

    tables: list[list[list[str]]] = []
    for block in response["Blocks"]:
        if block["BlockType"] != "TABLE":
            continue
        rows: dict[int, dict[int, str]] = {}
        for rel in block.get("Relationships", []):
            if rel["Type"] != "CHILD":
                continue
            for cell_id in rel["Ids"]:
                cell = blocks.get(cell_id)
                if not cell or cell["BlockType"] != "CELL":
                    continue
                rows.setdefault(cell["RowIndex"], {})[cell["ColumnIndex"]] = _get_text(cell, blocks)
        table_data = [
            [rows[r].get(c, "") for c in sorted(rows[r])]
            for r in sorted(rows)
        ]
        tables.append(table_data)

    logger.info(f"Detected {len(tables)} table(s)")
    for i, table in enumerate(tables):
        logger.debug(f"Table {i + 1}:")
        for row in table:
            logger.debug(f"  {row}")
    return tables


def _find_value_block(key_block: dict, blocks: dict) -> dict | None:
    for rel in key_block.get("Relationships", []):
        if rel["Type"] == "VALUE":
            return blocks.get(rel["Ids"][0])
    return None


def _get_text(block: dict, blocks: dict) -> str:
    words: list[str] = []
    for rel in block.get("Relationships", []):
        if rel["Type"] != "CHILD":
            continue
        for child_id in rel["Ids"]:
            child = blocks.get(child_id)
            if child and child["BlockType"] == "WORD":
                words.append(child["Text"])
            elif child and child["BlockType"] == "SELECTION_ELEMENT":
                words.append("SELECTED" if child["SelectionStatus"] == "SELECTED" else "NOT_SELECTED")
    return " ".join(words)


def main() -> None:
    #\image_example.png , alias_cbu.png , cbu.png , cbu_alias.png
    file_path =  Path(os.path.dirname(os.path.abspath(__file__)) + "\\alias_cbu.png")
    
    if not file_path.exists(): 
        logger.error("Provide a path to an image file as an argument.")
        logger.info("Usage: uv run examples/textract/main.py <image_path>")
        logger.info("Supports: JPEG, PNG, TIFF (max 5 MB for synchronous API)")
        sys.exit(1)   
        
    image_bytes = file_path.read_bytes()
    logger.info(f"Processing {file_path} ({len(image_bytes):,} bytes)")

    logger.info("=== Text Detection ===")
    detect_text(image_bytes)
    logger.info("=== END Text Detection ===")

    #logger.info("=== Form Analysis ===")
    #analyze_forms(image_bytes)

    #logger.info("=== Table Extraction ===")
    #analyze_tables(image_bytes)


if __name__ == "__main__":
    main()
