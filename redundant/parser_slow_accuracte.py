from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc.labels import DocItemLabel
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend 

# 1. Setup fast, ultra-low memory pipeline options using strictly valid fields
pipeline_options = PdfPipelineOptions()

pipeline_options.do_ocr = False                 # Valid
pipeline_options.do_table_structure = False     # Valid
pipeline_options.force_backend_text = True      # Valid
pipeline_options.generate_page_images = False   # Valid
pipeline_options.generate_picture_images = False # Valid (Stops image cropping layout loops)
pipeline_options.enable_remote_services = False  # Valid (Prevents fallback network pings)

# 2. Tie the backend AND the options together inside format_options
options_by_format = {
    InputFormat.PDF: PdfFormatOption(
        pipeline_options=pipeline_options, 
        backend=PyPdfiumDocumentBackend
    )
}

# 3. Create converter
converter = DocumentConverter(
    allowed_formats=[InputFormat.PDF],
    format_options=options_by_format
)

# 4. Drag & drop file path input
file_path = input("📄 Drag & drop your PDF here and press Enter:\n").strip()
file_path = file_path.strip('"').strip("'")

# 5. Convert PDF safely (Only once!)
try:
    result = converter.convert(file_path)
    doc = result.document

    print("\n\n===== DOCUMENT OUTPUT =====\n")

    for element, _level in doc.iterate_items():
        if element.label == DocItemLabel.SECTION_HEADER:
            print(f"\n🔷 HEADING: {element.text}")
            print("-" * 50)
        elif element.label == DocItemLabel.PARAGRAPH:
            print(f"  📝 {element.text}")
        elif element.label == DocItemLabel.LIST_ITEM:
            print(f"  • {element.text}")

    print("\n\n===== DONE =====")

except Exception as e:
    print(f"❌ Extraction failed: {e}")