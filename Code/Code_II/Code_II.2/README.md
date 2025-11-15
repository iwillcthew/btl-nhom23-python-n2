# Code II.2 - Command Line Lookup Tool

## Mô tả

Chương trình tra cứu thông tin cầu thủ qua command line sử dụng module `requests`.

## Tính năng

- ✅ Tra cứu cầu thủ theo tên
- ✅ Tra cứu cầu thủ theo câu lạc bộ
- ✅ Hiển thị kết quả dưới dạng bảng đẹp
- ✅ Tự động lưu kết quả ra file CSV
- ✅ Tên file CSV theo tên cầu thủ/câu lạc bộ

## Cài đặt

### Thư viện cần thiết

```bash
pip install requests tabulate
```

### Yêu cầu

- Python 3.7+
- API server đang chạy (xem Code_II.1)
- Database đã được tạo (xem Code_I)

## Cách sử dụng

### Cú pháp

```bash
python lookup.py --name <tên cầu thủ>
python lookup.py --club <tên câu lạc bộ>
```

### Ví dụ

#### 1. Tra cứu theo tên cầu thủ

```bash
# Ví dụ 1: Mohamed Salah
python lookup.py --name "Mohamed Salah"

# Ví dụ 2: Erling Haaland
python lookup.py --name "Erling Haaland"

# Ví dụ 3: Bukayo Saka
python lookup.py --name "Bukayo Saka"
```

**Kết quả:**
- Hiển thị bảng thông tin chi tiết trên màn hình
- Lưu file CSV: `Output/Output_II/Mohamed_Salah.csv`

#### 2. Tra cứu theo câu lạc bộ

```bash
# Ví dụ 1: Liverpool
python lookup.py --club Liverpool

# Ví dụ 2: Manchester City
python lookup.py --club "Manchester City"

# Ví dụ 3: Arsenal
python lookup.py --club Arsenal
```

**Kết quả:**
- Hiển thị bảng danh sách cầu thủ trên màn hình
- Lưu file CSV: `Output/Output_II/Liverpool_players.csv`

## Output

### 1. Hiển thị trên màn hình

#### Tra cứu cầu thủ:
```
===============================================================================
⚽ THÔNG TIN CẦU THỦ: Mohamed Salah
===============================================================================

📋 THÔNG TIN CƠ BẢN:
Tên             Mohamed Salah
Quốc tịch       eg EGY
Câu lạc bộ      Liverpool
Vị trí          FW,MF
Tuổi            32

⏱️ THỜI GIAN THI ĐẤU:
Số trận                 11
Số trận đá chính       11
Số phút                990

⚡ CHỈ SỐ TẤN CÔNG:
Bàn thắng              10
Kiến tạo               6
xG                     8.2
xAG                    4.5
...
```

#### Tra cứu câu lạc bộ:
```
====================================================================================================
🏆 DANH SÁCH CẦU THỦ: Liverpool
📊 Tổng số: 25 cầu thủ
====================================================================================================
+-------+--------------------------+----------+--------+----------+------------+-----------+
| STT   | Tên                      | Vị trí   | Tuổi   | Số phút  | Bàn thắng  | Kiến tạo  |
+=======+==========================+==========+========+==========+============+===========+
| 1     | Alexis Mac Allister      | MF       | 25     | 950      | 2          | 1         |
| 2     | Mohamed Salah            | FW,MF    | 32     | 990      | 10         | 6         |
| ...   | ...                      | ...      | ...    | ...      | ...        | ...       |
+-------+--------------------------+----------+--------+----------+------------+-----------+

📊 TỔNG HỢP:
⚽ Tổng bàn thắng: 28
🎯 Tổng kiến tạo: 15
```

### 2. File CSV

File được lưu tự động vào: `Output/Output_II/`

**Tên file:**
- Tra cứu cầu thủ: `<Tên_Cầu_Thủ>.csv`
- Tra cứu CLB: `<Tên_CLB>_players.csv`

**Nội dung:**
- Tất cả các chỉ số từ database (60+ cột)
- Format CSV chuẩn, mở được bằng Excel
- Encoding: UTF-8 with BOM

## Workflow

```
1. User chạy lệnh
   └─> python lookup.py --name "Mohamed Salah"

2. Kiểm tra API
   └─> Kết nối tới http://127.0.0.1:5000

3. Gọi API
   └─> GET /api/player/Mohamed%20Salah

4. Nhận response
   └─> JSON data với thông tin cầu thủ

5. Hiển thị kết quả
   ├─> In bảng ra màn hình (tabulate)
   └─> Lưu file CSV (Output/Output_II/)

6. Hoàn thành
   └─> Thông báo đường dẫn file
```

## Lưu ý

### 1. API Server phải chạy trước

```bash
# Terminal 1: Chạy API
cd Code/Code_II/Code_II.1
python api.py

# Terminal 2: Chạy lookup
cd Code/Code_II/Code_II.2
python lookup.py --name "Mohamed Salah"
```

### 2. Tên có dấu cách phải đặt trong dấu ngoặc kép

```bash
# ✅ Đúng
python lookup.py --name "Mohamed Salah"
python lookup.py --club "Manchester City"

# ❌ Sai
python lookup.py --name Mohamed Salah
```

### 3. Ưu tiên tham số

Nếu cung cấp cả 2 tham số, chỉ `--name` được xử lý:

```bash
# Chỉ tra cứu Mohamed Salah, bỏ qua Liverpool
python lookup.py --name "Mohamed Salah" --club Liverpool
```

## Khắc phục sự cố

### Lỗi: Cannot connect to API

```
❌ Không thể kết nối tới API server: http://127.0.0.1:5000

Solution:
1. Chạy API server:
   cd Code/Code_II/Code_II.1
   python api.py

2. Kiểm tra port 5000 không bị chiếm dụng
```

### Lỗi: Module 'tabulate' not found

```
Solution:
pip install tabulate
```

### Lỗi: Không tìm thấy cầu thủ

```
❌ Không tìm thấy cầu thủ có tên "xxx"

Solution:
1. Kiểm tra chính tả
2. Thử với tên ngắn hơn (ví dụ: "Salah" thay vì "Mohamed Salah")
3. Xem danh sách cầu thủ có sẵn trong database
```

## Ví dụ đầy đủ

### Test 1: Tra cứu cầu thủ

```bash
cd Code\Code_II\Code_II.2

python lookup.py --name "Mohamed Salah"
```

**Output:**
```
🔍 Đang kiểm tra kết nối API...
✅ Đã kết nối: http://127.0.0.1:5000

🔍 Đang tra cứu cầu thủ: Mohamed Salah

✅ Tìm thấy cầu thủ: Mohamed Salah

[Bảng thông tin chi tiết...]

💾 Đã lưu kết quả vào: d:\...\Output\Output_II\Mohamed_Salah.csv

✅ Hoàn thành!
```

### Test 2: Tra cứu câu lạc bộ

```bash
python lookup.py --club Liverpool
```

**Output:**
```
🔍 Đang kiểm tra kết nối API...
✅ Đã kết nối: http://127.0.0.1:5000

🔍 Đang tra cứu câu lạc bộ: Liverpool

✅ Tìm thấy 25 cầu thủ

[Bảng danh sách cầu thủ...]

💾 Đã lưu kết quả vào: d:\...\Output\Output_II\Liverpool_players.csv

✅ Hoàn thành!
```

## Cấu trúc thư mục

```
Code/Code_II/Code_II.2/
├── lookup.py           # Chương trình chính
├── test_lookup.bat     # Script test tự động
└── README.md           # File này

Output/Output_II/
├── Mohamed_Salah.csv           # Kết quả tra cứu cầu thủ
├── Liverpool_players.csv       # Kết quả tra cứu CLB
└── ...
```

## Tác giả

Nhóm 23 - Bài tập lớn Python - Phần II.2
