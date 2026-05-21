with open("scratch/extracted_content.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

keywords = ["電子親和力", "親和力", "EA", "Electron Affinity"]

with open("scratch/ea_search_output.txt", "w", encoding="utf-8") as out:
    out.write("=== Search Results and Context ===\n")
    for idx, line in enumerate(lines):
        if any(kw in line for kw in keywords):
            out.write(f"\n--- Match at Line {idx} ---\n")
            start = max(0, idx - 4)
            end = min(len(lines), idx + 5)
            for c_idx in range(start, end):
                prefix = ">>> " if c_idx == idx else "    "
                out.write(f"{prefix}Line {c_idx}: {lines[c_idx].strip()}\n")

print("Saved context output to scratch/ea_search_output.txt")
