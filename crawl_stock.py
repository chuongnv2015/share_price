import json
from datetime import datetime
import requests

def crawl_stock_prices():
    symbols = ["PVI", "FPT", "VCB", "HPG", "REE", "QTP"]
    
    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": {}
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://s.cafef.vn/"
    }

    for symbol in symbols:
        try:
            # Sử dụng API công khai lấy thông tin giá mới nhất của CafeF
            url = f"https://cafef.vn/du-lieu/tra-cuu-bang-gia.chn?symbol={symbol}"
            
            # Hoặc dùng API trực tiếp lấy giá nhanh qua dữ liệu tài chính
            api_url = f"https://einsight.cafef.vn/company/getquote?symbol={symbol}"
            
            response = requests.get(api_url, headers=headers, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                # Tùy theo cấu trúc JSON trả về của CafeF
                if "Data" in res_json and res_json["Data"]:
                    item = res_json["Data"]
                    current_price = item.get("CurrentPrice", 0) * 1000 # Thường giá đơn vị nghìn đồng
                    change = item.get("PriceChange", 0) * 1000
                    change_percent = item.get("PercentPriceChange", 0)
                    
                    data["stocks"][symbol] = {
                        "price": current_price,
                        "change": change,
                        "change_percent": change_percent
                    }
                    continue
            
            # Dự phòng nếu API phụ lỗi, gán giá trị mặc định để test
            data["stocks"][symbol] = {"price": 0, "change": 0, "change_percent": 0}
            
        except Exception as e:
            print(f"Lỗi khi lấy mã {symbol}: {e}")
            data["stocks"][symbol] = {"price": 0, "change": 0, "change_percent": 0}

    with open("stock-prices.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Đã cập nhật file stock-prices.json thành công!")

if __name__ == "__main__":
    crawl_stock_prices()