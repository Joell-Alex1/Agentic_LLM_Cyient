import re
import fitz  # PyMuPDF

file_path = input("📄 Drag & drop your PDF here and press Enter:\n").strip().strip('"').strip("'")

def clean_text_block(text):
    """Cleans up line breaks within a single paragraph and removes noise."""
    # Replace single newlines with spaces, but keep double newlines
    text = re.sub(re.compile(r'(?<!\n)\n(?!\n)'), ' ', text)
    # Clean up multiple spaces
    text = re.compile(r' {2,}').sub(' ', text)
    return text.strip()

try:
    print("\n⚡ Running high-speed structured extraction...")
    doc = fitz.open(file_path)
    
    print("\n\n===== DOCUMENT OUTPUT =====\n")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Use "dict" to grab actual font sizes and visual flags for flawless layout parsing
        text_page = page.get_text("dict")
        
        for block in text_page["blocks"]:
            if "lines" not in block:
                continue
                
            block_text = ""
            is_header = False
            is_list = False
            
            # Combine lines inside the block to check styling
            for line in block["lines"]:
                for span in line["spans"]:
                    # Skip repeating license/copyright noise
                    if "Licensed to" in span["text"] or "ISO Store" in span["text"] or "Single user licence" in span["text"]:
                        continue
                    if "© ISO 2015" in span["text"] or span["text"].strip().isdigit():
                        continue
                        
                    block_text += span["text"] + " "
                    
                    # Heuristic: Large or bold text at the start of a block signals a true heading
                    if span["size"] >= 11 or (span["flags"] & 4):  # Bold flag is usually 4
                        is_header = True

            cleaned_text = clean_text_block(block_text)
            if not cleaned_text:
                continue

            # --- STRUCTURAL ROUTING FOR VECTORLESS RAG ---
            
            # Catch true ISO Main Clauses and sub-clauses (e.g., "8.4", "8.4.1", "1 Scope")
            is_true_clause = re.match(r'^([1-10]\d?(\.\d+)*)\s+[A-Z]', cleaned_text)
            
            if is_true_clause or (is_header and len(cleaned_text) < 100 and not cleaned_text.startswith(('a)', 'b)', 'c)', 'd)', '1)', '2)'))):
                print(f"\n🔷 HEADING: {cleaned_text}")
                print("-" * 50)
                
            # Catch list components properly without making them headings
            elif cleaned_text.startswith(('a)', 'b)', 'c)', 'd)', 'e)', 'f)', '•', '-', '1)', '2)', '3)')):
                print(f"  • {cleaned_text}")
                
            # Standard unified paragraph text
            else:
                print(f"  📝 {cleaned_text}")
                
    print("\n\n===== DONE =====")

except Exception as e:
    print(f"❌ Extraction failed: {e}")