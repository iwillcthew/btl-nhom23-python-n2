# config.py - Cấu hình cho việc thu thập dữ liệu cầu thủ

# Cấu hình chung
BASE_URL = "https://fbref.com/en/comps/9/2024-2025/"
SEASON_SUFFIX = "2024-2025-Premier-League-Stats"
MIN_MINUTES = 90
WAIT_TIMEOUT = 10

# Cấu hình SQLite
DATABASE_FILE = "../../Output/Output_I/football_stats.db"
TABLE_PLAYERS = "players"
TABLE_TRANSFERS = "player_transfers"

# Danh sách các bảng thống kê cần thu thập từ fbref.com
TABLES = [
    {
        "url": "stats/",
        "table_id": "stats_standard",
        "fields": [
            ("Name", "player"),
            ("Nation", "nationality"),
            ("Team", "team"),
            ("Position", "position"),
            ("Age", "age"),
            ("Matches_Played", "games"),
            ("Starts", "games_starts"),
            ("Minutes", "minutes"),
            ("Goals", "goals"),
            ("Assists", "assists"),
            ("Yellow_Cards", "cards_yellow"),
            ("Red_Cards", "cards_red"),
            ("xG", "xg"),
            ("xAG", "xg_assist"),
            ("Progressive_Carries", "progressive_carries"),
            ("Progressive_Passes", "progressive_passes"),
            ("Progressive_Passes_Received", "progressive_passes_received"),
            ("Goals_Per90", "goals_per90"),
            ("Assists_Per90", "assists_per90"),
            ("xG_Per90", "xg_per90"),
            ("xAG_Per90", "xg_assist_per90"),
        ]
    },
    {
        "url": "keepers/",
        "table_id": "stats_keeper",
        "fields": [
            ("GA90", "gk_goals_against_per90"),
            ("Save_Pct", "gk_save_pct"),
            ("CS_Pct", "gk_clean_sheets_pct"),
            ("PK_Save_Pct", "gk_pens_save_pct"),
        ]
    },
    {
        "url": "shooting/",
        "table_id": "stats_shooting",
        "fields": [
            ("SoT_Pct", "shots_on_target_pct"),
            ("SoT_Per90", "shots_on_target_per90"),
            ("Goals_Per_Shot", "goals_per_shot"),
            ("Avg_Shot_Distance", "average_shot_distance"),
        ]
    },
    {
        "url": "passing/",
        "table_id": "stats_passing",
        "fields": [
            ("Passes_Completed", "passes_completed"),
            ("Pass_Completion_Pct", "passes_pct"),
            ("Progressive_Passing_Distance", "passes_progressive_distance"),
            ("Short_Pass_Pct", "passes_pct_short"),
            ("Medium_Pass_Pct", "passes_pct_medium"),
            ("Long_Pass_Pct", "passes_pct_long"),
            ("Key_Passes", "assisted_shots"),
            ("Passes_Into_Final_Third", "passes_into_final_third"),
            ("Passes_Into_Penalty_Area", "passes_into_penalty_area"),
            ("Crosses_Into_Penalty_Area", "crosses_into_penalty_area"),
        ]
    },
    {
        "url": "gca/",
        "table_id": "stats_gca",
        "fields": [
            ("SCA", "sca"),
            ("SCA90", "sca_per90"),
            ("GCA", "gca"),
            ("GCA90", "gca_per90"),
        ]
    },
    {
        "url": "defense/",
        "table_id": "stats_defense",
        "fields": [
            ("Tackles", "tackles"),
            ("Tackles_Won", "tackles_won"),
            ("Challenges", "challenges"),
            ("Challenges_Lost", "challenges_lost"),
            ("Blocks", "blocks"),
            ("Blocked_Shots", "blocked_shots"),
            ("Blocked_Passes", "blocked_passes"),
            ("Interceptions", "interceptions"),
        ]
    },
    {
        "url": "possession/",
        "table_id": "stats_possession",
        "fields": [
            ("Touches", "touches"),
            ("Touches_Def_Pen", "touches_def_pen_area"),
            ("Touches_Def_3rd", "touches_def_3rd"),
            ("Touches_Mid_3rd", "touches_mid_3rd"),
            ("Touches_Att_3rd", "touches_att_3rd"),
            ("Touches_Att_Pen", "touches_att_pen_area"),
            ("Take_Ons_Attempted", "take_ons"),
            ("Take_Ons_Success_Pct", "take_ons_won_pct"),
            ("Take_Ons_Tackled_Pct", "take_ons_tackled_pct"),
            ("Carries", "carries"),
            ("Progressive_Carries_Distance", "carries_progressive_distance"),
            ("Carries_Into_Final_Third", "carries_into_final_third"),
            ("Carries_Into_Penalty_Area", "carries_into_penalty_area"),
            ("Miscontrols", "miscontrols"),
            ("Dispossessed", "dispossessed"),
            ("Passes_Received", "passes_received"),
        ]
    },
    {
        "url": "misc/",
        "table_id": "stats_misc",
        "fields": [
            ("Fouls_Committed", "fouls"),
            ("Fouls_Drawn", "fouled"),
            ("Offsides", "offsides"),
            ("Crosses", "crosses"),
            ("Ball_Recoveries", "ball_recoveries"),
            ("Aerials_Won", "aerials_won"),
            ("Aerials_Lost", "aerials_lost"),
            ("Aerials_Won_Pct", "aerials_won_pct"),
        ]
    }
]

# Tạo danh sách tất cả các cột cho bảng SQL
ALL_COLUMNS = []
for table in TABLES:
    for field in table["fields"]:
        col_name = field[0]
        if col_name not in ALL_COLUMNS:
            ALL_COLUMNS.append(col_name)
