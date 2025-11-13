"""
best_team_analysis.py - Phân tích đội bóng tốt nhất
Tìm đội có chỉ số cao nhất ở mỗi metric và xác định đội có phong độ tốt nhất tổng thể
"""

import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

# Đường dẫn files
BASE_DIR = Path(__file__).parent.parent.parent.parent
INPUT_FILE = BASE_DIR / "Output" / "Output_III" / "team_statistics.csv"
OUTPUT_DIR = BASE_DIR / "Output" / "Output_III"
OUTPUT_FILE = OUTPUT_DIR / "best_teams_by_metric.csv"

# Các chỉ số quan trọng và trọng số đánh giá
ATTACKING_METRICS = {
    'Goals': 10,
    'Assists': 8,
    'xG': 9,
    'Goals_Per90': 8,
    'SoT_Pct': 6,
    'Key_Passes': 7,
    'Passes_Into_Final_Third': 6,
    'Passes_Into_Penalty_Area': 7,
    'Progressive_Passes': 6,
    'SCA': 7,
    'GCA': 8
}

DEFENSIVE_METRICS = {
    'Tackles': 7,
    'Tackles_Won': 8,
    'Interceptions': 7,
    'Blocks': 6,
    'Ball_Recoveries': 6,
    'Aerials_Won_Pct': 5
}

POSSESSION_METRICS = {
    'Pass_Completion_Pct': 6,
    'Progressive_Carries': 6,
    'Touches': 5,
    'Carries_Into_Final_Third': 6
}

GOALKEEPER_METRICS = {
    'Save_Pct': 8,
    'CS_Pct': 7
}

def load_statistics(file_path):
    """
    Đọc dữ liệu thống kê từ CSV
    
    Args:
        file_path: Đường dẫn file CSV
        
    Returns:
        DataFrame: Dữ liệu thống kê
    """
    print(f"📂 Đang đọc dữ liệu từ: {file_path}")
    df = pd.read_csv(file_path)
    print(f"✅ Đã đọc {len(df)} dòng thống kê")
    print(f"   {df['Team'].nunique()} đội, {df['Metric'].nunique()} chỉ số")
    return df

def find_best_teams_by_metric(df):
    """
    Tìm đội có chỉ số trung bình cao nhất cho mỗi metric
    
    Args:
        df: DataFrame thống kê
        
    Returns:
        DataFrame: Đội tốt nhất cho mỗi chỉ số
    """
    print("\n🏆 Đang tìm đội tốt nhất cho từng chỉ số...")
    
    best_teams = []
    metrics = df['Metric'].unique()
    
    for metric in sorted(metrics):
        metric_data = df[df['Metric'] == metric]
        
        # Tìm đội có Mean cao nhất
        best_row = metric_data.loc[metric_data['Mean'].idxmax()]
        
        best_teams.append({
            'Metric': metric,
            'Best_Team': best_row['Team'],
            'Mean': best_row['Mean'],
            'Median': best_row['Median'],
            'Std_Dev': best_row['Std_Dev'],
            'Count': best_row['Count']
        })
    
    print(f"✅ Đã phân tích {len(best_teams)} chỉ số")
    return pd.DataFrame(best_teams)

def calculate_overall_score(df, best_teams_df):
    """
    Tính điểm tổng thể cho mỗi đội dựa trên các chỉ số quan trọng
    
    Args:
        df: DataFrame thống kê gốc
        best_teams_df: DataFrame đội tốt nhất theo metric
        
    Returns:
        DataFrame: Điểm tổng thể của các đội
    """
    print("\n📊 Đang tính điểm tổng thể cho các đội...")
    
    teams = df['Team'].unique()
    team_scores = []
    
    # Tổng hợp tất cả metrics và trọng số
    all_metrics = {
        **ATTACKING_METRICS,
        **DEFENSIVE_METRICS,
        **POSSESSION_METRICS,
        **GOALKEEPER_METRICS
    }
    
    for team in teams:
        team_data = df[df['Team'] == team]
        total_score = 0
        max_possible_score = 0
        metric_scores = {}
        
        for metric, weight in all_metrics.items():
            metric_row = team_data[team_data['Metric'] == metric]
            
            if len(metric_row) > 0:
                # Lấy mean của đội này
                team_mean = metric_row.iloc[0]['Mean']
                
                # Lấy mean cao nhất của metric này
                best_mean = df[df['Metric'] == metric]['Mean'].max()
                
                # Tính điểm chuẩn hóa (0-1) × trọng số
                if best_mean > 0:
                    normalized_score = (team_mean / best_mean) * weight
                    total_score += normalized_score
                    metric_scores[metric] = normalized_score
                
                max_possible_score += weight
        
        # Tính phần trăm
        if max_possible_score > 0:
            score_percentage = (total_score / max_possible_score) * 100
        else:
            score_percentage = 0
        
        team_scores.append({
            'Team': team,
            'Total_Score': total_score,
            'Max_Score': max_possible_score,
            'Score_Percentage': score_percentage,
            'Attacking_Score': sum(metric_scores.get(m, 0) for m in ATTACKING_METRICS),
            'Defensive_Score': sum(metric_scores.get(m, 0) for m in DEFENSIVE_METRICS),
            'Possession_Score': sum(metric_scores.get(m, 0) for m in POSSESSION_METRICS),
            'GK_Score': sum(metric_scores.get(m, 0) for m in GOALKEEPER_METRICS)
        })
    
    scores_df = pd.DataFrame(team_scores).sort_values('Score_Percentage', ascending=False)
    print(f"✅ Đã tính điểm cho {len(teams)} đội")
    
    return scores_df

def analyze_best_team(scores_df, best_teams_df):
    """
    Phân tích chi tiết đội tốt nhất
    
    Args:
        scores_df: DataFrame điểm số
        best_teams_df: DataFrame đội tốt nhất theo metric
        
    Returns:
        dict: Thông tin đội tốt nhất
    """
    print("\n🥇 Đang phân tích đội tốt nhất...")
    
    best_team = scores_df.iloc[0]
    team_name = best_team['Team']
    
    # Đếm số lần đội này dẫn đầu các chỉ số
    leadership_count = len(best_teams_df[best_teams_df['Best_Team'] == team_name])
    
    # Tìm các chỉ số mà đội này dẫn đầu
    leading_metrics = best_teams_df[best_teams_df['Best_Team'] == team_name]['Metric'].tolist()
    
    analysis = {
        'team': team_name,
        'score_percentage': best_team['Score_Percentage'],
        'total_score': best_team['Total_Score'],
        'attacking_score': best_team['Attacking_Score'],
        'defensive_score': best_team['Defensive_Score'],
        'possession_score': best_team['Possession_Score'],
        'gk_score': best_team['GK_Score'],
        'leadership_count': leadership_count,
        'leading_metrics': leading_metrics
    }
    
    return analysis

def save_results_with_conclusion(best_teams_df, scores_df, best_team_analysis, output_file):
    """
    Lưu kết quả với dòng kết luận cuối cùng
    
    Args:
        best_teams_df: DataFrame đội tốt nhất theo metric
        scores_df: DataFrame điểm tổng thể
        best_team_analysis: Phân tích đội tốt nhất
        output_file: Đường dẫn file output
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n💾 Đang lưu kết quả vào: {output_file}")
    
    # Gộp hai DataFrame
    # Phần 1: Best teams by metric
    result_df = best_teams_df.copy()
    result_df['Analysis_Type'] = 'Best_By_Metric'
    
    # Phần 2: Overall scores
    scores_copy = scores_df.copy()
    scores_copy['Analysis_Type'] = 'Overall_Ranking'
    
    # Thêm các cột trống cho scores để khớp với best_teams
    for col in ['Metric', 'Mean', 'Median', 'Std_Dev', 'Count']:
        if col not in scores_copy.columns:
            scores_copy[col] = ''
    
    # Đổi tên cột Team thành Best_Team để khớp
    scores_copy = scores_copy.rename(columns={'Team': 'Best_Team'})
    
    # Sắp xếp lại cột
    common_cols = ['Analysis_Type', 'Best_Team', 'Metric', 'Mean', 'Median', 'Std_Dev', 'Count']
    score_cols = ['Total_Score', 'Score_Percentage', 'Attacking_Score', 'Defensive_Score', 'Possession_Score', 'GK_Score']
    
    for col in score_cols:
        if col not in result_df.columns:
            result_df[col] = ''
    
    # Gộp lại
    result_df = result_df[common_cols + score_cols]
    scores_copy = scores_copy[common_cols + score_cols]
    
    combined_df = pd.concat([result_df, scores_copy], ignore_index=True)
    
    # Thêm dòng phân cách
    separator_row = pd.DataFrame([{
        'Analysis_Type': '=' * 50,
        'Best_Team': '=' * 30,
        'Metric': '=' * 30,
        'Mean': '',
        'Median': '',
        'Std_Dev': '',
        'Count': '',
        'Total_Score': '',
        'Score_Percentage': '',
        'Attacking_Score': '',
        'Defensive_Score': '',
        'Possession_Score': '',
        'GK_Score': ''
    }])
    
    combined_df = pd.concat([combined_df, separator_row], ignore_index=True)
    
    # Thêm dòng kết luận
    conclusion_row = pd.DataFrame([{
        'Analysis_Type': '🏆 BEST TEAM',
        'Best_Team': best_team_analysis['team'],
        'Metric': f"Leading {best_team_analysis['leadership_count']} metrics",
        'Mean': '',
        'Median': '',
        'Std_Dev': '',
        'Count': '',
        'Total_Score': f"{best_team_analysis['total_score']:.2f}",
        'Score_Percentage': f"{best_team_analysis['score_percentage']:.2f}%",
        'Attacking_Score': f"{best_team_analysis['attacking_score']:.2f}",
        'Defensive_Score': f"{best_team_analysis['defensive_score']:.2f}",
        'Possession_Score': f"{best_team_analysis['possession_score']:.2f}",
        'GK_Score': f"{best_team_analysis['gk_score']:.2f}"
    }])
    
    combined_df = pd.concat([combined_df, conclusion_row], ignore_index=True)
    
    # Lưu file
    combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Đã lưu thành công!")
    print(f"   Kích thước file: {output_file.stat().st_size / 1024:.2f} KB")

def display_summary(scores_df, best_team_analysis, best_teams_df):
    """
    Hiển thị tóm tắt kết quả
    
    Args:
        scores_df: DataFrame điểm số
        best_team_analysis: Phân tích đội tốt nhất
        best_teams_df: DataFrame đội tốt nhất theo metric
    """
    print("\n" + "="*80)
    print("🏆 KẾT QUẢ PHÂN TÍCH - PREMIER LEAGUE 2024-2025")
    print("="*80)
    
    # Đội tốt nhất tổng thể
    print(f"\n🥇 ĐỘI CÓ PHONG ĐỘ TỐT NHẤT: {best_team_analysis['team']}")
    print(f"   Điểm tổng thể: {best_team_analysis['score_percentage']:.2f}%")
    print(f"   Dẫn đầu {best_team_analysis['leadership_count']} chỉ số")
    
    print(f"\n📊 Chi tiết điểm:")
    print(f"   ⚽ Tấn công:     {best_team_analysis['attacking_score']:.2f}")
    print(f"   🛡️  Phòng thủ:    {best_team_analysis['defensive_score']:.2f}")
    print(f"   🏃 Kiểm soát:    {best_team_analysis['possession_score']:.2f}")
    print(f"   🧤 Thủ môn:      {best_team_analysis['gk_score']:.2f}")
    
    # Top 5 đội
    print(f"\n📋 TOP 5 ĐỘI:")
    print("-" * 80)
    print(f"{'Hạng':<6} {'Đội':<25} {'Điểm%':<10} {'Tấn công':<12} {'Phòng thủ':<12} {'Kiểm soát':<12}")
    print("-" * 80)
    for idx, row in scores_df.head(5).iterrows():
        print(f"{idx+1:<6} {row['Team']:<25} {row['Score_Percentage']:>6.2f}%   "
              f"{row['Attacking_Score']:>8.2f}    {row['Defensive_Score']:>8.2f}    "
              f"{row['Possession_Score']:>8.2f}")
    
    # Thống kê dẫn đầu
    print(f"\n🎯 SỐ LẦN DẪN ĐẦU CHỈ SỐ:")
    print("-" * 80)
    leadership_counts = best_teams_df['Best_Team'].value_counts().head(10)
    for i, (team, count) in enumerate(leadership_counts.items(), 1):
        print(f"{i:2d}. {team:<25} {count:>3} chỉ số")
    
    # Một số chỉ số nổi bật
    print(f"\n⭐ MỘT SỐ CHỈ SỐ NỔI BẬT:")
    print("-" * 80)
    important_metrics = ['Goals', 'Assists', 'Pass_Completion_Pct', 'Tackles_Won', 'Save_Pct']
    for metric in important_metrics:
        metric_row = best_teams_df[best_teams_df['Metric'] == metric]
        if len(metric_row) > 0:
            row = metric_row.iloc[0]
            print(f"   {metric:<30} → {row['Best_Team']:<20} ({row['Mean']:.2f})")

def main():
    """Hàm chính"""
    print("="*80)
    print("⚽ PHÂN TÍCH ĐỘI BÓNG TỐT NHẤT - PREMIER LEAGUE 2024-2025")
    print("="*80)
    
    try:
        # Bước 1: Đọc dữ liệu
        df = load_statistics(INPUT_FILE)
        
        # Bước 2: Tìm đội tốt nhất cho từng chỉ số
        best_teams_df = find_best_teams_by_metric(df)
        
        # Bước 3: Tính điểm tổng thể
        scores_df = calculate_overall_score(df, best_teams_df)
        
        # Bước 4: Phân tích đội tốt nhất
        best_team_analysis = analyze_best_team(scores_df, best_teams_df)
        
        # Bước 5: Lưu kết quả
        save_results_with_conclusion(best_teams_df, scores_df, best_team_analysis, OUTPUT_FILE)
        
        # Bước 6: Hiển thị tổng hợp
        display_summary(scores_df, best_team_analysis, best_teams_df)
        
        print("\n" + "="*80)
        print("✅ HOÀN THÀNH!")
        print("="*80)
        print(f"\n📁 File kết quả: {OUTPUT_FILE}")
        print(f"\n💡 Kết luận:")
        print(f"   Đội {best_team_analysis['team']} đang có phong độ tốt nhất")
        print(f"   Premier League mùa giải 2024-2025 với điểm tổng thể {best_team_analysis['score_percentage']:.2f}%")
        
    except FileNotFoundError as e:
        print(f"\n❌ Lỗi: Không tìm thấy file")
        print(f"   {e}")
        print(f"\n💡 Vui lòng chạy team_statistics.py trước")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
