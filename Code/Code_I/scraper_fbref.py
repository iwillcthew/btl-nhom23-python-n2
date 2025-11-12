"""
scraper_fbref.py - Thu thập dữ liệu cầu thủ từ fbref.com
Phần I.1 của bài tập lớn
"""

import time
import sqlite3
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
from config import (
    BASE_URL, SEASON_SUFFIX, TABLES, DATABASE_FILE, 
    TABLE_PLAYERS, MIN_MINUTES, WAIT_TIMEOUT, ALL_COLUMNS
)


def setup_driver():
    """Thiết lập Selenium WebDriver với Edge"""
    edge_options = Options()
    edge_options.add_argument('--headless')  # Chạy ẩn trình duyệt
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')
    
    driver = webdriver.Edge(options=edge_options)
    return driver


def fetch_table_data(driver, url, table_id, fields):
    """
    Lấy dữ liệu từ một bảng thống kê trên fbref.com
    
    Args:
        driver: Selenium WebDriver
        url: URL của trang
        table_id: ID của bảng HTML cần lấy
        fields: Danh sách các trường cần thu thập
        
    Returns:
        dict: Dữ liệu cầu thủ với key là (tên, đội)
    """
    print(f"Đang tải trang: {url}")
    driver.get(url)
    
    # Đợi bảng xuất hiện
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, table_id))
        )
        time.sleep(2)  # Đợi thêm để đảm bảo JavaScript load xong
    except Exception as e:
        print(f"Không tìm thấy bảng {table_id}: {e}")
        return {}
    
    # Parse HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", id=table_id)
    
    if not table:
        print(f"Không tìm thấy bảng {table_id}")
        return {}
    
    tbody = table.find("tbody")
    if not tbody:
        return {}
    
    rows = tbody.find_all("tr")
    data = {}
    
    for row in rows:
        # Bỏ qua các hàng phụ (không phải dữ liệu cầu thủ)
        if row.get('class') and 'thead' in row.get('class'):
            continue
            
        player_cell = row.find("td", {"data-stat": "player"})
        team_cell = row.find("td", {"data-stat": "team"})
        
        if not player_cell or not team_cell:
            continue
        
        player_name = player_cell.text.strip()
        team_name = team_cell.text.strip()
        
        if not player_name or not team_name:
            continue
        
        # Key duy nhất cho mỗi cầu thủ
        key = (player_name, team_name)
        
        if key not in data:
            data[key] = {}
        
        # Thu thập các trường dữ liệu
        for col_name, stat_name in fields:
            cell = row.find("td", {"data-stat": stat_name})
            value = cell.text.strip() if cell and cell.text.strip() else "N/a"
            data[key][col_name] = value
    
    print(f"  -> Đã lấy {len(data)} cầu thủ")
    return data


def combine_data(list_of_dicts):
    """
    Gộp dữ liệu từ nhiều bảng thành một
    
    Args:
        list_of_dicts: Danh sách các dict dữ liệu từ các bảng khác nhau
        
    Returns:
        dict: Dữ liệu đã gộp
    """
    combined = {}
    for data_dict in list_of_dicts:
        for key, values in data_dict.items():
            if key not in combined:
                combined[key] = {}
            combined[key].update(values)
    return combined


def filter_by_minutes(data, min_minutes=MIN_MINUTES):
    """
    Lọc cầu thủ theo số phút thi đấu
    
    Args:
        data: Dữ liệu cầu thủ
        min_minutes: Số phút tối thiểu
        
    Returns:
        list: Danh sách cầu thủ đủ điều kiện
    """
    filtered = []
    for player_data in data.values():
        minutes_str = player_data.get("Minutes", "0")
        # Xử lý dấu phẩy trong số (ví dụ: 1,234 -> 1234)
        minutes_str = minutes_str.replace(",", "")
        
        try:
            minutes = int(minutes_str)
        except ValueError:
            minutes = 0
        
        if minutes > min_minutes:
            filtered.append(player_data)
    
    print(f"Đã lọc: {len(filtered)} cầu thủ có số phút > {min_minutes}")
    return filtered


def create_database():
    """Tạo cơ sở dữ liệu SQLite và bảng players"""
    # Tạo thư mục nếu chưa có
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Tạo câu lệnh CREATE TABLE động dựa trên ALL_COLUMNS
    columns_def = []
    for col in ALL_COLUMNS:
        columns_def.append(f"{col} TEXT")
    
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_PLAYERS} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {', '.join(columns_def)}
    )
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()
    print(f"Đã tạo database: {DATABASE_FILE}")
    print(f"Đã tạo bảng: {TABLE_PLAYERS}")


def save_to_database(players_data):
    """
    Lưu dữ liệu cầu thủ vào SQLite
    
    Args:
        players_data: Danh sách dữ liệu cầu thủ
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Xóa dữ liệu cũ (nếu có)
    cursor.execute(f"DELETE FROM {TABLE_PLAYERS}")
    
    # Chuẩn bị câu lệnh INSERT
    placeholders = ", ".join(["?" for _ in ALL_COLUMNS])
    insert_sql = f"INSERT INTO {TABLE_PLAYERS} ({', '.join(ALL_COLUMNS)}) VALUES ({placeholders})"
    
    # Insert từng cầu thủ
    for player in players_data:
        # Đảm bảo đủ các cột, điền "N/a" nếu thiếu
        values = []
        for col in ALL_COLUMNS:
            value = player.get(col, "N/a")
            # Loại bỏ dấu phẩy trong số
            if isinstance(value, str):
                value = value.replace(",", "")
            values.append(value)
        
        cursor.execute(insert_sql, values)
    
    conn.commit()
    conn.close()
    print(f"Đã lưu {len(players_data)} cầu thủ vào database")


def save_to_csv(players_data, output_file):
    """
    Lưu dữ liệu cầu thủ ra file CSV
    
    Args:
        players_data: Danh sách dữ liệu cầu thủ
        output_file: Đường dẫn file CSV
    """
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=ALL_COLUMNS)
        writer.writeheader()
        
        for player in players_data:
            # Đảm bảo đủ các cột, điền "N/a" nếu thiếu
            row = {}
            for col in ALL_COLUMNS:
                value = player.get(col, "N/a")
                # Loại bỏ dấu phẩy trong số
                if isinstance(value, str):
                    value = value.replace(",", "")
                row[col] = value
            writer.writerow(row)
    
    print(f"Đã lưu {len(players_data)} cầu thủ ra file CSV: {output_file}")


def main():
    """Hàm chính để chạy scraper"""
    print("=" * 60)
    print("BẮT ĐẦU THU THẬP DỮ LIỆU CẦU THỦ TỪ FBREF.COM")
    print("=" * 60)
    
    # Thiết lập driver
    driver = setup_driver()
    
    try:
        # Thu thập dữ liệu từ các bảng
        all_tables_data = []
        
        for table_config in TABLES:
            url = BASE_URL + table_config["url"] + SEASON_SUFFIX
            table_data = fetch_table_data(
                driver, 
                url, 
                table_config["table_id"], 
                table_config["fields"]
            )
            all_tables_data.append(table_data)
            time.sleep(2)  # Tránh bị rate-limit
        
        # Gộp dữ liệu
        print("\nĐang gộp dữ liệu từ các bảng...")
        merged_data = combine_data(all_tables_data)
        print(f"Tổng số cầu thủ: {len(merged_data)}")
        
        # Lọc theo số phút
        print(f"\nĐang lọc cầu thủ có số phút > {MIN_MINUTES}...")
        filtered_players = filter_by_minutes(merged_data)
        
        # Tạo database và lưu dữ liệu
        print("\nĐang tạo database và lưu dữ liệu...")
        create_database()
        save_to_database(filtered_players)
        
        # Lưu ra file CSV
        csv_file = os.path.join(os.path.dirname(DATABASE_FILE), "players_stats.csv")
        save_to_csv(filtered_players, csv_file)
        
        print("\n" + "=" * 60)
        print("HOÀN THÀNH THU THẬP DỮ LIỆU!")
        print(f"Database: {DATABASE_FILE}")
        print(f"CSV File: {csv_file}")
        print(f"Bảng: {TABLE_PLAYERS}")
        print(f"Số lượng cầu thủ: {len(filtered_players)}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nLỗi: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
