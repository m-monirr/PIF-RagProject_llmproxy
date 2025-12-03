import logging
import time
from pathlib import Path
import pandas as pd
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TesseractCliOcrOptions
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.transforms.serializer.markdown import MarkdownDocSerializer
from .chunking import clean_markdown

def extract_from_pdf(input_pdf_path: Path, output_dir: Path):
    is_arabic = "AR" in input_pdf_path.name.upper()
    logging.basicConfig(level=logging.INFO)
    _log = logging.getLogger(__name__)

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.ocr_options = TesseractCliOcrOptions(
        force_full_page_ocr=True,
        lang=["ara"] if is_arabic else ["eng"]
    )
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.images_scale = 3.0
    pipeline_options.generate_page_images = True
    pipeline_options.generate_picture_images = True

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    start_time = time.time()
    conv_res = doc_converter.convert(input_pdf_path)
    doc = conv_res.document
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_filename = conv_res.input.file.stem

    image_dir = output_dir / "images"
    image_dir.mkdir(exist_ok=True)

    direction_tag = "dir='rtl'" if "AR" in doc_filename.upper() else ""

    serializer = MarkdownDocSerializer(doc=doc)
    ser_result = serializer.serialize()
    raw_md = ser_result.text

    cleaned_md = clean_markdown(raw_md)
    md_parts = [f"# Extracted Content from {doc_filename}\n", f"<div {direction_tag}>\n", cleaned_md, "</div>"]

    for i, table in enumerate(doc.tables):
        df = table.export_to_dataframe()
        df.to_csv(output_dir / f"{doc_filename}-table-{i+1}.csv", index=False)
        table_md = df.to_markdown(index=False)
        md_parts.append(f"\n\n## Table {i+1}\n")
        md_parts.append(table_md)
        img_name = f"{doc_filename}-table-img-{i+1}.png"
        img_path = image_dir / img_name
        table.get_image(doc).save(img_path, "PNG")

    for i, page in enumerate(doc.pages):
        if hasattr(page, "image") and page.image:
            page_img_name = f"{doc_filename.lower()}_page_{i+1}_img.png"
            page_img_path = image_dir / page_img_name
            page.image.save(page_img_path, "PNG")
        else:
            _log.warning(f"Skipping page {i+1} — no image found.")

    for i, picture in enumerate(getattr(doc, "pictures", [])):
        try:
            picture_name = f"{doc_filename.lower()}_picture_{i+1}.png"
            picture_path = image_dir / picture_name
            picture.get_image(doc).save(picture_path, "PNG")
        except Exception as e:
            _log.warning(f"Failed to save embedded image {i+1}: {e}")

    final_md = "\n".join(md_parts)
    (output_dir / f"{doc_filename}.md").write_text(final_md, encoding="utf-8")

    elapsed = time.time() - start_time
    _log.info(f"Extraction completed in {elapsed:.2f} seconds")

    return doc, doc_filename