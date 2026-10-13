#!/usr/bin/env python3
"""
memory_guard.py
A quick health check and memory guard script for the workspace.
Checks free RAM, kills orphaned headless Chrome processes, and manages Ollama memory.
"""
import subprocess
import sys
import os

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""

def check_memory():
    print("=== [1] 系統記憶體狀況 ===")
    vm_stat = run("vm_stat")
    free_pages = 0
    speculative_pages = 0
    page_size = 16384
    for line in vm_stat.splitlines():
        if "Pages free:" in line:
            free_pages = int(line.split(":")[1].strip().rstrip("."))
        elif "Pages speculative:" in line:
            speculative_pages = int(line.split(":")[1].strip().rstrip("."))
    
    available_gb = ((free_pages + speculative_pages) * page_size) / (1024 ** 3)
    total_mem_gb = int(run("sysctl -n hw.memsize") or "0") / (1024 ** 3)
    print(f"實體總記憶體: {total_mem_gb:.1f} GB")
    print(f"當前可用記憶體: {available_gb:.1f} GB")
    
    if available_gb < 15:
        print("⚠️ 警告：可用記憶體低於 15 GB，若載入 32B 模型可能造成 Swap 換頁卡頓。")
    else:
        print(" 可用記憶體充足，可安全調用 32B 本地模型！")

def clean_orphaned_chrome():
    print("\n=== [2] 檢查背景殘留 Chrome 行程 ===")
    pids = run("pgrep -f 'Google Chrome for Testing'").split()
    if pids:
        print(f"發現殘留 Chrome 行程: {len(pids)} 個，正在強制清理...")
        run("pkill -9 -f 'Google Chrome for Testing'")
        print("✅ 已成功清理所有殘留 Chrome 行程！")
    else:
        print("✅ 目前沒有殘留的無頭 Chrome 行程。")

def check_ollama():
    print("\n=== [3] Ollama 本地模型狀態 ===")
    ollama_ps = run("ollama ps")
    if ollama_ps and len(ollama_ps.splitlines()) > 1:
        print("當前載入中的模型:")
        print(ollama_ps)
        if len(sys.argv) > 1 and sys.argv[1] == "--unload":
            lines = ollama_ps.splitlines()[1:]
            for line in lines:
                parts = line.split()
                if parts:
                    name = parts[0]
                    print(f"正在卸載模型: {name} ...")
                    run(f"ollama stop {name}")
            print("✅ 已卸載所有 Ollama 模型，釋放統一記憶體！")
    else:
        print("✅ 目前 Ollama 沒有常駐佔用記憶體的模型。")

if __name__ == "__main__":
    check_memory()
    clean_orphaned_chrome()
    check_ollama()
