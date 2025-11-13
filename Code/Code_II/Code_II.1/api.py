"""
api.py - Flask REST API cho phần II.1
Cung cấp API tra cứu thông tin cầu thủ từ database
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Cho phép CORS để frontend có thể gọi API

# Đường dẫn tới database
DATABASE_PATH = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', '..', 'Output', 'Output_I', 'football_stats.db'
)


def get_db_connection():
    """Tạo kết nối tới database SQLite"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Trả về dict thay vì tuple
    return conn


def row_to_dict(row):
    """Chuyển đổi SQLite Row object thành dictionary"""
    return {key: row[key] for key in row.keys()}


@app.route('/')
def home():
    """Trang chủ API - hướng dẫn sử dụng"""
    return jsonify({
        'message': 'Football Stats API - Premier League 2024-2025',
        'version': '1.0',
        'endpoints': {
            'GET /api/player/<name>': 'Tra cứu cầu thủ theo tên',
            'GET /api/team/<team_name>': 'Tra cứu cầu thủ theo câu lạc bộ',
            'GET /api/players': 'Lấy danh sách tất cả cầu thủ (có phân trang)',
            'GET /api/teams': 'Lấy danh sách tất cả câu lạc bộ'
        },
        'examples': {
            'player': '/api/player/Mohamed Salah',
            'team': '/api/team/Liverpool',
            'players': '/api/players?page=1&per_page=20',
            'teams': '/api/teams'
        }
    })


@app.route('/api/player/<name>')
def get_player_by_name(name):
    """
    Tra cứu cầu thủ theo tên
    
    Args:
        name: Tên cầu thủ (có thể tìm kiếm gần đúng)
        
    Returns:
        JSON: Thông tin đầy đủ của cầu thủ hoặc danh sách cầu thủ tương tự
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Tìm kiếm chính xác trước
        cursor.execute(
            'SELECT * FROM players WHERE LOWER(Name) = LOWER(?)',
            (name,)
        )
        player = cursor.fetchone()
        
        # Nếu không tìm thấy, tìm kiếm gần đúng
        if not player:
            cursor.execute(
                'SELECT * FROM players WHERE LOWER(Name) LIKE LOWER(?)',
                (f'%{name}%',)
            )
            players = cursor.fetchall()
            conn.close()
            
            if not players:
                return jsonify({
                    'success': False,
                    'message': f'Không tìm thấy cầu thủ có tên "{name}"',
                    'suggestion': 'Vui lòng kiểm tra lại tên cầu thủ'
                }), 404
            
            # Trả về danh sách cầu thủ tương tự
            return jsonify({
                'success': True,
                'message': f'Tìm thấy {len(players)} cầu thủ có tên tương tự',
                'count': len(players),
                'data': [row_to_dict(p) for p in players]
            })
        
        # Trả về thông tin cầu thủ
        conn.close()
        return jsonify({
            'success': True,
            'message': f'Thông tin cầu thủ "{player["Name"]}"',
            'data': row_to_dict(player)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Lỗi khi truy vấn database'
        }), 500


@app.route('/api/team/<team_name>')
def get_players_by_team(team_name):
    """
    Tra cứu danh sách cầu thủ theo câu lạc bộ
    
    Args:
        team_name: Tên câu lạc bộ
        
    Returns:
        JSON: Danh sách tất cả cầu thủ thuộc câu lạc bộ đó
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Tìm kiếm câu lạc bộ (không phân biệt hoa thường)
        cursor.execute(
            'SELECT * FROM players WHERE LOWER(Team) = LOWER(?) ORDER BY Name',
            (team_name,)
        )
        players = cursor.fetchall()
        
        # Nếu không tìm thấy, thử tìm kiếm gần đúng
        if not players:
            cursor.execute(
                'SELECT * FROM players WHERE LOWER(Team) LIKE LOWER(?) ORDER BY Name',
                (f'%{team_name}%',)
            )
            players = cursor.fetchall()
        
        conn.close()
        
        if not players:
            # Lấy danh sách tất cả các đội để gợi ý
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT Team FROM players ORDER BY Team')
            teams = [row['Team'] for row in cursor.fetchall()]
            conn.close()
            
            return jsonify({
                'success': False,
                'message': f'Không tìm thấy câu lạc bộ "{team_name}"',
                'available_teams': teams
            }), 404
        
        # Thống kê tổng quan
        team_stats = {
            'team_name': players[0]['Team'],
            'total_players': len(players),
            'positions': {}
        }
        
        # Đếm số lượng cầu thủ theo vị trí
        for player in players:
            position = player['Position']
            team_stats['positions'][position] = team_stats['positions'].get(position, 0) + 1
        
        return jsonify({
            'success': True,
            'message': f'Danh sách cầu thủ của {players[0]["Team"]}',
            'team_stats': team_stats,
            'data': [row_to_dict(p) for p in players]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Lỗi khi truy vấn database'
        }), 500


@app.route('/api/players')
def get_all_players():
    """
    Lấy danh sách tất cả cầu thủ (có phân trang)
    
    Query Parameters:
        page: Số trang (mặc định 1)
        per_page: Số lượng mỗi trang (mặc định 20, tối đa 100)
        
    Returns:
        JSON: Danh sách cầu thủ với thông tin phân trang
    """
    try:
        # Lấy tham số phân trang
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Giới hạn per_page
        per_page = min(per_page, 100)
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Đếm tổng số cầu thủ
        cursor.execute('SELECT COUNT(*) as count FROM players')
        total = cursor.fetchone()['count']
        
        # Lấy dữ liệu với phân trang
        cursor.execute(
            'SELECT * FROM players ORDER BY Name LIMIT ? OFFSET ?',
            (per_page, offset)
        )
        players = cursor.fetchall()
        conn.close()
        
        # Tính toán thông tin phân trang
        total_pages = (total + per_page - 1) // per_page
        
        return jsonify({
            'success': True,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            },
            'data': [row_to_dict(p) for p in players]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Lỗi khi truy vấn database'
        }), 500


@app.route('/api/teams')
def get_all_teams():
    """
    Lấy danh sách tất cả các câu lạc bộ
    
    Returns:
        JSON: Danh sách câu lạc bộ với số lượng cầu thủ
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                Team,
                COUNT(*) as player_count
            FROM players
            GROUP BY Team
            ORDER BY Team
        ''')
        teams = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Danh sách {len(teams)} câu lạc bộ',
            'total_teams': len(teams),
            'data': [
                {
                    'team': row['Team'],
                    'player_count': row['player_count']
                }
                for row in teams
            ]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Lỗi khi truy vấn database'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Xử lý lỗi 404"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'API endpoint bạn đang tìm không tồn tại. Vui lòng truy cập / để xem danh sách API.'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Xử lý lỗi 500"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'Đã xảy ra lỗi trên server. Vui lòng thử lại sau.'
    }), 500


if __name__ == '__main__':
    # Kiểm tra database tồn tại
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Lỗi: Không tìm thấy database tại {DATABASE_PATH}")
        print("Vui lòng chạy scraper_fbref.py trước để tạo database.")
    else:
        print("=" * 60)
        print("🚀 FLASK REST API SERVER")
        print("=" * 60)
        print(f"📂 Database: {DATABASE_PATH}")
        print(f"🌐 Server: http://127.0.0.1:5000")
        print(f"📖 API Docs: http://127.0.0.1:5000")
        print("=" * 60)
        print("\nNhấn Ctrl+C để dừng server\n")
        
        # Chạy server
        app.run(debug=True, host='0.0.0.0', port=5000)
