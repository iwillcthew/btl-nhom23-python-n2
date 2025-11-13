# Code II - REST API & Giao diện Tkinter

## Mô tả

Phần II.1 của bài tập lớn: Tạo REST API và giao diện tra cứu thông tin cầu thủ.

## Files

### 1. `api.py` - Flask REST API

REST API để tra cứu thông tin cầu thủ từ database SQLite.

#### Cài đặt thư viện

```bash
pip install Flask flask-cors
```

#### Chạy server

```bash
cd Code/Code_II/Code_II.1
python api.py
# hoặc double-click: run_api.bat
```

Server sẽ chạy tại: **http://127.0.0.1:5000**

#### API Endpoints

##### 1. Trang chủ - Hướng dẫn API
```
GET /
```

##### 2. Tra cứu theo tên cầu thủ
```
GET /api/player/<name>
```

**Ví dụ:**
- http://127.0.0.1:5000/api/player/Mohamed%20Salah
- http://127.0.0.1:5000/api/player/Erling%20Haaland

**Response mẫu:**
```json
{
  "success": true,
  "message": "Thông tin cầu thủ \"Mohamed Salah\"",
  "data": {
    "id": 123,
    "Name": "Mohamed Salah",
    "Team": "Liverpool",
    "Position": "FW",
    "Goals": "15",
    "Assists": "10",
    ...
  }
}
```

##### 3. Tra cứu theo câu lạc bộ
```
GET /api/team/<team_name>
```

**Ví dụ:**
- http://127.0.0.1:5000/api/team/Liverpool
- http://127.0.0.1:5000/api/team/Manchester%20City

**Response mẫu:**
```json
{
  "success": true,
  "message": "Danh sách cầu thủ của Liverpool",
  "team_stats": {
    "team_name": "Liverpool",
    "total_players": 25,
    "positions": {
      "FW": 5,
      "MF": 10,
      "DF": 8,
      "GK": 2
    }
  },
  "data": [...]
}
```

##### 4. Lấy danh sách tất cả cầu thủ (có phân trang)
```
GET /api/players?page=1&per_page=20
```

##### 5. Lấy danh sách tất cả câu lạc bộ
```
GET /api/teams
```

#### Test API với curl

**Windows PowerShell:**
```powershell
# Tra cứu cầu thủ
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/player/Mohamed Salah"

# Tra cứu câu lạc bộ
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/team/Liverpool"
```

**Linux/Mac:**
```bash
# Tra cứu cầu thủ
curl "http://127.0.0.1:5000/api/player/Mohamed%20Salah"

# Tra cứu câu lạc bộ
curl "http://127.0.0.1:5000/api/team/Liverpool"
```

---

### 2. `ui_tkinter_api.py` - Giao diện Tkinter (API Client)

Giao diện đồ họa kết nối với Flask API để tra cứu thông tin cầu thủ.

**Ưu điểm:**
- Tách biệt frontend và backend
- API có thể chạy trên server riêng
- Dễ dàng mở rộng và bảo trì
- Nhiều client có thể kết nối cùng lúc

#### Chạy với API

**Cách 1: Tự động (Khuyến nghị)**
```bash
cd Code/Code_II/Code_II.1
start_both.bat
```
Script sẽ tự động:
1. Chạy Flask API server
2. Đợi 3 giây
3. Chạy UI client

**Cách 2: Thủ công**

Terminal 1 - Chạy API server:
```bash
cd Code/Code_II/Code_II.1
python api.py
# hoặc: run_api.bat
```

Terminal 2 - Chạy UI client:
```bash
cd Code/Code_II/Code_II.1
python ui_tkinter_api.py
# hoặc: run_ui_api.bat
```

**Lưu ý:** API server phải đang chạy trước!

#### Tính năng (Cả 2 phiên bản)

**Tab 1: 🔍 Tra cứu theo Tên Cầu Thủ**
- Nhập tên cầu thủ vào ô tìm kiếm
- Nhấn Enter hoặc click "🔍 Tìm kiếm"
- Hiển thị toàn bộ chỉ số của cầu thủ:
  - Thông tin cơ bản (tên, tuổi, vị trí, CLB)
  - Thời gian thi đấu (số trận, số phút)
  - Chỉ số tấn công (bàn thắng, kiến tạo, xG, xAG)
  - Chỉ số chuyền bóng
  - Chỉ số phòng thủ
  - Kỷ luật (thẻ vàng, thẻ đỏ)

**Tab 2: 🏆 Tra cứu theo Câu Lạc Bộ**
- Chọn câu lạc bộ từ dropdown
- Click "🔍 Xem danh sách"
- Hiển thị:
  - Thống kê tổng quan (số lượng cầu thủ, phân bố vị trí)
  - Bảng danh sách cầu thủ với các chỉ số chính
  - Tổng hợp bàn thắng và kiến tạo của đội

#### Screenshot giao diện

```
┌─────────────────────────────────────────────────────────────┐
│     ⚽ FOOTBALL STATS - PREMIER LEAGUE 2024/25              │
├─────────────────────────────────────────────────────────────┤
│ [🔍 Tra cứu theo Tên] [🏆 Tra cứu theo CLB]                │
│                                                             │
│ Nhập tên cầu thủ: [_________________] [🔍 Tìm] [🗑️ Xóa]   │
│                                                             │
│ ┌─ 📊 Thông tin cầu thủ ─────────────────────────────────┐ │
│ │                                                         │ │
│ │ ======================================================  │ │
│ │ ⚽ THÔNG TIN CẦU THỦ: Mohamed Salah                    │ │
│ │ ======================================================  │ │
│ │                                                         │ │
│ │ 📋 THÔNG TIN CƠ BẢN:                                   │ │
│ │ Tên             : Mohamed Salah                         │ │
│ │ Quốc tịch       : eg EGY                               │ │
│ │ Câu lạc bộ      : Liverpool                            │ │
│ │ ...                                                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Cấu trúc thư mục

```
Code/Code_II/Code_II.1/
├── api.py              # Flask REST API
├── ui_tkinter_api.py   # Giao diện Tkinter (API client - kết nối qua API) ⭐
├── run_api.bat         # Script chạy API server
├── run_ui_api.bat      # Script chạy UI API client
├── start_both.bat      # Script chạy cả API + UI ⭐
└── README.md           # File này
```

## Yêu cầu hệ thống

- Python 3.7+
- Flask, flask-cors (cho API)
- requests (cho UI API client)
- tkinter (đã có sẵn trong Python)
- SQLite database đã được tạo từ phần I

**Cài đặt dependencies:**
```bash
pip install Flask flask-cors requests
```

## Lưu ý

1. **Database**: Đảm bảo đã chạy `scraper_fbref.py` để tạo database trước
2. **Đường dẫn**: Database phải ở `Output/Output_I/football_stats.db`
3. **Chọn phiên bản phù hợp**:
   - **ui_tkinter.py** (Standalone): Truy cập trực tiếp database, không cần API server
     - ✅ Đơn giản, chạy ngay
     - ❌ Không có tính năng client-server
   
   - **ui_tkinter_api.py** (API Client): Kết nối qua Flask API
     - ✅ Tách biệt frontend/backend
     - ✅ API có thể chạy remote
     - ✅ Nhiều client cùng lúc
     - ❌ Cần chạy API server trước
   
   - **Flask API**: REST API cho integration
     - ✅ Chuẩn RESTful
     - ✅ Dễ tích hợp với app khác
     - ✅ Có thể deploy lên server

## Khắc phục sự cố

### Lỗi: Không tìm thấy database
```
Solution: Chạy lại scraper_fbref.py để tạo database
cd Code/Code_I
python scraper_fbref.py
```

### Lỗi: Module 'Flask' not found
```
Solution: Cài đặt Flask
pip install Flask flask-cors
```

### Lỗi: Tkinter không hoạt động
```
Solution: Tkinter thường có sẵn trong Python, nếu không có:
- Windows: Reinstall Python với tùy chọn "tcl/tk and IDLE"
- Linux: sudo apt-get install python3-tk
- Mac: Đã có sẵn
```

### Lỗi: Cannot connect to API server (ui_tkinter_api.py)
```
Solution 1: Chạy API server trước
cd Code/Code_II/Code_II.1
python api.py

Solution 2: Kiểm tra URL trong ui_tkinter_api.py
API_BASE_URL = "http://127.0.0.1:5000"  # Đúng port
```

## Demo

### Chạy UI + API (Architecture đầy đủ)
```bash
cd Code/Code_II/Code_II.1
start_both.bat
# hoặc thủ công:
# Terminal 1: python api.py
# Terminal 2: python ui_tkinter_api.py
```
➡️ API server chạy ở cổng 5000, UI kết nối qua HTTP

### Test API với Browser/Postman
```bash
# Bước 1: Chạy server
cd Code/Code_II/Code_II.1
python api.py

# Bước 2: Mở browser
http://127.0.0.1:5000

# Bước 3: Test endpoint
http://127.0.0.1:5000/api/player/Mohamed%20Salah
http://127.0.0.1:5000/api/team/Liverpool
```

---

## Tác giả

Nhóm 23 - Bài tập lớn Python
