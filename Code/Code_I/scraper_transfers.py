"""
scraper_transfers.py - Thu thập giá chuyển nhượng từ footballtransfers.com
Phần I.2 của bài tập lớn
"""

import time
import sqlite3
import re
import os
import csv
import base64
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from config import DATABASE_FILE, TABLE_PLAYERS, TABLE_TRANSFERS


def setup_driver():
    """Thiết lập Selenium WebDriver với Edge"""
    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_argument('--log-level=3')
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    edge_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')
    
    return webdriver.Edge(options=edge_options)


def get_players_from_db():
    """Lấy danh sách cầu thủ từ database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, Name, Team FROM {TABLE_PLAYERS}")
    players = cursor.fetchall()
    conn.close()
    return players


def get_etv_from_base64_data(soup):
    """Trích xuất giá trị ETV mùa 2024-2025 từ dữ liệu base64"""
    try:
        player_graph = soup.find('div', class_='player-graph')
        if not player_graph or 'data-base64' not in player_graph.attrs:
            return None
        
        # Decode base64 và parse JSON
        data_base64 = player_graph['data-base64']
        decoded = base64.b64decode(data_base64).decode('utf-8')
        data = json.loads(decoded)
        
        if 'dataSets' not in data:
            return None
        
        # Tìm dataset có order=2 (ETV estimate)
        for dataset in data['dataSets']:
            if dataset.get('order') == 2 and 'data' in dataset:
                # Tìm điểm dữ liệu x="04-'25"
                for point in dataset['data']:
                    if point.get('x') == "04-'25" and point.get('price'):
                        return point['price']
        
        return None
        
    except:
        return None


def extract_value_from_page(soup):
    """Trích xuất giá trị chuyển nhượng từ trang (ưu tiên base64)"""
    # Phương pháp 1: Lấy từ base64 data
    etv_value = get_etv_from_base64_data(soup)
    if etv_value:
        return etv_value
    
    # Phương pháp 2: Lấy từ player-value-large
    player_value_div = soup.find('div', class_='player-value player-value-large')
    if player_value_div:
        player_tag = player_value_div.find('span', class_='player-tag')
        if player_tag:
            value_text = player_tag.get_text(strip=True)
            match = re.search(r'([€£$])([\d,.]+)([MK])?', value_text, re.I)
            if match:
                return f"{match.group(1)}{match.group(2)}{match.group(3) or ''}"
    
    return None


def search_player_transfer_value(driver, player_name):
    """Tìm giá chuyển nhượng của cầu thủ"""
    try:
        # Phương pháp 1: Truy cập trực tiếp
        search_name = player_name.replace(" ", "-").lower()
        url = f"https://www.footballtransfers.com/en/players/{search_name}"
        driver.get(url)
        time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        value = extract_value_from_page(soup)
        if value:
            return value
        
        # Phương pháp 2: Tìm kiếm
        search_url = f"https://www.footballtransfers.com/en/search?search_value={player_name.replace(' ', '+')}"
        driver.get(search_url)
        time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        player_list_panel = soup.find('div', class_='playerList-panel')
        
        if player_list_panel:
            first_link = player_list_panel.find('a', href=True)
            if first_link:
                player_detail_url = first_link['href']
                if not player_detail_url.startswith('http'):
                    player_detail_url = f"https://www.footballtransfers.com{player_detail_url}"
                
                driver.get(player_detail_url)
                time.sleep(1)
                
                soup = BeautifulSoup(driver.page_source, "html.parser")
                value = extract_value_from_page(soup)
                if value:
                    return value
        
        return "N/a"
        
    except:
        return "N/a"


def create_transfers_table():
    """Tạo bảng player_transfers trong database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Xóa bảng cũ nếu tồn tại
    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_TRANSFERS}")
    
    # Tạo bảng mới với cấu trúc đơn giản
    create_table_sql = f"""
    CREATE TABLE {TABLE_TRANSFERS} (
        player_id INTEGER PRIMARY KEY,
        player_name TEXT,
        team TEXT,
        transfer_value TEXT,
        FOREIGN KEY (player_id) REFERENCES {TABLE_PLAYERS}(id)
    )
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()
    print(f"Đã tạo bảng: {TABLE_TRANSFERS}")


def save_transfer_value(player_id, player_name, team, transfer_value):
    """Lưu giá trị chuyển nhượng vào database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute(f"""
        INSERT OR REPLACE INTO {TABLE_TRANSFERS} 
        (player_id, player_name, team, transfer_value)
        VALUES (?, ?, ?, ?)
    """, (player_id, player_name, team, transfer_value))
    
    conn.commit()
    conn.close()


def save_transfers_to_csv(output_file):
    """Lưu dữ liệu ra file CSV"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT player_id, player_name, team, transfer_value
        FROM {TABLE_TRANSFERS}
        ORDER BY player_id
    """)
    rows = cursor.fetchall()
    conn.close()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['player_id', 'player_name', 'team', 'transfer_value'])
        writer.writerows(rows)
    
    print(f"Đã lưu {len(rows)} cầu thủ ra CSV: {output_file}")


def main():
    """Hàm chính"""
    print("Bắt đầu thu thập giá chuyển nhượng...")
    
    create_transfers_table()
    
    players = get_players_from_db()
    print(f"Có {len(players)} cầu thủ cần xử lý")
    
    driver = setup_driver()
    
    try:
        success_count = 0
        na_count = 0
        
        for i, (player_id, player_name, team) in enumerate(players, 1):
            print(f"[{i}/{len(players)}] {player_name} ({team})", end=" ")
            
            transfer_value = search_player_transfer_value(driver, player_name)
            save_transfer_value(player_id, player_name, team, transfer_value)
            
            if transfer_value != "N/a":
                print(f"✓ {transfer_value}")
                success_count += 1
            else:
                print("✗")
                na_count += 1
            
            if i % 10 == 0:
                print(f"  Tiến độ: {success_count}/{i} thành công")
            
            time.sleep(1)
        
        csv_file = os.path.join(os.path.dirname(DATABASE_FILE), "player_transfers.csv")
        save_transfers_to_csv(csv_file)
        
        print(f"\nHoàn thành! Thành công: {success_count}/{len(players)}")
        print(f"Database: {DATABASE_FILE}")
        print(f"CSV: {csv_file}")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
