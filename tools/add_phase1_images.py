from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile


DOCX = Path("docs/Smart_Sportz_Phase_1_Foundation.docx")
BACKUP = Path("docs/Smart_Sportz_Phase_1_Foundation.before_images.docx")
ASSETS = {
    "rIdPhase1Lifecycle": ("phase1_tournament_lifecycle.png", "Tournament Lifecycle Workflow", "Tournament lifecycle workflow diagram", "2. Project Overview"),
    "rIdPhase1Rbac": ("phase1_rbac_model.png", "Role-Based Access Control Model", "Role-based access control model diagram", "6. User Roles and RBAC"),
    "rIdPhase1Architecture": ("phase1_system_architecture.png", "High-Level System Architecture", "High-level system architecture diagram", "9. High-Level System Architecture"),
}

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}

for prefix, uri in NS.items():
    if prefix not in {"rel", "ct"}:
        ET.register_namespace(prefix, uri)


def q(prefix: str, local: str) -> str:
    return f"{{{NS[prefix]}}}{local}"


def paragraph_text(el: ET.Element) -> str:
    return "".join(t.text or "" for t in el.findall(".//w:t", NS)).strip()


def image_paragraph(rel_id: str, name: str, descr: str, doc_pr_id: int, width_in: float = 6.8) -> ET.Element:
    cx = int(width_in * 914400)
    cy = int((width_in / (1600 / 820)) * 914400)
    xml = f'''
<w:p xmlns:w="{NS["w"]}" xmlns:r="{NS["r"]}" xmlns:wp="{NS["wp"]}" xmlns:a="{NS["a"]}" xmlns:pic="{NS["pic"]}">
  <w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_pr_id}" name="{name}" descr="{descr}"/>
        <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr>
                <pic:cNvPr id="{doc_pr_id}" name="{name}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''
    return ET.fromstring(xml)


def strip_existing_phase1_images(body: ET.Element) -> None:
    for child in list(body):
        xml = ET.tostring(child, encoding="unicode")
        if "rIdPhase1Lifecycle" in xml or "rIdPhase1Rbac" in xml or "rIdPhase1Architecture" in xml:
            body.remove(child)


def patch_document(xml: bytes) -> bytes:
    root = ET.fromstring(xml)
    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("word/document.xml has no w:body")
    strip_existing_phase1_images(body)

    insertions = {
        heading: image_paragraph(rel_id, name, descr, i + 20)
        for i, (rel_id, (_file, name, descr, heading)) in enumerate(ASSETS.items(), start=1)
    }
    for child in list(body):
        text = paragraph_text(child)
        if text in insertions:
            idx = list(body).index(child)
            body.insert(idx + 1, insertions[text])
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_rels(xml: bytes) -> bytes:
    root = ET.fromstring(xml)
    existing = {el.attrib.get("Id") for el in root}
    for rel_id, (filename, _name, _descr, _heading) in ASSETS.items():
        if rel_id not in existing:
            ET.SubElement(root, "Relationship", {
                "Id": rel_id,
                "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
                "Target": f"media/{filename}",
            })
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_content_types(xml: bytes) -> bytes:
    root = ET.fromstring(xml)
    has_png = any(el.tag.endswith("Default") and el.attrib.get("Extension") == "png" for el in root)
    if not has_png:
        ET.SubElement(root, "Default", {"Extension": "png", "ContentType": "image/png"})
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main() -> None:
    if not DOCX.exists():
        raise FileNotFoundError(DOCX)
    for filename, *_rest in ASSETS.values():
        path = Path("docs/assets") / filename
        if not path.exists():
            raise FileNotFoundError(path)

    if not BACKUP.exists():
        shutil.copy2(DOCX, BACKUP)

    with TemporaryDirectory() as tmp:
        tmp_docx = Path(tmp) / DOCX.name
        with ZipFile(DOCX, "r") as zin, ZipFile(tmp_docx, "w", ZIP_DEFLATED) as zout:
            written = set()
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = patch_document(data)
                elif item.filename == "word/_rels/document.xml.rels":
                    data = patch_rels(data)
                elif item.filename == "[Content_Types].xml":
                    data = patch_content_types(data)
                zout.writestr(item, data)
                written.add(item.filename)
            for filename, *_rest in ASSETS.values():
                target = f"word/media/{filename}"
                if target not in written:
                    zout.write(Path("docs/assets") / filename, target)
        shutil.move(tmp_docx, DOCX)
    print(DOCX.resolve())


if __name__ == "__main__":
    main()
