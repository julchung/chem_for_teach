import urllib.request
import json
import base64
import os
import glob
import time

IMG_DIR = "/Users/julchung/Library/CloudStorage/OneDrive-國立新化高級工業職業學校/玩具檔案/my_化學網/my_chem_004_原子結構/01_原子結構發展近代史"
OUTPUT_FILE = os.path.join(IMG_DIR, "extracted_questions.json")

png_files = sorted(glob.glob(os.path.join(IMG_DIR, "螢幕擷取畫面 *.png")))
print(f"Found {len(png_files)} images to process:")
for f in png_files:
    print(os.path.basename(f))

results = {}
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except:
        results = {}

prompt = """你是一位高階化學教師兼視覺文字分析專家。請詳細辨識這張試題圖片中的所有內容，並輸出格式化結構：
1. 題目類型與主題（例如：陰極射線、荷質比、密立坎油滴、拉塞福散射、同位素計算、莫斯利等）
2. 題目完整文字（保留所有化學符號、上下標、數字、公式）
3. 選項內容（(A), (B), (C), (D), (E) 等）
4. 正確答案（例如 (A), (B)...）
5. 詳細解析與計算步驟

請儘可能精確、嚴謹。
"""

for img_path in png_files:
    fname = os.path.basename(img_path)
    if fname in results and "content" in results[fname]:
        print(f"Already processed: {fname}")
        continue

    print(f"\nProcessing {fname} with qwen2.5vl:32b...")
    t0 = time.time()
    with open(img_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')

    payload = {
        'model': 'qwen2.5vl:32b',
        'messages': [
            {
                'role': 'user',
                'content': prompt,
                'images': [b64]
            }
        ],
        'options': {
            'num_ctx': 4096
        },
        'stream': False
    }

    req = urllib.request.Request(
        'http://localhost:11434/api/chat',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            content = data['message']['content']
            results[fname] = {
                'filename': fname,
                'content': content,
                'elapsed': time.time() - t0
            }
            print(f"Done in {time.time()-t0:.1f}s")
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error on {fname}: {e}")

print("\nAll done! Total processed:", len(results))
