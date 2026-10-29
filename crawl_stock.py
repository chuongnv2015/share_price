import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def crawl_stock_prices():
    # Danh sách các mã cổ phiếu bạn muốn theo dõi (Ví dụ: VCB, FPT, HPG, PVI...)
    symbols = ["VCB", "FPT", "HPG", "PVI"]
    
    data = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": {}
    }

    for symbol in symbols:
        try:
            # Ví dụ lấy dữ liệu từ trang Cafef cho từng mã cổ phiếu
            url = f"https://s.cafef.vn/hastc/{symbol}-chi-tiet-giao-dich.chn" # Hoặc đường dẫn API nội bộ của Cafef
            # Hoặc bạn có thể dùng các API công khai dạng JSON của Cafef:
            api_url = f"https://cafef.vn/du-lieu/tra-cuu-bang-gia.chn?symbol={symbol}"
            
            # (Hoặc dùng thư viện yfinance nếu cổ phiếu quốc tế / có niêm yết)
            
            # Giả lập dữ liệu mẫu hoặc parse từ HTML CafeF/SSI
            # ... đoạn code parse BeautifulSoup tùy chỉnh theo cấu trúc trang ...
            
        except Exception as e:
            print(f"Lỗi khi lấy mã {symbol}: {e}")

    # Lưu ra file stock-prices.json để trang HTML fetch()
    with open("stock-prices.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    crawl_stock_prices()