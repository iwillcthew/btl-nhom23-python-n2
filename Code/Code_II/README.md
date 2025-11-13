# Code II - Tổng quan

## Mô tả

Phần II của bài tập lớn: Tạo REST API và các công cụ tra cứu dữ liệu cầu thủ.

## Cấu trúc

```
Code/Code_II/
├── Code_II.1/          # REST API + GUI
│   ├── api.py          # Flask REST API server
│   ├── ui_tkinter.py   # Giao diện Tkinter
│   ├── run_api.bat     # Script chạy API
│   ├── start_both.bat  # Script chạy API + UI
│   └── README.md
│
└── Code_II.2/          # Command Line Tool
    ├── lookup.py       # CLI tra cứu
    ├── demo.bat        # Script demo
    ├── quick_test.bat  # Test nhanh
    ├── README.md
    └── QUICKSTART.md
```

## Phần II.1 - REST API & Giao diện

### Tính năng:
- ✅ Flask REST API server (port 5000)
- ✅ Giao diện Tkinter kết nối với API
- ✅ Tra cứu theo tên cầu thủ
- ✅ Tra cứu theo câu lạc bộ

### Chạy:
```bash
cd Code_II.1
start_both.bat
```

### API Endpoints:
- `GET /api/player/<name>` - Tra cứu cầu thủ
- `GET /api/team/<team>` - Tra cứu CLB
- `GET /api/teams` - Danh sách CLB
- `GET /api/players` - Danh sách cầu thủ

---

## Phần II.2 - Command Line Tool

### Tính năng:
- ✅ Tra cứu qua command line
- ✅ Hiển thị bảng trên console
- ✅ Xuất file CSV tự động
- ✅ Tên file theo input

### Cú pháp:
```bash
python lookup.py --name "Mohamed Salah"
python lookup.py --club Liverpool
```

### Output:
- Console: Bảng dữ liệu
- File CSV: `Output/Output_II/<tên>.csv`

---

## So sánh II.1 vs II.2

| Tiêu chí | II.1 (GUI + API) | II.2 (CLI) |
|----------|------------------|------------|
| **Interface** | Giao diện Tkinter | Command line |
| **Input** | UI controls | Arguments |
| **Output** | Màn hình GUI | Console + CSV |
| **Use case** | Desktop app | Automation/Scripts |
| **Dependencies** | Flask, requests, tkinter | requests, tabulate |

---

## Workflow đầy đủ

### Setup một lần:
```bash
# 1. Cài đặt dependencies
pip install Flask flask-cors requests tabulate

# 2. Tạo database (nếu chưa có)
cd Code/Code_I
python scraper_fbref.py
```

### Sử dụng II.1 (GUI):
```bash
# Terminal 1: API Server
cd Code/Code_II/Code_II.1
python api.py

# Terminal 2: GUI
python ui_tkinter.py
```

### Sử dụng II.2 (CLI):
```bash
# API server phải chạy trước
cd Code/Code_II/Code_II.2

# Tra cứu
python lookup.py --name "Mohamed Salah"
python lookup.py --club Liverpool
```

---

## Demo nhanh

### Demo II.1:
```bash
cd Code_II.1
start_both.bat
```

### Demo II.2:
```bash
cd Code_II.2
demo.bat
```

---

## Output Structure

```
Output/
├── Output_I/           # Phần I - Scraping
│   ├── football_stats.db
│   ├── players_stats.csv
│   └── player_transfers.csv
│
└── Output_II/          # Phần II - Tra cứu
    ├── Mohamed_Salah.csv
    ├── Liverpool.csv
    ├── Erling_Haaland.csv
    └── Manchester_City.csv
```

---

## Dependencies

### Phần II.1:
```
Flask>=3.0.0
flask-cors>=4.0.0
requests>=2.31.0
tkinter (built-in)
```

### Phần II.2:
```
requests>=2.31.0
tabulate>=0.9.0
```

---

## Troubleshooting

### Lỗi: Cannot connect to API
**Nguyên nhân:** API server chưa chạy  
**Giải pháp:**
```bash
cd Code_II.1
python api.py
```

### Lỗi: Module not found
**Giải pháp:**
```bash
pip install Flask flask-cors requests tabulate
```

### Lỗi: Database not found
**Giải pháp:**
```bash
cd Code/Code_I
python scraper_fbref.py
```

---

## Kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                     Database Layer                       │
│              Output/Output_I/football_stats.db          │
└─────────────────────────────────────────────────────────┘
                            ▲
                            │
┌─────────────────────────────────────────────────────────┐
│                     API Server Layer                     │
│              Code_II.1/api.py (Flask)                   │
│                   Port: 5000                            │
└─────────────────────────────────────────────────────────┘
                            ▲
                    ┌───────┴───────┐
                    │               │
        ┌───────────▼─────┐  ┌──────▼────────┐
        │   GUI Client    │  │  CLI Client   │
        │ (ui_tkinter.py) │  │  (lookup.py)  │
        │   II.1          │  │    II.2       │
        └─────────────────┘  └───────────────┘
```

---

## Testing

### Test II.1:
1. Chạy `start_both.bat`
2. Trong UI, tab 1: nhập "Mohamed Salah"
3. Tab 2: chọn "Liverpool"

### Test II.2:
```bash
# Test cầu thủ
python lookup.py --name "Mohamed Salah"

# Test CLB
python lookup.py --club Liverpool

# Kiểm tra CSV
dir ..\..\Output\Output_II\
```

---

## Tác giả

Nhóm 23 - Bài tập lớn Python - N2
