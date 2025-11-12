# Bài Tập Lớn Python - Phần I

## Mô tả

Thu thập dữ liệu cầu thủ Ngoại hạng Anh mùa 2024-2025 từ:
- fbref.com: Thống kê chi tiết cầu thủ (60+ chỉ số)
- footballtransfers.com: Giá chuyển nhượng ước tính

## Cấu trúc thư mục

```
Code/
  ├── config.py              # Cấu hình URL, bảng, database
  ├── scraper_fbref.py       # Thu thập dữ liệu từ fbref.com (I.1)
  ├── scraper_transfers.py   # Thu thập giá chuyển nhượng (I.2)
  └── README.md              # File này

Output/
  └── Output_I/
      └── football_stats.db  # Database SQLite (tự động tạo)

Report/
  └── main.tex               # Báo cáo LaTeX
```

## Yêu cầu cài đặt

### Thư viện Python cần thiết

```bash
pip install selenium beautifulsoup4
```

### Edge Browser

- Code sử dụng Microsoft Edge (có sẵn trên Windows)
- Edge WebDriver được cài tự động cùng Edge
- Đảm bảo Edge đã được cập nhật lên phiên bản mới nhất

## Cách sử dụng

### Bước 1: Thu thập dữ liệu cầu thủ (I.1)

```bash
cd Main/Code
python scraper_fbref.py
```

Kết quả:
- Database: `../Output/Output_I/football_stats.db`
- CSV File: `../Output/Output_I/players_stats.csv`
- Bảng: `players` (chứa tất cả thống kê cầu thủ)
- Điều kiện: Cầu thủ có số phút > 90
- Thời gian: ~10-15 phút

### Bước 2: Thu thập giá chuyển nhượng (I.2)

```bash
python scraper_transfers.py
```

Kết quả:
- Database: `../Output/Output_I/football_stats.db`
- CSV File: `../Output/Output_I/player_transfers.csv`
- Bảng: `player_transfers` (trong cùng database)
- Liên kết với bảng `players` qua `player_id`
- Thời gian: ~20-25 phút (3-4 giây/cầu thủ, do có 2 phương pháp)
- Tỷ lệ thành công: >90%

## File Output

### CSV Files

1. **players_stats.csv**
   - Chứa toàn bộ dữ liệu thống kê cầu thủ (60+ cột)
   - Định dạng: Name, Team, Position, Goals, Assists, xG, ...
   - Dễ mở bằng Excel/Google Sheets

2. **player_transfers.csv**
   - Chứa giá chuyển nhượng của cầu thủ (7 cột)
   - Định dạng: player_id, player_name, team, transfer_value, currency, source, updated_date
   - Có thể kết hợp với players_stats.csv qua player_id

### Database SQLite

- File: `football_stats.db`
- 2 bảng: `players` và `player_transfers`
- Có thể JOIN để phân tích mối quan hệ giữa thống kê và giá trị

## Cấu trúc Database

### Bảng `players`

Chứa các cột:
- Name, Nation, Team, Position, Age
- Matches_Played, Starts, Minutes
- Goals, Assists, Yellow_Cards, Red_Cards
- xG, xAG, Goals_Per90, Assists_Per90
- Passes_Completed, Pass_Completion_Pct
- SoT_Pct, Goals_Per_Shot
- GA90, Save_Pct (thủ môn)
- Tackles, Blocks, Interceptions
- Touches, Carries, Take_Ons_Success_Pct
- Fouls, Aerials_Won, Ball_Recoveries
- SCA, GCA
- Và nhiều chỉ số khác...

**Tổng cộng:** 60+ chỉ số thống kê

### Bảng `player_transfers`

Chứa các cột:
- player_id (khóa ngoại đến bảng players)
- player_name, team
- transfer_value (giá chuyển nhượng, ví dụ: "€25.6M")
- currency (đơn vị: EUR, GBP, USD)
- source (nguồn: footballtransfers.com)
- updated_date (ngày cập nhật)

## Xử lý vấn đề Rate-limit & Bot Detection

### Rate-limit

- Sử dụng `time.sleep(2-3)` giữa các requests
- Hiển thị tiến độ mỗi 10 cầu thủ
- Nếu bị chặn, tăng thời gian sleep lên 5 giây

### Bot Detection

Code đã được tối ưu để tránh bị phát hiện:
```python
edge_options.add_argument('--disable-blink-features=AutomationControlled')
edge_options.add_argument('--log-level=3')
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
edge_options.add_argument('user-agent=Mozilla/5.0...')
```

### Phương pháp thu thập giá trị chuyển nhượng

Chương trình lấy giá trị **ETV (Estimated Transfer Value) tại tháng 04/2025** - trong mùa giải 2024-2025 - từ biểu đồ lịch sử giá trị trên trang cầu thủ.

### Cách lấy ETV mùa 2024-2025

1. **Tìm biểu đồ**: Tìm `<div class="player-graph">` có thuộc tính `data-base64`
2. **Decode base64**: Chuyển chuỗi base64 thành JSON
3. **Trích xuất dataset**: Trong JSON, tìm dataset có `order=2` (ETV estimate)
4. **Lấy giá trị**: Tìm điểm có `x="04-'25"` và lấy trường `price`

**Ví dụ cấu trúc JSON:**
```json
{
  "dataSets": [
    {...},  // Dataset 0-1: bounds
    {       // Dataset 2: ETV estimate
      "order": 2,
      "data": [
        {"x": "04-'25", "price": "€44M"},  // <- Lấy giá trị này
        ...
      ]
    },
    ...
  ]
}
```

### 2 phương pháp tìm trang cầu thủ

### Phương pháp 1: Truy cập trực tiếp

1. **Tạo URL**: Chuyển tên cầu thủ thành format URL (lowercase, thay khoảng trắng = dấu gạch ngang)
   - Ví dụ: "Mohamed Salah" → "mohamed-salah"
   - URL: `https://www.footballtransfers.com/en/players/mohamed-salah`

2. **Trích xuất giá trị**: 
   - Ưu tiên: Lấy từ base64 data (ETV tháng 04/2025)
   - Fallback: Lấy từ `<div class="player-value player-value-large">`

### Phương pháp 2: Tìm kiếm và truy cập chi tiết (fallback)

Nếu phương pháp 1 không tìm thấy (tên không khớp URL):

1. **Sử dụng search**: `https://www.footballtransfers.com/en/search?search_value=Ten+Cau+Thu`
2. **Lấy link cầu thủ đầu tiên**:
   - Tìm thẻ `<div class="playerList-panel">`
   - Lấy href đầu tiên (ví dụ: `/en/players/ronald-araujo`)
3. **Truy cập trang chi tiết**:
   - Ghép thành URL đầy đủ
   - Trích xuất giá trị từ base64 data (ưu tiên) hoặc player-value-large

### Lý do thiết kế này

- **Đúng mùa giải**: Lấy ETV tháng 04/2025 đảm bảo giá trị thuộc mùa 2024-2025
- **Tên không chuẩn**: "Alisson" → "alisson-4", "Carlos Alcaraz" → "carlos-jonas-alcaraz"
- **Tên có dấu**: Tiếng Tây Ban Nha, Bồ Đào Nha không khớp URL
- **Fallback nhiều tầng**: base64 data → player-value-large → search → N/a

**Tỷ lệ thành công**: >90%

## Xem kết quả

### Sử dụng SQLite Browser

```bash
sqlite3 ../Output/Output_I/football_stats.db
```

### Truy vấn mẫu

```sql
-- Xem 10 cầu thủ đầu tiên
SELECT * FROM players LIMIT 10;

-- Xem giá chuyển nhượng
SELECT * FROM player_transfers LIMIT 10;

-- Top 10 cầu thủ ghi bàn nhiều nhất
SELECT Name, Team, Goals, Minutes 
FROM players 
ORDER BY CAST(Goals AS INTEGER) DESC 
LIMIT 10;

-- Kết hợp 2 bảng: Cầu thủ + giá trị
SELECT p.Name, p.Team, p.Goals, t.transfer_value
FROM players p
LEFT JOIN player_transfers t ON p.id = t.player_id
ORDER BY CAST(p.Goals AS INTEGER) DESC
LIMIT 10;
```

### Sử dụng Python

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('../Output/Output_I/football_stats.db')

# Đọc bảng players
df_players = pd.read_sql_query("SELECT * FROM players", conn)
print(df_players.head())

# Đọc bảng transfers
df_transfers = pd.read_sql_query("SELECT * FROM player_transfers", conn)
print(df_transfers.head())

conn.close()
```

## Lưu ý

1. **Edge Browser**: Code sử dụng Edge, không cần cài ChromeDriver

2. **Dữ liệu thiếu**: 
   - Một số chỉ số thống kê là "N/a" (không áp dụng cho vị trí đó)
   - Giá chuyển nhượng "N/a" rất hiếm (<10%) nhờ phương pháp kết hợp

3. **Kết quả thực tế**:
   - Đã thu thập: 381 cầu thủ
   - Tỷ lệ tìm thấy giá: >90%
   - Code: ~180 dòng

4. **Mở rộng**:
   - Có thể thay đổi `MIN_MINUTES` trong config.py
   - Có thể thêm các bảng thống kê khác trong TABLES

## Xử lý lỗi thường gặp

### Lỗi "NoSuchDriverException"

**Giải pháp:** Cập nhật Edge lên phiên bản mới nhất

### Connection reset / Timeout

**Giải pháp:** 
- Kiểm tra kết nối internet
- Tăng thời gian sleep
- Chạy lại script

### Không tìm thấy giá trị chuyển nhượng

**Nguyên nhân:**
- Cầu thủ không có trên website
- Tên không khớp chính xác
- Website thay đổi cấu trúc

**Giải pháp:** Dữ liệu sẽ được lưu là "N/a"
