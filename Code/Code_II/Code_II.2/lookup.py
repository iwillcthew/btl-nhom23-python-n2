"""
lookup.py - Tra cứu dữ liệu cầu thủ qua command line
Phần II.2 - Sử dụng module requests
"""

import requests
import argparse
import sys
import csv
import os
from datetime import datetime
from tabulate import tabulate

# URL của API server
API_BASE_URL = "http://127.0.0.1:5000"


def check_api_connection():
    """Kiểm tra API server có đang chạy không"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=2)
        return response.status_code == 200
    except:
        return False


def search_player(player_name):
    """Tra cứu cầu thủ theo tên"""
    try:
        url = f"{API_BASE_URL}/api/player/{player_name}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data
        elif response.status_code == 404:
            data = response.json()
            return {'success': False, 'message': data.get('message', 'Không tìm thấy')}
        else:
            return {'success': False, 'message': f'HTTP Error: {response.status_code}'}
    except Exception as e:
        return {'success': False, 'message': f'Lỗi: {str(e)}'}


def search_club(club_name):
    """Tra cứu cầu thủ theo câu lạc bộ"""
    try:
        url = f"{API_BASE_URL}/api/team/{club_name}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data
        elif response.status_code == 404:
            data = response.json()
            return {'success': False, 'message': data.get('message', 'Không tìm thấy')}
        else:
            return {'success': False, 'message': f'HTTP Error: {response.status_code}'}
    except Exception as e:
        return {'success': False, 'message': f'Lỗi: {str(e)}'}


def sanitize_filename(name):
    """Làm sạch tên file, loại bỏ ký tự không hợp lệ"""
    # Thay thế các ký tự không hợp lệ
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    # Loại bỏ khoảng trắng thừa
    name = name.strip().replace(' ', '_')
    return name


def save_to_csv(data, filename, is_player=True):
    """Lưu dữ liệu ra file CSV"""
    # Tạo thư mục output nếu chưa có
    output_dir = os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..', 'Output', 'Output_II'
    )
    os.makedirs(output_dir, exist_ok=True)
    
    # Đường dẫn file đầy đủ
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            if is_player:
                # Lưu thông tin 1 cầu thủ
                if isinstance(data, dict):
                    writer = csv.DictWriter(f, fieldnames=data.keys())
                    writer.writeheader()
                    writer.writerow(data)
                else:
                    # Nhiều cầu thủ
                    if len(data) > 0:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
            else:
                # Lưu danh sách cầu thủ của CLB
                if len(data) > 0:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        
        return filepath
    except Exception as e:
        print(f"Lỗi khi lưu file CSV: {e}")
        return None


def display_player_table(player_data):
    """Hiển thị thông tin cầu thủ dưới dạng bảng"""
    if isinstance(player_data, list):
        # Nhiều cầu thủ - hiển thị bảng tóm tắt
        table_data = []
        for p in player_data:
            table_data.append([
                p.get('Name', 'N/a'),
                p.get('Team', 'N/a'),
                p.get('Position', 'N/a'),
                p.get('Age', 'N/a'),
                p.get('Minutes', 'N/a'),
                p.get('Goals', 'N/a'),
                p.get('Assists', 'N/a')
            ])
        
        headers = ['Tên', 'CLB', 'Vị trí', 'Tuổi', 'Phút', 'Bàn thắng', 'Kiến tạo']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
    else:
        # 1 cầu thủ - hiển thị chi tiết
        player = player_data
        
        print("\n" + "=" * 80)
        print(f"THÔNG TIN CẦU THỦ: {player.get('Name', 'N/a')}")
        print("=" * 80)
        
        # Thông tin cơ bản
        print("\nTHÔNG TIN CƠ BẢN:")
        basic_info = [
            ['Tên', player.get('Name', 'N/a')],
            ['Quốc tịch', player.get('Nation', 'N/a')],
            ['Câu lạc bộ', player.get('Team', 'N/a')],
            ['Vị trí', player.get('Position', 'N/a')],
            ['Tuổi', player.get('Age', 'N/a')],
        ]
        print(tabulate(basic_info, tablefmt='simple'))
        
        # Thời gian thi đấu
        print("\nTHỜI GIAN THI ĐẤU:")
        time_info = [
            ['Số trận', player.get('Matches_Played', 'N/a')],
            ['Số trận đá chính', player.get('Starts', 'N/a')],
            ['Số phút', player.get('Minutes', 'N/a')],
        ]
        print(tabulate(time_info, tablefmt='simple'))
        
        # Tấn công
        print("\nCHỈ SỐ TẤN CÔNG:")
        attack_info = [
            ['Bàn thắng', player.get('Goals', 'N/a')],
            ['Kiến tạo', player.get('Assists', 'N/a')],
            ['xG', player.get('xG', 'N/a')],
            ['xAG', player.get('xAG', 'N/a')],
            ['Bàn thắng/90 phút', player.get('Goals_Per90', 'N/a')],
            ['Kiến tạo/90 phút', player.get('Assists_Per90', 'N/a')],
        ]
        print(tabulate(attack_info, tablefmt='simple'))
        
        # Chuyền bóng
        print("\nCHỈ SỐ CHUYỀN BÓNG:")
        pass_info = [
            ['Đường chuyền hoàn thành', player.get('Passes_Completed', 'N/a')],
            ['Tỉ lệ chính xác (%)', player.get('Pass_Completion_Pct', 'N/a')],
            ['Chuyền bóng quyết định', player.get('Key_Passes', 'N/a')],
        ]
        print(tabulate(pass_info, tablefmt='simple'))
        
        # Phòng thủ
        print("\nCHỈ SỐ PHÒNG THỦ:")
        defense_info = [
            ['Tắc bóng', player.get('Tackles', 'N/a')],
            ['Tắc bóng thành công', player.get('Tackles_Won', 'N/a')],
            ['Chặn bóng', player.get('Blocks', 'N/a')],
            ['Cắt bóng', player.get('Interceptions', 'N/a')],
        ]
        print(tabulate(defense_info, tablefmt='simple'))
        
        # Kỷ luật
        print("\nKỶ LUẬT:")
        card_info = [
            ['Thẻ vàng', player.get('Yellow_Cards', 'N/a')],
            ['Thẻ đỏ', player.get('Red_Cards', 'N/a')],
        ]
        print(tabulate(card_info, tablefmt='simple'))
        print("\n" + "=" * 80)


def display_club_table(players_data, club_name):
    """Hiển thị danh sách cầu thủ của CLB dưới dạng bảng"""
    print("\n" + "=" * 100)
    print(f"DANH SÁCH CẦU THỦ: {club_name}")
    print(f"Tổng số: {len(players_data)} cầu thủ")
    print("=" * 100)
    
    # Chuẩn bị dữ liệu cho bảng
    table_data = []
    total_goals = 0
    total_assists = 0
    
    for i, player in enumerate(players_data, 1):
        table_data.append([
            i,
            player.get('Name', 'N/a')[:25],  # Giới hạn độ dài
            player.get('Position', 'N/a'),
            player.get('Age', 'N/a'),
            player.get('Minutes', 'N/a'),
            player.get('Goals', 'N/a'),
            player.get('Assists', 'N/a')
        ])
        
        # Tính tổng
        try:
            goals = player.get('Goals', '0')
            if goals != 'N/a':
                total_goals += float(goals)
        except:
            pass
        
        try:
            assists = player.get('Assists', '0')
            if assists != 'N/a':
                total_assists += float(assists)
        except:
            pass
    
    # Hiển thị bảng
    headers = ['STT', 'Tên', 'Vị trí', 'Tuổi', 'Số phút', 'Bàn thắng', 'Kiến tạo']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    # Thống kê tổng hợp
    print("\nTỔNG HỢP:")
    print(f"Tổng bàn thắng: {int(total_goals)}")
    print(f"Tổng kiến tạo: {int(total_assists)}")
    print("=" * 100)


def main():
    """Hàm main"""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Tra cứu thông tin cầu thủ Premier League 2024/25',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python lookup.py --name "Mohamed Salah"

Lưu ý:
  - API server phải đang chạy (python api.py)
  - Kết quả được lưu vào Output/Output_II/
        """
    )
    
    parser.add_argument('--name', type=str, help='Tên cầu thủ cần tra cứu')
    parser.add_argument('--club', type=str, help='Tên câu lạc bộ cần tra cứu')
    
    args = parser.parse_args()
    
    # Kiểm tra input
    if not args.name and not args.club:
        parser.print_help()
        print("\nLỗi: Vui lòng cung cấp ít nhất một tham số (--name hoặc --club)")
        sys.exit(1)
    
    if args.name and args.club:
        print("Cảnh báo: Chỉ nên sử dụng một tham số tại một thời điểm.")
        print("Ưu tiên tra cứu theo tên cầu thủ...\n")
    
    # Kiểm tra kết nối API
    print("Đang kiểm tra kết nối API...")
    if not check_api_connection():
        print(f"Không thể kết nối tới API server: {API_BASE_URL}")
        sys.exit(1)
    
    print(f"Đã kết nối: {API_BASE_URL}\n")
    
    # Tra cứu theo tên cầu thủ
    if args.name:
        print(f"Đang tra cứu cầu thủ: {args.name}")
        result = search_player(args.name)
        
        if result.get('success'):
            data = result['data']
            
            # Hiển thị trên màn hình
            if isinstance(data, list):
                print(f"\nTìm thấy {len(data)} cầu thủ có tên tương tự:")
                display_player_table(data)
                
                # Lưu CSV
                filename = f"{sanitize_filename(args.name)}_players.csv"
                filepath = save_to_csv(data, filename, is_player=True)
                
            else:
                print(f"\nTìm thấy cầu thủ: {data.get('Name')}")
                display_player_table(data)
                
                # Lưu CSV
                filename = f"{sanitize_filename(data.get('Name', args.name))}.csv"
                filepath = save_to_csv(data, filename, is_player=True)
            
            if filepath:
                print(f"\nĐã lưu kết quả vào: {filepath}")
        else:
            print(f"\n{result.get('message', 'Không tìm thấy cầu thủ')}")
            sys.exit(1)
    
    # Tra cứu theo câu lạc bộ
    elif args.club:
        print(f"Đang tra cứu câu lạc bộ: {args.club}")
        result = search_club(args.club)
        
        if result.get('success'):
            players = result['data']
            team_name = result.get('team_stats', {}).get('team_name', args.club)
            
            # Hiển thị trên màn hình
            print(f"\nTìm thấy {len(players)} cầu thủ")
            display_club_table(players, team_name)
            
            # Lưu CSV
            filename = f"{sanitize_filename(team_name)}_players.csv"
            filepath = save_to_csv(players, filename, is_player=False)
            
            if filepath:
                print(f"\nĐã lưu kết quả vào: {filepath}")
        else:
            print(f"\n{result.get('message', 'Không tìm thấy câu lạc bộ')}")
            sys.exit(1)
    
    print("\nHoàn thành!")


if __name__ == '__main__':
    main()
