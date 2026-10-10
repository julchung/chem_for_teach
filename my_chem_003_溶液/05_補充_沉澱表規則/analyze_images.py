import urllib.request
import json
import base64
import os
import glob
import sys

target_dir = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_003_溶液/05_補充_沉澱表規則"
raw_results_path = os.path.join(target_dir, "ollama_vision_raw_results.json")

# 讀取既有結果（避免重跑）
if os.path.exists(raw_results_path):
    try:
        with open(raw_results_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception:
        results = {}
else:
    results = {}

png_files = sorted(glob.glob(os.path.join(target_dir, "螢幕擷取畫面*.png")))

prompt_text = """請詳細分析這張高中化學題目截圖：
1. 完整辨識題目題幹文字（包含所有化學式、離子符號與條件）
2. 完整辨識所有選項 (A)(B)(C)(D)(E)
3. 判定正確答案，並提供詳細的解題步驟、化學反應方程式、沉澱規則判斷依據與分析說明。
請使用繁體中文輸出。"""

for png in png_files:
    fname = os.path.basename(png)
    if fname in results and len(results[fname].strip()) > 30:
        print(f"Skipping {fname}, already analyzed.")
        continue

    print(f"Analyzing {fname} with qwen2.5vl:32b...")
    with open(png, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": "qwen2.5vl:32b",
        "prompt": prompt_text,
        "stream": False,
        "images": [img_b64]
    }

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            answer_text = data.get("response", "")
            results[fname] = answer_text
            print(f"Done {fname} ({len(answer_text)} chars)")
            with open(raw_results_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error analyzing {fname}: {e}")

print("All analysis completed!")
