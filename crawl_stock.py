import json
from datetime import datetime
import time
import requests

def crawl_stock_prices():
    symbols = ["PVI", "FPT", "VCB", "HPG", "REE", "QTP"]
    
    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": {}
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://iboard.ssi.com.vn/"
    }

    # Tạo mốc thời gian Unix timestamp cho 30 ngày qua đến hiện tại
    now = int(time.time())
    past = now - (30 * 24 * 60 * 60)

    for symbol in symbols:
        try:
            # Gọi API chuẩn của SSI iBoard kèm theo dải thời gian
            url = f"https://iboard.ssi.com.vn/dchart/api/history?resolution=1D&symbol={symbol}&from={past}&to={now}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                res_data = response.json()
                if "c" in res_data and len(res_data["c"]) > 0:
                    current_price = res_data["c"][-1] # Giá phiên gần nhất (tính bằng nghìn đồng)
                    prev_close = res_data["c"][-2] if len(res_data["c"]) > 1 else current_price
                    change = round(current_price - prev_close, 2)
                    change_percent = round((change / prev_close) * 100, 2) if prev_close else 0
                    
                    data["stocks"][symbol] = {
                        "price": current_price * 1000, # Quy đổi ra VNĐ (ví dụ: 65.5 -> 65500)
                        "change": change * 1000,
                        "change_percent": change_percent
                    }
                    continue
            
            data["stocks"][symbol] = {"price": 0, "change": 0, "change_percent": 0}
        except Exception as e:
            print(f"Lỗi khi lấy mã {symbol}: {e}")
            data["stocks"][symbol] = {"price": 0, "change": 0, "change_percent": 0}

    with open("stock-prices.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Đã cập nhật file stock-prices.json thành công!")

if __name__ == "__main__":
    crawl_stock_prices()