import pandas as pd
import numpy as np
transfers_data = pd.read_csv('../../Output/Output_I/player_transfers.csv')
players_data = pd.read_csv('../../Output/Output_I/players_stats.csv')
players_data['transfer_value'] = transfers_data['transfer_value']
def convert_transfer_value(value):
    if value == 'N/a':
        return np.nan
    value = value.replace('€', '')
    if 'M' in value:
        return float(value.replace('M', '')) * 1_000_000
    elif 'K' in value:
        return float(value.replace('K', '')) * 1_000
    else:
        return float(value)
players_data['transfer_value'] = players_data['transfer_value'].apply(convert_transfer_value)
median_transfer_value = players_data['transfer_value'].median()
players_data['transfer_value'] = players_data['transfer_value'].fillna(median_transfer_value)
features = players_data.columns.tolist()
null_features = []
for feature in features:
    if players_data[feature].dtype == object:
        if players_data[feature].str.contains("N/a").any():
            null_features.append(feature)
    else:
        if players_data[feature].isnull().any():
            null_features.append(feature)
print(f"Number of features: {len(features)}")
print(f"Features with 'N/a' values: {len(null_features)}")
print(f"null_features: {null_features}")
for feature in null_features:
    null_count = players_data[feature].str.contains("N/a").sum()
    total_count = len(players_data)
    null_percentage = (null_count / total_count) * 100
    feature_type = players_data[feature].dtype
    print(f"Feature: {feature}, Null Percentage: {null_percentage:.2f}%, Type: {feature_type}")
for feature in null_features:
    if players_data[feature].dtype == object:
        null_count = players_data[feature].str.contains("N/a").sum()
    total_count = len(players_data)
    null_percentage = (null_count / total_count) * 100
    if null_percentage > 90:
        players_data = players_data.drop(columns=[feature])
    else:
        mode_value = players_data[players_data[feature] != "N/a"][feature].mode()[0]
        players_data[feature] = players_data[feature].replace("N/a", mode_value)
print(f"shape {players_data.shape}")


## Chuyển đổi sang kiểu dữ liệu số
for feature in players_data.columns:
    try:
        players_data[feature] = pd.to_numeric(players_data[feature])
        print(f"Converted feature: {feature} to numeric")
    except ValueError:
        pass
numeric_features = players_data.select_dtypes(include=[np.number]).columns.tolist()
categorical_features = players_data.select_dtypes(exclude=[np.number]).columns.tolist()
print(f"Numeric features: {numeric_features}")
print(f"Categorical features: {categorical_features}")
for feature in categorical_features:
    unique_values = players_data[feature].unique()
    print(f"Feature: {feature}, Unique values: {unique_values}")
players_data = players_data.drop(columns=['Name', 'Team', 'Nation'])
goal_scoring_map = {
    # 0 - Thủ môn
    'GK': 0,
    
    # 1 - Hậu vệ
    'DF': 1,
    'DFFW': 1,
    
    # 2 - Tiền vệ phòng ngự
    'DFMF': 2,
    'MFDF': 2,
    
    # 3 - Tiền vệ trung tâm
    'MF': 3,
    
    # 4 - Tiền vệ công 
    'MFFW': 4,
    'FWMF': 4,
    'FWDF': 4, 
    
    # 5 - Tiền đạo cắm
    'FW': 5
}
players_data['Position'] = players_data['Position'].map(goal_scoring_map)

## Phân tích dữ liệu số 
numeric_summary = players_data[players_data.columns].describe().T
print("Numeric Features Summary:")
print(numeric_summary)

## Chuẩn hóa dữ liệu
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
players_data_scaled = scaler.fit_transform(players_data[players_data.columns])
players_data_scaled = pd.DataFrame(players_data_scaled, columns=players_data.columns)

## Mô tả dữ liệu sau tiền xử lý
numeric_summary_scaled = players_data_scaled.describe().T
print("Numeric Features Summary after Scaling:")
print(numeric_summary_scaled)
# Save processed data
players_data.to_csv('../../Output/Output_IV/players_data_processed.csv', index=False)
players_data_scaled.to_csv('../../Output/Output_IV/players_data_scaled.csv', index=False)