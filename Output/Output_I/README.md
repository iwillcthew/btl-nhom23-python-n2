# Output Phần I - Thu thập dữ liệu cầu thủ

Thư mục này chứa kết quả thu thập dữ liệu từ Phần I của bài tập.

## Files

### 1. football_stats.db
**SQLite Database chứa toàn bộ dữ liệu**

#### Bảng `players`
- **Số cột**: 60+
- **Số dòng**: ~380-400 cầu thủ (có số phút > 90)
- **Nội dung**: Tất cả chỉ số thống kê từ fbref.com
- **Khóa chính**: id (auto-increment)

Các nhóm chỉ số:
- Thông tin cơ bản: Name, Nation, Team, Position, Age
- Thời gian: Matches_Played, Starts, Minutes
- Tấn công: Goals, Assists, xG, xAG
- Chuyền bóng: Passes_Completed, Pass_Completion_Pct, Key_Passes
- Sút: SoT_Pct, Goals_Per_Shot, Avg_Shot_Distance
- Thủ môn: GA90, Save_Pct, CS_Pct
- Phòng thủ: Tackles, Blocks, Interceptions
- Kiểm soát: Touches, Carries, Take_Ons_Success_Pct
- Khác: Fouls, Aerials_Won, SCA, GCA

#### Bảng `player_transfers`
- **Số cột**: 8
- **Số dòng**: ~380-400 cầu thủ (tương ứng với bảng players)
- **Nội dung**: Giá chuyển nhượng từ footballtransfers.com
- **Khóa ngoại**: player_id → players(id)

Các cột:
- id: Khóa chính
- player_id: Liên kết với bảng players
- player_name: Tên cầu thủ
- team: Câu lạc bộ
- transfer_value: Giá trị (ví dụ: €50M, £25.6M)
- currency: Đơn vị tiền tệ (EUR, GBP, USD)
- source: footballtransfers.com
- updated_date: Ngày thu thập

### 2. players_stats.csv
**File CSV chứa dữ liệu thống kê cầu thủ**

- **Định dạng**: CSV với header
- **Encoding**: UTF-8
- **Số cột**: 60+
- **Nội dung**: Tương tự bảng `players` trong database

**Cách sử dụng**:
```python
import pandas as pd
df = pd.read_csv('players_stats.csv')
print(df.head())
```

Hoặc mở bằng Excel/Google Sheets.

### 3. player_transfers.csv
**File CSV chứa giá chuyển nhượng**

- **Định dạng**: CSV với header
- **Encoding**: UTF-8
- **Số cột**: 7
- **Nội dung**: Tương tự bảng `player_transfers` trong database

**Cách sử dụng**:
```python
import pandas as pd
df = pd.read_csv('player_transfers.csv')
print(df.head())

# Kết hợp với players_stats.csv
players = pd.read_csv('players_stats.csv')
transfers = pd.read_csv('player_transfers.csv')
merged = pd.merge(players, transfers, left_on='Name', right_on='player_name')
```

## Truy vấn SQL

### Ví dụ truy vấn bảng players
```sql
-- Top 10 cầu thủ ghi nhiều bàn nhất
SELECT Name, Team, Goals, Minutes
FROM players
ORDER BY CAST(Goals AS INTEGER) DESC
LIMIT 10;

-- Thống kê theo đội
SELECT Team, 
       COUNT(*) as num_players,
       AVG(CAST(Goals AS REAL)) as avg_goals,
       AVG(CAST(Assists AS REAL)) as avg_assists
FROM players
GROUP BY Team
ORDER BY avg_goals DESC;
```

### Ví dụ truy vấn kết hợp 2 bảng
```sql
-- Top 10 cầu thủ có giá trị cao nhất
SELECT p.Name, p.Team, p.Goals, p.Assists, t.transfer_value
FROM players p
JOIN player_transfers t ON p.id = t.player_id
WHERE t.transfer_value != 'N/a'
ORDER BY t.transfer_value DESC
LIMIT 10;

-- Phân tích mối quan hệ giữa Goals và giá trị
SELECT p.Name, p.Goals, p.xG, t.transfer_value
FROM players p
JOIN player_transfers t ON p.id = t.player_id
WHERE t.transfer_value != 'N/a'
ORDER BY CAST(p.Goals AS INTEGER) DESC;
```

## Thống kê

### Dữ liệu thu thập
- **Tổng cầu thủ**: ~380-400
- **Tỷ lệ tìm thấy giá chuyển nhượng**: >90%
- **Số chỉ số thống kê**: 60+
- **Nguồn dữ liệu**: 
  - fbref.com (8 bảng thống kê)
  - footballtransfers.com (giá chuyển nhượng)

### Thời gian thu thập
- **Phần I.1** (fbref): ~10-15 phút
- **Phần I.2** (transfers): ~20-25 phút
- **Tổng**: ~30-40 phút

## Lưu ý

1. **Giá trị N/a**: 
   - Các chỉ số không áp dụng (ví dụ: GA90 cho cầu thủ ngoài)
   - Giá chuyển nhượng không tìm thấy (~10%)

2. **Định dạng số**:
   - Trong database và CSV: Dấu phẩy đã được loại bỏ
   - Có thể convert trực tiếp sang số: `CAST(Goals AS INTEGER)`

3. **Đơn vị tiền tệ**:
   - EUR (€): Hầu hết các cầu thủ
   - GBP (£): Một số cầu thủ Anh
   - USD ($): Rất ít

4. **Cập nhật dữ liệu**:
   - Chạy lại scraper để cập nhật
   - Dữ liệu cũ sẽ bị xóa và thay thế
