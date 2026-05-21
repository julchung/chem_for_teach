import zipfile
import xml.etree.ElementTree as ET
import os

docx_path = r"選化二_第一章_原子結構2024.docx"
output_path = r"scratch/extracted_content.txt"

os.makedirs("scratch", exist_ok=True)

def extract_docx_text(path):
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }
    
    with zipfile.ZipFile(path) as docx:
        tree = ET.parse(docx.open('word/document.xml'))
        root = tree.getroot()
        
        paragraphs = []
        for paragraph in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = [node.text for node in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            if texts:
                paragraphs.append("".join(texts))
            else:
                paragraphs.append("") # representing empty line or table spacing
                
        return paragraphs

try:
    print("Extracting docx text...")
    lines = extract_docx_text(docx_path)
    print(f"Extracted {len(lines)} lines.")
    
    # Save the lines to a text file so we can view it
    with open(output_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
            
    print(f"Text successfully saved to {output_path}")
    
    # Search for keywords related to '電子親和力'
    keywords = ["電子親和力", "親和力", "EA", "Electron Affinity"]
    matches = []
    for idx, line in enumerate(lines):
        for kw in keywords:
            if kw in line:
                matches.append((idx, line))
                break
                
    print(f"Found {len(matches)} matches for keywords.")
    for idx, line in matches[:20]:
        print(f"Line {idx}: {line[:120]}")

except Exception as e:
    import traceback
    print("Error occurred:")
    traceback.print_exc()
