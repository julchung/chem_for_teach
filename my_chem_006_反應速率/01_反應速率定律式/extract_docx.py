import docx
import glob

files = glob.glob('*.docx')
if not files:
    print("No docx found")
else:
    doc = docx.Document(files[0])
    text = '\n'.join([p.text for p in doc.paragraphs if p.text.strip() != ''])
    with open('extracted.txt', 'w', encoding='utf-8') as f:
        f.write(text)
