import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Construct absolute path to index.html
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.join(current_dir, 'index.html')
        file_url = f"file:///{html_file_path.replace(chr(92), '/')}"
        
        await page.goto(file_url, wait_until='networkidle')
        
        # Save as PDF, format A4
        pdf_path = os.path.join(current_dir, '01_反應速率定律式_講義.pdf')
        await page.pdf(path=pdf_path, format='A4', margin={'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'}, print_background=True)
        
        print(f"Successfully converted to {pdf_path}")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
