from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


root = Path(__file__).resolve().parents[3]
final_path = root / "docs" / "mini-ta" / "04-output" / "AKSARA_LAPORAN_FINAL.docx"

document = Document(str(final_path))
settings = document.settings.element
update_fields = settings.find(qn("w:updateFields"))
if update_fields is None:
    update_fields = OxmlElement("w:updateFields")
    settings.append(update_fields)
update_fields.set(qn("w:val"), "false")
document.save(str(final_path))

print(f"Finalized={final_path}")
