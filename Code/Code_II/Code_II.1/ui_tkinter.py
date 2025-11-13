"""
ui_tkinter.py - Giao diện Tkinter kết nối với Flask API
Phần II.1 - Tra cứu thông tin cầu thủ
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json

# URL của API server
API_BASE_URL = "http://127.0.0.1:5000"


class FootballStatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽ Football Stats - Premier League 2024/25")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        
        # Màu sắc theme
        self.colors = {
            'primary': '#1E3A5F',
            'success': '#4CAF50',
            'danger': '#f44336',
            'info': '#2196F3',
            'bg': '#F5F5F5',
            'white': '#FFFFFF'
        }
        
        # Kiểm tra kết nối API
        self.check_and_setup_connection()
        
        # Tạo giao diện
        self.create_widgets()
        
        # Load danh sách teams
        self.load_teams()
    
    def check_and_setup_connection(self):
        """Kiểm tra kết nối API khi khởi động"""
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=2)
            if response.status_code == 200:
                self.api_connected = True
                return
        except:
            pass
        
        # Nếu không kết nối được
        self.api_connected = False
        result = messagebox.askyesno(
            "⚠️ Lỗi kết nối API", 
            "Không thể kết nối tới API server!\n\n"
            f"URL: {API_BASE_URL}\n\n"
            "❗ Vui lòng chạy API server trước:\n"
            "   cd Code/Code_II/Code_II.1\n"
            "   python api.py\n\n"
            "Bạn có muốn tiếp tục không?\n"
            "(Ứng dụng sẽ không hoạt động nếu API không chạy)"
        )
        
        if not result:
            self.root.destroy()
            exit()
    
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="⚽ FOOTBALL STATS - PREMIER LEAGUE 2024/25",
            font=("Arial", 18, "bold"),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=15)
        
        # Connection Status
        status_color = "#90EE90" if self.api_connected else "#FF6B6B"
        status_text = f"🟢 Connected: {API_BASE_URL}" if self.api_connected else "🔴 Disconnected"
        
        self.status_label = tk.Label(
            header_frame,
            text=status_text,
            font=("Arial", 9),
            bg=self.colors['primary'],
            fg=status_color
        )
        self.status_label.pack()
        
        # Main Container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Notebook (Tabs)
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Tra cứu theo tên cầu thủ
        self.create_player_tab()
        
        # Tab 2: Tra cứu theo câu lạc bộ
        self.create_team_tab()
        
        # Tab 3: API Info
        self.create_api_info_tab()
    
    def create_player_tab(self):
        """Tab tra cứu theo tên cầu thủ"""
        tab = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(tab, text="  🔍 Tra cứu Cầu Thủ  ")
        
        # Search Frame
        search_frame = tk.Frame(tab, bg=self.colors['white'], pady=20)
        search_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(
            search_frame,
            text="Tên cầu thủ:",
            font=("Arial", 12, "bold"),
            bg=self.colors['white']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.player_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            width=35,
            relief=tk.SOLID,
            bd=1
        )
        self.player_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        self.player_entry.bind('<Return>', lambda e: self.search_player())
        
        # Buttons
        tk.Button(
            search_frame,
            text="🔍 Tìm kiếm",
            font=("Arial", 11, "bold"),
            bg=self.colors['success'],
            fg=self.colors['white'],
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.search_player
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            search_frame,
            text="🗑️ Xóa",
            font=("Arial", 11),
            bg=self.colors['danger'],
            fg=self.colors['white'],
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.clear_player_result
        ).pack(side=tk.LEFT)
        
        # Result Frame
        result_container = tk.LabelFrame(
            tab,
            text="  📊 Kết quả  ",
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            relief=tk.SOLID,
            bd=1
        )
        result_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.player_text = scrolledtext.ScrolledText(
            result_container,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors['bg'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.player_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_team_tab(self):
        """Tab tra cứu theo câu lạc bộ"""
        tab = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(tab, text="  🏆 Tra cứu Câu Lạc Bộ  ")
        
        # Select Frame
        select_frame = tk.Frame(tab, bg=self.colors['white'], pady=20)
        select_frame.pack(fill=tk.X, padx=20)
        
        tk.Label(
            select_frame,
            text="Câu lạc bộ:",
            font=("Arial", 12, "bold"),
            bg=self.colors['white']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.team_combo = ttk.Combobox(
            select_frame,
            font=("Arial", 12),
            width=32,
            state="readonly"
        )
        self.team_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Buttons
        tk.Button(
            select_frame,
            text="🔍 Xem danh sách",
            font=("Arial", 11, "bold"),
            bg=self.colors['info'],
            fg=self.colors['white'],
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.search_team
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            select_frame,
            text="🗑️ Xóa",
            font=("Arial", 11),
            bg=self.colors['danger'],
            fg=self.colors['white'],
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=self.clear_team_result
        ).pack(side=tk.LEFT)
        
        # Result Frame
        result_container = tk.LabelFrame(
            tab,
            text="  📋 Danh sách cầu thủ  ",
            font=("Arial", 11, "bold"),
            bg=self.colors['white'],
            relief=tk.SOLID,
            bd=1
        )
        result_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.team_text = scrolledtext.ScrolledText(
            result_container,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors['bg'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.team_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_api_info_tab(self):
        """Tab thông tin API"""
        tab = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(tab, text="  ℹ️ API Info  ")
        
        info_container = tk.Frame(tab, bg=self.colors['white'], pady=20)
        info_container.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Title
        tk.Label(
            info_container,
            text="📡 Thông tin API Server",
            font=("Arial", 16, "bold"),
            bg=self.colors['white']
        ).pack(pady=(0, 20))
        
        # Info Text
        self.api_info_text = scrolledtext.ScrolledText(
            info_container,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors['bg'],
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.api_info_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Refresh Button
        tk.Button(
            info_container,
            text="🔄 Làm mới thông tin",
            font=("Arial", 11, "bold"),
            bg=self.colors['info'],
            fg=self.colors['white'],
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.load_api_info
        ).pack()
        
        # Load initial info
        self.load_api_info()
    
    def load_teams(self):
        """Load danh sách câu lạc bộ từ API"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/teams", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    teams = [item['team'] for item in data['data']]
                    self.team_combo['values'] = teams
                    if teams:
                        self.team_combo.current(0)
        except Exception as e:
            print(f"Lỗi load teams: {e}")
    
    def search_player(self):
        """Tìm kiếm cầu thủ"""
        player_name = self.player_entry.get().strip()
        
        if not player_name:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng nhập tên cầu thủ!")
            return
        
        self.player_text.delete(1.0, tk.END)
        self.player_text.insert(tk.END, "⏳ Đang tìm kiếm...\n")
        self.root.update()
        
        try:
            url = f"{API_BASE_URL}/api/player/{player_name}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    if isinstance(data['data'], list):
                        self.display_multiple_players(data)
                    else:
                        self.display_player_detail(data['data'])
                else:
                    self.show_error(data.get('message', 'Không tìm thấy'))
            elif response.status_code == 404:
                data = response.json()
                self.show_error(data.get('message', 'Không tìm thấy cầu thủ'))
            else:
                self.show_error(f"Lỗi HTTP: {response.status_code}")
                
        except requests.exceptions.Timeout:
            messagebox.showerror("❌ Lỗi", "Kết nối timeout! API server có thể quá chậm.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "❌ Lỗi kết nối",
                "Không thể kết nối tới API!\n\n"
                "Vui lòng kiểm tra:\n"
                "1. API server đang chạy (python api.py)\n"
                f"2. URL đúng: {API_BASE_URL}"
            )
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Lỗi không xác định:\n{str(e)}")
    
    def display_multiple_players(self, data):
        """Hiển thị nhiều cầu thủ tìm được"""
        self.player_text.delete(1.0, tk.END)
        
        self.player_text.insert(tk.END, f"🔍 {data.get('message', 'Kết quả tìm kiếm')}\n\n")
        
        players = data.get('data', [])
        for i, player in enumerate(players, 1):
            self.player_text.insert(tk.END, f"{i}. ")
            self.player_text.insert(tk.END, f"{player['Name']}", "bold")
            self.player_text.insert(tk.END, f" - {player['Team']} ({player['Position']})\n")
            self.player_text.insert(
                tk.END,
                f"   ⚽ Bàn thắng: {player['Goals']} | 🎯 Kiến tạo: {player['Assists']} | "
                f"⏱️ Số phút: {player['Minutes']}\n\n"
            )
        
        self.player_text.tag_config("bold", font=("Consolas", 10, "bold"))
    
    def display_player_detail(self, player):
        """Hiển thị chi tiết cầu thủ"""
        self.player_text.delete(1.0, tk.END)
        
        # Header
        self.player_text.insert(tk.END, "=" * 85 + "\n")
        self.player_text.insert(tk.END, f"⚽ THÔNG TIN CẦU THỦ: {player['Name']}\n", "title")
        self.player_text.insert(tk.END, "=" * 85 + "\n\n")
        
        # Thông tin cơ bản
        self.player_text.insert(tk.END, "📋 THÔNG TIN CƠ BẢN:\n", "section")
        self.player_text.insert(tk.END, "-" * 85 + "\n")
        self.add_info_row("Tên", player.get('Name', 'N/a'))
        self.add_info_row("Quốc tịch", player.get('Nation', 'N/a'))
        self.add_info_row("Câu lạc bộ", player.get('Team', 'N/a'))
        self.add_info_row("Vị trí", player.get('Position', 'N/a'))
        self.add_info_row("Tuổi", player.get('Age', 'N/a'))
        
        # Thời gian thi đấu
        self.player_text.insert(tk.END, "\n⏱️ THỜI GIAN THI ĐẤU:\n", "section")
        self.player_text.insert(tk.END, "-" * 85 + "\n")
        self.add_info_row("Số trận", player.get('Matches_Played', 'N/a'))
        self.add_info_row("Số trận đá chính", player.get('Starts', 'N/a'))
        self.add_info_row("Số phút", player.get('Minutes', 'N/a'))
        
        # Tấn công
        self.player_text.insert(tk.END, "\n⚡ CHỈ SỐ TẤN CÔNG:\n", "section")
        self.player_text.insert(tk.END, "-" * 85 + "\n")
        self.add_info_row("Bàn thắng", player.get('Goals', 'N/a'))
        self.add_info_row("Kiến tạo", player.get('Assists', 'N/a'))
        self.add_info_row("xG (Expected Goals)", player.get('xG', 'N/a'))
        self.add_info_row("xAG (Expected Assists)", player.get('xAG', 'N/a'))
        self.add_info_row("Bàn thắng/90 phút", player.get('Goals_Per90', 'N/a'))
        self.add_info_row("Kiến tạo/90 phút", player.get('Assists_Per90', 'N/a'))
        
        # Chuyền bóng
        self.player_text.insert(tk.END, "\n🎯 CHỈ SỐ CHUYỀN BÓNG:\n", "section")
        self.player_text.insert(tk.END, "-" * 85 + "\n")
        self.add_info_row("Đường chuyền hoàn thành", player.get('Passes_Completed', 'N/a'))
        self.add_info_row("Tỉ lệ chính xác (%)", player.get('Pass_Completion_Pct', 'N/a'))
        self.add_info_row("Chuyền bóng quyết định", player.get('Key_Passes', 'N/a'))
        
        # Phòng thủ
        self.player_text.insert(tk.END, "\n🛡️ CHỈ SỐ PHÒNG THỦ:\n", "section")
        self.player_text.insert(tk.END, "-" * 85 + "\n")
        self.add_info_row("Tắc bóng", player.get('Tackles', 'N/a'))
        self.add_info_row("Tắc bóng thành công", player.get('Tackles_Won', 'N/a'))
        self.add_info_row("Chặn bóng", player.get('Blocks', 'N/a'))
        self.add_info_row("Cắt bóng", player.get('Interceptions', 'N/a'))
        
        # Kỷ luật
        self.player_text.insert(tk.END, "\n🟨 KỶ LUẬT:\n", "section")
        self.player_text.insert(tk.END, "-" * 85 + "\n")
        self.add_info_row("Thẻ vàng", player.get('Yellow_Cards', 'N/a'))
        self.add_info_row("Thẻ đỏ", player.get('Red_Cards', 'N/a'))
        
        self.player_text.insert(tk.END, "\n" + "=" * 85 + "\n")
        self.player_text.insert(tk.END, f"\n💡 Dữ liệu từ API: {API_BASE_URL}\n", "footer")
        
        # Configure tags
        self.player_text.tag_config("title", font=("Consolas", 11, "bold"))
        self.player_text.tag_config("section", font=("Consolas", 10, "bold"))
        self.player_text.tag_config("footer", font=("Consolas", 9, "italic"))
    
    def add_info_row(self, label, value):
        """Helper để thêm dòng thông tin"""
        self.player_text.insert(tk.END, f"{label:30s}: {value}\n")
    
    def search_team(self):
        """Tìm kiếm cầu thủ theo CLB"""
        team_name = self.team_combo.get().strip()
        
        if not team_name:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn câu lạc bộ!")
            return
        
        self.team_text.delete(1.0, tk.END)
        self.team_text.insert(tk.END, "⏳ Đang tải dữ liệu...\n")
        self.root.update()
        
        try:
            url = f"{API_BASE_URL}/api/team/{team_name}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.display_team_detail(data)
                else:
                    self.team_text.delete(1.0, tk.END)
                    self.team_text.insert(tk.END, f"❌ {data.get('message', 'Không tìm thấy')}\n")
            elif response.status_code == 404:
                data = response.json()
                self.team_text.delete(1.0, tk.END)
                self.team_text.insert(tk.END, f"❌ {data.get('message', 'Không tìm thấy')}\n")
            else:
                self.team_text.delete(1.0, tk.END)
                self.team_text.insert(tk.END, f"❌ Lỗi HTTP: {response.status_code}\n")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "❌ Lỗi kết nối",
                "Không thể kết nối tới API!\n\nVui lòng chạy API server trước."
            )
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Lỗi không xác định:\n{str(e)}")
    
    def display_team_detail(self, data):
        """Hiển thị danh sách cầu thủ của CLB"""
        self.team_text.delete(1.0, tk.END)
        
        team_stats = data.get('team_stats', {})
        players = data.get('data', [])
        
        # Header
        self.team_text.insert(tk.END, "=" * 105 + "\n")
        self.team_text.insert(tk.END, f"🏆 {team_stats.get('team_name', 'N/a')}\n", "title")
        self.team_text.insert(tk.END, f"📊 Tổng số: {team_stats.get('total_players', 0)} cầu thủ\n")
        self.team_text.insert(tk.END, "=" * 105 + "\n\n")
        
        # Thống kê vị trí
        positions = team_stats.get('positions', {})
        if positions:
            self.team_text.insert(tk.END, "📈 PHÂN BỐ VỊ TRÍ:\n", "section")
            self.team_text.insert(tk.END, "-" * 105 + "\n")
            for pos, count in sorted(positions.items()):
                self.team_text.insert(tk.END, f"  {pos:10s}: {count} cầu thủ\n")
            self.team_text.insert(tk.END, "\n")
        
        # Bảng cầu thủ
        self.team_text.insert(tk.END, "👥 DANH SÁCH CẦU THỦ:\n", "section")
        self.team_text.insert(tk.END, "-" * 105 + "\n")
        
        # Header bảng
        header = f"{'STT':<5} {'TÊN':<26} {'VỊ TRÍ':<8} {'TUỔI':<6} {'PHÚT':<10} {'BÀN THẮNG':<12} {'KIẾN TẠO':<10}\n"
        self.team_text.insert(tk.END, header, "bold")
        self.team_text.insert(tk.END, "-" * 105 + "\n")
        
        # Dữ liệu
        total_goals = 0
        total_assists = 0
        
        for i, player in enumerate(players, 1):
            name = player['Name'][:24] + '..' if len(player['Name']) > 24 else player['Name']
            row = f"{i:<5} {name:<26} {player['Position']:<8} {player['Age']:<6} "
            row += f"{player['Minutes']:<10} {player['Goals']:<12} {player['Assists']:<10}\n"
            self.team_text.insert(tk.END, row)
            
            try:
                if player['Goals'] != 'N/a':
                    total_goals += float(player['Goals'])
                if player['Assists'] != 'N/a':
                    total_assists += float(player['Assists'])
            except:
                pass
        
        # Footer
        self.team_text.insert(tk.END, "\n" + "=" * 105 + "\n")
        self.team_text.insert(tk.END, "📊 TỔNG HỢP:\n", "section")
        self.team_text.insert(tk.END, f"⚽ Tổng bàn thắng: {int(total_goals)}\n")
        self.team_text.insert(tk.END, f"🎯 Tổng kiến tạo: {int(total_assists)}\n")
        self.team_text.insert(tk.END, f"\n💡 Dữ liệu từ API: {API_BASE_URL}\n", "footer")
        
        # Configure tags
        self.team_text.tag_config("title", font=("Consolas", 12, "bold"))
        self.team_text.tag_config("section", font=("Consolas", 10, "bold"))
        self.team_text.tag_config("bold", font=("Consolas", 10, "bold"))
        self.team_text.tag_config("footer", font=("Consolas", 9, "italic"))
    
    def load_api_info(self):
        """Load thông tin API"""
        self.api_info_text.delete(1.0, tk.END)
        
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                self.api_info_text.insert(tk.END, "=" * 85 + "\n")
                self.api_info_text.insert(tk.END, "📡 API SERVER INFORMATION\n", "title")
                self.api_info_text.insert(tk.END, "=" * 85 + "\n\n")
                
                self.api_info_text.insert(tk.END, f"🌐 Base URL    : {API_BASE_URL}\n")
                self.api_info_text.insert(tk.END, f"📦 Version     : {data.get('version', 'N/a')}\n")
                self.api_info_text.insert(tk.END, f"📝 Description : {data.get('message', 'N/a')}\n\n")
                
                self.api_info_text.insert(tk.END, "=" * 85 + "\n")
                self.api_info_text.insert(tk.END, "📋 ENDPOINTS:\n", "section")
                self.api_info_text.insert(tk.END, "=" * 85 + "\n\n")
                
                endpoints = data.get('endpoints', {})
                for endpoint, desc in endpoints.items():
                    self.api_info_text.insert(tk.END, f"🔹 {endpoint}\n", "bold")
                    self.api_info_text.insert(tk.END, f"   → {desc}\n\n")
                
                self.api_info_text.insert(tk.END, "=" * 85 + "\n")
                self.api_info_text.insert(tk.END, "💡 EXAMPLES:\n", "section")
                self.api_info_text.insert(tk.END, "=" * 85 + "\n\n")
                
                examples = data.get('examples', {})
                for name, url in examples.items():
                    self.api_info_text.insert(tk.END, f"🔸 {name.capitalize()}:\n")
                    self.api_info_text.insert(tk.END, f"   {API_BASE_URL}{url}\n\n")
                
                self.api_info_text.insert(tk.END, "=" * 85 + "\n")
                self.api_info_text.insert(tk.END, "✅ API Server đang hoạt động bình thường!\n", "success")
                
                # Update status
                self.status_label.config(
                    text=f"🟢 Connected: {API_BASE_URL}",
                    fg="#90EE90"
                )
                self.api_connected = True
                
            else:
                self.show_api_error(f"HTTP Error: {response.status_code}")
                
        except Exception as e:
            self.show_api_error(str(e))
    
    def show_api_error(self, error):
        """Hiển thị lỗi API"""
        self.api_info_text.insert(tk.END, "=" * 85 + "\n")
        self.api_info_text.insert(tk.END, "❌ CONNECTION ERROR\n", "error")
        self.api_info_text.insert(tk.END, "=" * 85 + "\n\n")
        self.api_info_text.insert(tk.END, f"Lỗi: {error}\n\n")
        self.api_info_text.insert(tk.END, "💡 Vui lòng kiểm tra:\n")
        self.api_info_text.insert(tk.END, "   1. API server đang chạy (python api.py)\n")
        self.api_info_text.insert(tk.END, f"   2. URL đúng: {API_BASE_URL}\n")
        self.api_info_text.insert(tk.END, "   3. Không có firewall chặn kết nối\n")
        
        self.status_label.config(text="🔴 Disconnected", fg="#FF6B6B")
        self.api_connected = False
    
    def show_error(self, message):
        """Hiển thị lỗi trong player text"""
        self.player_text.delete(1.0, tk.END)
        self.player_text.insert(tk.END, f"❌ {message}\n\n")
        self.player_text.insert(tk.END, "💡 Gợi ý: Kiểm tra lại tên cầu thủ hoặc thử tìm với từ khóa ngắn hơn.")
    
    def clear_player_result(self):
        """Xóa kết quả tìm kiếm cầu thủ"""
        self.player_entry.delete(0, tk.END)
        self.player_text.delete(1.0, tk.END)
    
    def clear_team_result(self):
        """Xóa kết quả tìm kiếm team"""
        self.team_text.delete(1.0, tk.END)


def main():
    """Main function"""
    root = tk.Tk()
    app = FootballStatsApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
