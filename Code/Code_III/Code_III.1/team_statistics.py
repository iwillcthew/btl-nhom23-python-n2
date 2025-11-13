"""
team_statistics.py - Phân tích thống kê cầu thủ theo đội
Tính toán trung vị, trung bình và độ lệch chuẩn của mỗi chỉ số cho từng đội
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# Đường dẫn files
BASE_DIR = Path(__file__).parent.parent.parent
INPUT_FILE = BASE_DIR / "Output" / "Output_I" / "players_stats.csv"
OUTPUT_DIR = BASE_DIR / "Output" / "Output_III"
OUTPUT_FILE = OUTPUT_DIR / "team_statistics.csv"

def load_data(file_path):
    """
    Đọc dữ liệu từ CSV
    
    Args:
        file_path: Đường dẫn file CSV
        
    Returns:
        DataFrame: Dữ liệu cầu thủ
    """
    print(f"📂 Đang đọc dữ liệu từ: {file_path}")
    df = pd.read_csv(file_path)
    print(f"✅ Đã đọc {len(df)} cầu thủ từ {df['Team'].nunique()} đội")
    return df

def convert_to_numeric(df):
    """
    Chuyển đổi các cột sang dạng số, thay thế 'N/a' bằng NaN
    
    Args:
        df: DataFrame đầu vào
        
    Returns:
        DataFrame: DataFrame đã được chuyển đổi
    """
    print("\n🔄 Đang chuyển đổi dữ liệu sang dạng số...")
    
    # Các cột không phải số (giữ nguyên)
    non_numeric_cols = ['Name', 'Nation', 'Team', 'Position']
    
    # Chuyển đổi các cột còn lại sang số
    for col in df.columns:
        if col not in non_numeric_cols:
            # Thay thế 'N/a' bằng NaN, sau đó chuyển sang số
            df[col] = pd.to_numeric(df[col].replace('N/a', np.nan), errors='coerce')
    
    print(f"✅ Đã chuyển đổi {len(df.columns) - len(non_numeric_cols)} cột số")
    return df

def calculate_team_statistics(df):
    """
    Tính toán thống kê (trung vị, trung bình, độ lệch chuẩn) cho mỗi đội
    
    Args:
        df: DataFrame cầu thủ
        
    Returns:
        DataFrame: Thống kê theo đội
    """
    print("\n📊 Đang tính toán thống kê cho từng đội...")
    
    # Lấy các cột số (bỏ qua Name, Nation, Team, Position)
    non_numeric_cols = ['Name', 'Nation', 'Team', 'Position']
    numeric_cols = [col for col in df.columns if col not in non_numeric_cols]
    
    # Nhóm theo đội
    teams = df['Team'].unique()
    print(f"   Số đội: {len(teams)}")
    
    results = []
    
    for team in sorted(teams):
        print(f"   Đang xử lý: {team}...")
        team_data = df[df['Team'] == team]
        
        # Tính thống kê cho từng chỉ số
        for col in numeric_cols:
            # Lấy dữ liệu không null
            values = team_data[col].dropna()
            
            if len(values) > 0:
                # Tính toán các chỉ số thống kê
                median_val = np.median(values)
                mean_val = np.mean(values)
                std_val = np.std(values, ddof=1) if len(values) > 1 else 0
                
                results.append({
                    'Team': team,
                    'Metric': col,
                    'Count': len(values),  # Số cầu thủ có dữ liệu
                    'Median': median_val,
                    'Mean': mean_val,
                    'Std_Dev': std_val
                })
    
    stats_df = pd.DataFrame(results)
    print(f"\n✅ Hoàn thành! Tổng cộng {len(results)} dòng thống kê")
    print(f"   ({len(teams)} đội × {len(numeric_cols)} chỉ số)")
    
    return stats_df

def save_results(df, output_file):
    """
    Lưu kết quả vào file CSV
    
    Args:
        df: DataFrame kết quả
        output_file: Đường dẫn file output
    """
    # Tạo thư mục nếu chưa có
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 Đang lưu kết quả vào: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Đã lưu thành công!")
    print(f"   Kích thước file: {output_file.stat().st_size / 1024:.2f} KB")

def display_summary(stats_df):
    """
    Hiển thị tổng hợp thống kê
    
    Args:
        stats_df: DataFrame thống kê
    """
    print("\n" + "="*70)
    print("📈 TỔNG HỢP KẾT QUẢ")
    print("="*70)
    
    teams = stats_df['Team'].unique()
    metrics = stats_df['Metric'].unique()
    
    print(f"\n🏆 Số đội: {len(teams)}")
    print(f"📊 Số chỉ số: {len(metrics)}")
    print(f"📝 Tổng số dòng: {len(stats_df)}")
    
    print(f"\n🔢 Các chỉ số phân tích:")
    print(f"   - Trung vị (Median)")
    print(f"   - Trung bình (Mean)")
    print(f"   - Độ lệch chuẩn (Std_Dev)")
    
    print(f"\n📋 Danh sách đội:")
    for i, team in enumerate(sorted(teams), 1):
        team_count = len(stats_df[stats_df['Team'] == team])
        print(f"   {i:2d}. {team:20s} - {team_count} chỉ số")
    
    # Ví dụ một số kết quả
    print(f"\n📊 VÍ DỤ KẾT QUẢ (Goals):")
    print("-" * 70)
    goals_stats = stats_df[stats_df['Metric'] == 'Goals'].sort_values('Mean', ascending=False).head(5)
    if len(goals_stats) > 0:
        print(f"{'Đội':<20} {'Count':<8} {'Median':<10} {'Mean':<10} {'Std_Dev':<10}")
        print("-" * 70)
        for _, row in goals_stats.iterrows():
            print(f"{row['Team']:<20} {row['Count']:<8.0f} {row['Median']:<10.2f} {row['Mean']:<10.2f} {row['Std_Dev']:<10.2f}")

def main():
    """Hàm chính"""
    print("="*70)
    print("⚽ PHÂN TÍCH THỐNG KÊ CẦU THỦ THEO ĐỘI")
    print("   Premier League 2024-2025")
    print("="*70)
    
    try:
        # Bước 1: Đọc dữ liệu
        df = load_data(INPUT_FILE)
        
        # Bước 2: Chuyển đổi sang dạng số
        df = convert_to_numeric(df)
        
        # Bước 3: Tính toán thống kê
        stats_df = calculate_team_statistics(df)
        
        # Bước 4: Lưu kết quả
        save_results(stats_df, OUTPUT_FILE)
        
        # Bước 5: Hiển thị tổng hợp
        display_summary(stats_df)
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH!")
        print("="*70)
        print(f"\n📁 File kết quả: {OUTPUT_FILE}")
        print(f"📊 Mở file CSV để xem chi tiết thống kê của từng đội")
        
    except FileNotFoundError as e:
        print(f"\n❌ Lỗi: Không tìm thấy file")
        print(f"   {e}")
        print(f"\n💡 Vui lòng chạy scraper (Code_I) trước để tạo dữ liệu")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
