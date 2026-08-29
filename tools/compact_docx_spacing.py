from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile
import xml.etree.ElementTree as ET


NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{NS_W}}}"


def has_manual_page_break(paragraph: ET.Element) -> bool:
    for br in paragraph.findall(f".//{W}br"):
        if br.attrib.get(f"{W}type") == "page":
            return True
    return False


def is_empty_spacing_paragraph(paragraph: ET.Element) -> bool:
    if paragraph.find(f".//{W}drawing") is not None:
        return False
    if paragraph.find(f".//{W}pict") is not None:
        return False
    if paragraph.find(f".//{W}object") is not None:
        return False
    if paragraph.find(f".//{W}sectPr") is not None:
        return False
    if paragraph.find(f".//{W}fldChar") is not None:
        return False
    if paragraph.find(f".//{W}instrText") is not None:
        return False
    text = "".join(t.text or "" for t in paragraph.findall(f".//{W}t"))
    return text.strip() == ""


def compact_document_xml(xml_bytes: bytes) -> tuple[bytes, dict[str, int]]:
    ET.register_namespace("w", NS_W)
    root = ET.fromstring(xml_bytes)
    body = root.find(f"{W}body")
    if body is None:
        raise ValueError("word/document.xml does not contain w:body")

    removed_page_breaks = 0
    removed_blank_paragraphs = 0
    compact_children: list[ET.Element] = []
    previous_blank = False

    for child in list(body):
        if child.tag == f"{W}p" and has_manual_page_break(child):
            removed_page_breaks += 1
            previous_blank = False
            continue

        if child.tag == f"{W}p" and is_empty_spacing_paragraph(child):
            if previous_blank:
                removed_blank_paragraphs += 1
                continue
            previous_blank = True
            compact_children.append(child)
            continue

        previous_blank = False
        compact_children.append(child)

    body[:] = compact_children
    updated = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    return updated, {
        "removed_page_breaks": removed_page_breaks,
        "removed_blank_paragraphs": removed_blank_paragraphs,
    }


def compact_docx(path: Path) -> dict[str, int]:
    with ZipFile(path, "r") as zin:
        document_xml = zin.read("word/document.xml")
        updated_xml, stats = compact_document_xml(document_xml)
        entries = [(item, zin.read(item.filename)) for item in zin.infolist()]

    with NamedTemporaryFile(delete=False, suffix=".docx", dir=str(path.parent)) as tmp_file:
        tmp_path = Path(tmp_file.name)

    try:
        with ZipFile(tmp_path, "w", ZIP_DEFLATED) as zout:
            for item, data in entries:
                if item.filename == "word/document.xml":
                    data = updated_xml
                zout.writestr(item, data)
        tmp_path.replace(path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()
    return stats


def main() -> None:
    docs = sorted(Path("docs").glob("Smart_Sportz_Phase_*.docx"))
    if not docs:
        raise SystemExit("No phase DOCX files found.")

    for doc in docs:
        try:
            stats = compact_docx(doc)
            print(f"{doc}: removed page breaks={stats['removed_page_breaks']}, removed extra blanks={stats['removed_blank_paragraphs']}")
        except PermissionError:
            print(f"{doc}: skipped because the file is locked/open")


if __name__ == "__main__":
    main()
