import json
from datetime import datetime
import requests

def crawl_stock_prices():
    symbols = ["PVI", "FPT", "VCB", "HPG", "REE", "QTP"]
    
    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": {}
    }

    # Sử dụng API lấy giá trực tiếp của FireAnt
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://fireant.vn/"
    }

    for symbol in symbols:
        try:
            # API lấy quote giá cơ bản của FireAnt
            url = f"https://restapi.fireant.vn/symbols/quote/{symbol}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                item = response.json()
                if item and "lastPrice" in item:
                    current_price = item.get("lastPrice", 0) * 1000 # FireAnt tính theo nghìn đồng
                    change = item.get("priceChange", 0) * 1000
                    change_percent = item.get("percentChange", 0)
                    
                    data["stocks"][symbol] = {
                        "price": current_price,
                        "change": change,
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