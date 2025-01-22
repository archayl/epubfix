import zipfile
import os
import tempfile
import shutil

def fix_epub_encoding(epub_path):
    """
    Fix character encoding issues in epub files.
    
    Args:
        epub_path (str): Path to the epub file to fix
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Create output filename
    base_name = os.path.splitext(epub_path)[0]
    output_path = f"{base_name}_fixed.epub"
    
    # Windows-1252 codepage mappings for 0x80-0x9F range
    replacements = {
        'â‚¬': '€',    # 0x80 EURO SIGN
        'â€ž': '„',    # 0x84 DOUBLE LOW-9 QUOTATION MARK
        'â€¦': '…',    # 0x85 HORIZONTAL ELLIPSIS
        'â€¡': '‡',    # 0x87 DOUBLE DAGGER
        'â€°': '‰',    # 0x89 PER MILLE SIGN
        'â€¹': '‹',    # 0x8B SINGLE LEFT-POINTING ANGLE QUOTATION MARK
        'â€˜': '‘',    # 0x91 LEFT SINGLE QUOTATION MARK
        'â€™': '’',    # 0x92 RIGHT SINGLE QUOTATION MARK
        'â€œ': '“',    # 0x93 LEFT DOUBLE QUOTATION MARK
        'â€¢': '•',    # 0x95 BULLET
        'â€“': '–',    # 0x96 EN DASH
        'â€”': '—',    # 0x97 EM DASH
        'â„¢': '™',    # 0x99 TRADE MARK SIGN
    }

    replacements2 = {
        'Æ’': '‚',     # 0x82 SINGLE LOW-9 QUOTATION MARK
        'â€' : '†',     # 0x86 DAGGER
        'Ë†': 'ˆ',     # 0x88 MODIFIER LETTER CIRCUMFLEX ACCENT
        'Å’': 'Œ',     # 0x8C LATIN CAPITAL LIGATURE OE
        'Å½': 'Ž',     # 0x8E LATIN CAPITAL LETTER Z WITH CARON
        'â€': '”',     # 0x94 RIGHT DOUBLE QUOTATION MARK
        'Ëœ': '˜',     # 0x98 SMALL TILDE
        'Å¡': 'š',     # 0x9A LATIN SMALL LETTER S WITH CARON
        'Å“': 'œ',     # 0x9C LATIN SMALL LIGATURE OE
        'Å¾': 'ž',     # 0x9E LATIN SMALL LETTER Z WITH CARON
        'Å¸': 'Ÿ',     # 0x9F LATIN CAPITAL LETTER Y WITH DIAERESIS
        # Additional common problematic characters
        'Ã©': 'é',     # e with acute
        'Ã¨': 'è',     # e with grave
    }

    replacements3 = {
        'Å': 'Š',      # 0x8A LATIN CAPITAL LETTER S WITH CARON
        # Additional common problematic characters
        'Â': '',       # Non-breaking space
        'Ã': 'à',      # a with grave
    }

    
    try:
        # Extract epub
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Process all files in the epub
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(('.html', '.xhtml', '.xml', '.css', '.opf')):
                    file_path = os.path.join(root, file)
                    
                    # Read the content
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        continue
                    
                    # Apply all replacements
                    for wrong, correct in replacements.items():
                        content = content.replace(wrong, correct)
                    
                    for wrong, correct in replacements2.items():
                        content = content.replace(wrong, correct)

                    for wrong, correct in replacements3.items():
                        content = content.replace(wrong, correct)

                    # Write the fixed content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
        
        # Create new epub with fixed content
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zip_ref.write(file_path, arcname)
        
        print(f"Fixed epub saved as: {output_path}")
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

# Example usage
if __name__ == "__main__":
    fix_epub_encoding("ebook.epub")
