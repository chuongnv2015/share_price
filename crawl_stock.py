import json
from datetime import datetime
import requests

def crawl_stock_prices():
    # Danh sách các mã cổ phiếu bạn muốn theo dõi
    symbols = ["PVI", "FPT", "VCB", "HPG", "REE", "QTP"]
    
    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": {}
    }

    # Sử dụng API bảng giá công khai của SSI (hoặc các nguồn tương tự)
    # Hoặc cào trực tiếp qua API giá của CafeF / SSI iBoard
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    for symbol in symbols:
        try:
            # Gọi API lấy dữ liệu giá cổ phiếu từ SSI iBoard công khai
            url = f"https://iboard.ssi.com.vn/dchart/api/history?resolution=1&symbol={symbol}&from=0&to=9999999999"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                res_data = response.json()
                if "c" in res_data and len(res_data["c"]) > 0:
                    current_price = res_data["c"][-1] # Giá đóng cửa mới nhất
                    prev_close = res_data["c"][-2] if len(res_data["c"]) > 1 else current_price
                    change = current_price - prev_close
                    change_percent = (change / prev_close) * 100 if prev_close else 0
                    
                    data["stocks"][symbol] = {
                        "price": current_price,
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2)
                    }
                else:
                    data["stocks"][symbol] = {"price": "N/A", "change": 0, "change_percent": 0}
            else:
                data["stocks"][symbol] = {"price": "N/A", "change": 0, "change_percent": 0}
        except Exception as e:
            print(f"Lỗi khi lấy mã {symbol}: {e}")
            data["stocks"][symbol] = {"price": "N/A", "change": 0, "change_percent": 0}

    # Lưu ra file stock-prices.json
    with open("stock-prices.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Đã cập nhật file stock-prices.json thành công!")

if __name__ == "__main__":
    crawl_stock_prices()