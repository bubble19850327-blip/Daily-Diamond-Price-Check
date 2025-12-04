import requests
from bs4 import BeautifulSoup
import os
import sys

def send_line_notify(msg):
    # 從 GitHub Secrets 獲取 Token，若本地測試請直接替換字串
    token = os.environ.get('LINE_TOKEN')
    
    if not token:
        print("錯誤：找不到 LINE_TOKEN 環境變數")
        return

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload = {'message': msg}
    try:
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
        print(f"推播狀態: {r.status_code}")
    except Exception as e:
        print(f"推播失敗: {e}")

def get_diamond_price():
    # 設定目標網址 (以 GIA 鑽石網為例)
    url = "https://www.giadiamond.com.tw/price/diamond/1-carat"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 檢查連線狀態
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # --- 注意：此處需依網站實際 HTML 結構調整 CSS 選擇器 ---
        # 這裡假設抓取頁面標題或特定價格區塊作為範例
        # 實際使用請按 F12 檢查網頁元素，例如: price = soup.select_one('.price-class').text
        
        title = soup.title.string.strip() if soup.title else "未知標題"
        # 模擬抓取到的數據 (若您找到實際選擇器，請替換下方字串)
        result_text = f"\n【鑽石報價日報】\n來源: {title}\n連結: {url}\n(請修改程式碼中的選擇器以抓取精確價格)"
        
        return result_text

    except Exception as e:
        return f"\n爬蟲發生錯誤: {e}"

if __name__ == "__main__":
    print("開始執行鑽石報價爬蟲...")
    msg = get_diamond_price()
    send_line_notify(msg)
    print("執行結束")
