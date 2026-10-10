import urllib.request, json, base64, glob, os, time

imgs = sorted(glob.glob('螢幕擷取畫面*.png'))
output_file = 'extracted_questions.json'

results = {}
if os.path.exists(output_file):
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
    except Exception as e:
        print('Could not load existing results:', e)

print(f"Total images found: {len(imgs)}. Already processed: {len(results)}")

for idx, img_path in enumerate(imgs):
    if img_path in results and results[img_path].get('content'):
        print(f"[{idx+1}/{len(imgs)}] Skipping already processed: {img_path}")
        continue

    print(f"[{idx+1}/{len(imgs)}] Processing {img_path} with qwen2.5vl:32b...")
    try:
        with open(img_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')

        payload = {
            'model': 'qwen2.5vl:32b',
            'messages': [
                {
                    'role': 'user',
                    'content': '請分析這張圖片中的化學試題。請完整提取：\n1. 題目文字（含任何條件、單位、化學符號、數值）\n2. 所有選項 (A)(B)(C)(D)(E)\n3. 正確答案（若圖中有標記或勾選答案請指出，若無則依化學專業解答）\n4. 詳細解題步驟與化學觀念解析：',
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

        t0 = time.time()
        with urllib.request.urlopen(req, timeout=300) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            content = res['message']['content']
            elapsed = time.time() - t0
            print(f"  Done in {elapsed:.1f}s. Extracted {len(content)} chars.")
            results[img_path] = {
                'status': 'success',
                'elapsed': elapsed,
                'content': content
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"  Error processing {img_path}: {e}")
        results[img_path] = {
            'status': 'error',
            'error': str(e)
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

print("Batch analysis complete!")
