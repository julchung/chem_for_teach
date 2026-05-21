# Read extracted_content.txt and write the segment around '電子親和力'
with open("scratch/extracted_content.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Write lines from 1350 to 1503 (or end) to a separate file for reading
segment = lines[1300:] # Page 50 is likely towards the end of this chapter
with open("scratch/ea_content.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(segment):
        out.write(f"Line {1300 + idx}: {line}")

print("Saved Electron Affinity segment to scratch/ea_content.txt")
