# Code III - Phân tích thống kê theo đội

## Mô tả

Phần III của bài tập lớn: Phân tích thống kê mô tả cho dữ liệu cầu thủ theo từng đội.

## Mục tiêu

Tính toán các chỉ số thống kê mô tả cho mỗi metric của các cầu thủ trong từng đội:
- **Trung vị (Median)**: Giá trị ở giữa khi sắp xếp
- **Trung bình (Mean)**: Giá trị trung bình cộng
- **Độ lệch chuẩn (Standard Deviation)**: Độ phân tán của dữ liệu

## Files

### `team_statistics.py` - Chương trình phân tích chính

Chương trình Python sử dụng **NumPy** và **Pandas** để tính toán thống kê.

## Cài đặt

### Thư viện cần thiết

```bash
pip install pandas numpy
```

Hoặc cài từ file requirements:
```bash
pip install -r ../../requirements.txt
```

### Yêu cầu

- Python 3.7+
- Pandas 1.3.0+
- NumPy 1.20.0+
- File dữ liệu đầu vào: `Output/Output_I/players_stats.csv` (từ Code_I)

## Cách sử dụng

### Chạy chương trình

```bash
cd Code/Code_III
python team_statistics.py
```

### Output

Chương trình sẽ tạo file CSV tại:
```
Output/Output_III/team_statistics.csv
```

## Cấu trúc output

### File CSV có các cột:

| Cột | Mô tả | Ví dụ |
|-----|-------|-------|
| `Team` | Tên câu lạc bộ | Arsenal, Liverpool, Man City |
| `Metric` | Tên chỉ số | Goals, Assists, Minutes |
| `Count` | Số cầu thủ có dữ liệu | 22 |
| `Median` | Trung vị | 2.5 |
| `Mean` | Trung bình | 3.04 |
| `Std_Dev` | Độ lệch chuẩn | 2.90 |

### Ví dụ dữ liệu:

```csv
Team,Metric,Count,Median,Mean,Std_Dev
Arsenal,Goals,22,2.5,3.04,2.90
Arsenal,Assists,22,2.0,2.5,2.94
Arsenal,Minutes,22,1657.5,1698.91,941.38
Liverpool,Goals,25,1.0,2.12,2.45
Liverpool,Assists,25,1.0,1.48,1.56
...
```

## Quy trình xử lý

### 1. Load dữ liệu
```python
df = pd.read_csv("Output/Output_I/players_stats.csv")
```

### 2. Chuyển đổi dữ liệu
- Thay thế `'N/a'` → `NaN`
- Chuyển đổi các cột số sang dạng numeric
- Giữ nguyên các cột text (Name, Nation, Team, Position)

```python
df[col] = pd.to_numeric(df[col].replace('N/a', np.nan), errors='coerce')
```

### 3. Nhóm theo đội và tính toán

Với mỗi đội:
```python
for team in teams:
    team_data = df[df['Team'] == team]
    
    for metric in numeric_columns:
        values = team_data[metric].dropna()
        
        median = np.median(values)
        mean = np.mean(values)
        std = np.std(values, ddof=1)
```

### 4. Lưu kết quả
```python
stats_df.to_csv("Output/Output_III/team_statistics.csv", 
                index=False, encoding='utf-8-sig')
```

## Cấu trúc code

```
team_statistics.py
├── load_data()              # Đọc CSV
├── convert_to_numeric()     # Chuyển đổi dữ liệu
├── calculate_team_statistics()  # Tính toán chính
├── save_results()           # Lưu file CSV
├── display_summary()        # Hiển thị tổng hợp
└── main()                   # Hàm điều phối
```

## Kết quả

### Thống kê tổng hợp:
- **Số đội**: 20 đội (Premier League)
- **Số chỉ số**: 71 chỉ số mỗi đội
- **Tổng số dòng**: ~1,420 dòng (20 đội × 71 chỉ số)

### Các chỉ số được phân tích:

#### Thông tin cơ bản:
- Age, Matches_Played, Starts, Minutes

#### Hiệu suất tấn công:
- Goals, Assists, Goals_Per90, Assists_Per90
- xG, xAG, xG_Per90, xAG_Per90

#### Chỉ số sút:
- SoT_Pct, SoT_Per90, Goals_Per_Shot, Avg_Shot_Distance

#### Chuyền bóng:
- Passes_Completed, Pass_Completion_Pct
- Key_Passes, Progressive_Passes
- Passes_Into_Final_Third, Passes_Into_Penalty_Area

#### Phòng thủ:
- Tackles, Tackles_Won, Blocks, Interceptions
- Challenges, Challenges_Lost

#### Kiểm soát bóng:
- Touches, Carries, Progressive_Carries
- Take_Ons_Attempted, Take_Ons_Success_Pct

#### Thủ môn:
- GA90, Save_Pct, CS_Pct, PK_Save_Pct

#### Khác:
- Yellow_Cards, Red_Cards, Fouls_Committed, Fouls_Drawn
- Offsides, Crosses, Ball_Recoveries
- Aerials_Won, Aerials_Lost, Aerials_Won_Pct

## Ví dụ output console

```
======================================================================
⚽ PHÂN TÍCH THỐNG KÊ CẦU THỦ THEO ĐỘI
   Premier League 2024-2025
======================================================================

📂 Đang đọc dữ liệu từ: Output/Output_I/players_stats.csv
✅ Đã đọc 503 cầu thủ từ 20 đội

🔄 Đang chuyển đổi dữ liệu sang dạng số...
✅ Đã chuyển đổi 71 cột số

📊 Đang tính toán thống kê cho từng đội...
   Số đội: 20
   Đang xử lý: Arsenal...
   Đang xử lý: Aston Villa...
   Đang xử lý: Bournemouth...
   ...

✅ Hoàn thành! Tổng cộng 1420 dòng thống kê
   (20 đội × 71 chỉ số)

💾 Đang lưu kết quả vào: Output/Output_III/team_statistics.csv
✅ Đã lưu thành công!
   Kích thước file: 125.45 KB

======================================================================
📈 TỔNG HỢP KẾT QUẢ
======================================================================

🏆 Số đội: 20
📊 Số chỉ số: 71
📝 Tổng số dòng: 1420

🔢 Các chỉ số phân tích:
   - Trung vị (Median)
   - Trung bình (Mean)
   - Độ lệch chuẩn (Std_Dev)

📋 Danh sách đội:
    1. Arsenal              - 71 chỉ số
    2. Aston Villa          - 71 chỉ số
    3. Bournemouth          - 71 chỉ số
    ...

📊 VÍ DỤ KẾT QUẢ (Goals):
----------------------------------------------------------------------
Đội                  Count    Median     Mean       Std_Dev   
----------------------------------------------------------------------
Man City             25       2.00       3.04       3.78
Arsenal              22       2.50       3.04       2.90
Liverpool            25       1.00       2.12       2.45
...

======================================================================
✅ HOÀN THÀNH!
======================================================================

📁 File kết quả: Output/Output_III/team_statistics.csv
📊 Mở file CSV để xem chi tiết thống kê của từng đội
```

## Ứng dụng

### 1. So sánh đội
```python
# Đọc kết quả
stats = pd.read_csv("Output/Output_III/team_statistics.csv")

# So sánh Goals trung bình của các đội
goals_mean = stats[stats['Metric'] == 'Goals'][['Team', 'Mean']].sort_values('Mean', ascending=False)
print(goals_mean.head(5))
```

### 2. Tìm đội có độ phân tán cao nhất
```python
# Đội có độ lệch chuẩn Goals cao nhất (phân hóa lớn)
goals_std = stats[stats['Metric'] == 'Goals'][['Team', 'Std_Dev']].sort_values('Std_Dev', ascending=False)
print(goals_std.head(5))
```

### 3. Phân tích theo chỉ số
```python
# Thống kê của một chỉ số cụ thể
passes = stats[stats['Metric'] == 'Passes_Completed']
print(passes[['Team', 'Median', 'Mean', 'Std_Dev']])
```

## Xử lý dữ liệu thiếu

- **Giá trị 'N/a'**: Được chuyển thành `NaN` và bỏ qua khi tính toán
- **Count**: Hiển thị số cầu thủ thực sự có dữ liệu cho mỗi chỉ số
- **Std_Dev**: Nếu chỉ có 1 cầu thủ, std = 0

## Troubleshooting

### Lỗi: "Module not found: pandas/numpy"
```bash
pip install pandas numpy
```

### Lỗi: "File not found: players_stats.csv"
Chạy Code_I trước để tạo dữ liệu:
```bash
cd Code/Code_I
python scraper_fbref.py
```

### Lỗi: "Permission denied" khi ghi file
Đóng file CSV nếu đang mở trong Excel, sau đó chạy lại.

## Workflow đầy đủ

```
1. Thu thập dữ liệu (Code_I)
   └─> python scraper_fbref.py
   └─> Output: players_stats.csv

2. Phân tích thống kê (Code_III)
   └─> python team_statistics.py
   └─> Output: team_statistics.csv

3. Phân tích kết quả
   └─> Mở team_statistics.csv
   └─> Sử dụng Excel/Python để trực quan hóa
```

## Công nghệ sử dụng

| Thư viện | Phiên bản | Mục đích |
|----------|-----------|----------|
| **Pandas** | 1.3.0+ | Xử lý DataFrame, nhóm dữ liệu |
| **NumPy** | 1.20.0+ | Tính toán thống kê (median, mean, std) |
| **Pathlib** | Built-in | Quản lý đường dẫn file |

## Mở rộng

### Thêm chỉ số thống kê khác:
```python
# Thêm vào hàm calculate_team_statistics()
min_val = np.min(values)
max_val = np.max(values)
q25 = np.percentile(values, 25)
q75 = np.percentile(values, 75)
```

### Xuất sang định dạng khác:
```python
# Excel
stats_df.to_excel("team_statistics.xlsx", index=False)

# JSON
stats_df.to_json("team_statistics.json", orient='records')
```

### Trực quan hóa:
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Boxplot Goals của các đội
goals_data = stats[stats['Metric'] == 'Goals']
plt.figure(figsize=(12, 6))
sns.barplot(data=goals_data, x='Team', y='Mean')
plt.xticks(rotation=45)
plt.title('Average Goals by Team')
plt.show()
```

## Tác giả

**Nhóm 8** - Môn Ngôn ngữ lập trình Python
- Học viện Công nghệ Bưu chính Viễn thông

## License

Dự án học tập - Premier League 2024-2025
