import pickle
import json
import os
from collections import defaultdict

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, 'crop_data.json')
QTABLE_PATH = os.path.join(BASE_DIR, 'output', 'trained_q_table.pkl')

# Load crop data
with open(DATA_PATH, 'r') as f:
    crop_data = json.load(f)

# Dynamic crop name mappings
crop_names = list(crop_data.keys())
crop_to_index = {name: idx for idx, name in enumerate(crop_names)}
index_to_crop = {idx: name for name, idx in crop_to_index.items()}

# Define seasons manually
seasons = ["Spring", "Summer", "Fall", "Winter"]
season_to_index = {season: idx for idx, season in enumerate(seasons)}
index_to_season = {idx: season for season, idx in season_to_index.items()}

# Month to season mapping
month_to_season = {
    1: "Winter", 2: "Winter", 3: "Spring", 
    4: "Spring", 5: "Spring", 6: "Summer",
    7: "Summer", 8: "Summer", 9: "Fall",
    10: "Fall", 11: "Fall", 12: "Winter"
}

# Season to representative month mapping
season_to_month = {
    "Spring": 4,
    "Summer": 7,
    "Fall": 10,
    "Winter": 1
}

# Load trained Q-table
try:
    with open(QTABLE_PATH, 'rb') as f:
        q_table = pickle.load(f)
    print(f"Loaded Q-table from {QTABLE_PATH} with {len(q_table)} entries")
except FileNotFoundError:
    print(f"Q-table not found at {QTABLE_PATH}")
    q_table = {}

def find_closest_month(target_month, available_months):
    """Find the closest month to the target from the available months"""
    if not available_months:
        return None
    
    distances = []
    for month in available_months:
        direct_dist = abs(month - target_month)
        wrap_dist = 12 - direct_dist
        min_dist = min(direct_dist, wrap_dist)
        distances.append((min_dist, month))
    
    return min(distances, key=lambda x: x[0])[1]

def extract_available_months(q_table):
    """Extract all months that have data in the Q-table"""
    available_months = set()
    
    for (state, _), _ in q_table.items():
        if isinstance(state, tuple) and len(state) >= 1:
            if 1 <= state[0] <= 12:  # Ensure it's a valid month
                available_months.add(state[0])
    
    return sorted(available_months)

def get_recommendations(last_crop_name, season_name=None, month=None, max_recommendations=3, min_q_value=0):
    """Get crop recommendations based on previous crop and either season or month."""
    print(f"DEBUG: Starting get_recommendations with last_crop_name={last_crop_name}, season_name={season_name}, month={month}")
    
    last_crop_name = last_crop_name.strip().title()
    
    if last_crop_name not in crop_to_index:
        close_matches = [name for name in crop_names if last_crop_name.lower() in name.lower()]
        if close_matches:
            return None, f"Invalid crop name: '{last_crop_name}'. Did you mean one of these? {', '.join(close_matches)}"
        return None, f"Invalid crop name: '{last_crop_name}'. Available crops: {', '.join(crop_names)}"
    
    if month is None and season_name is not None:
        season_name = season_name.strip().title()
        if season_name not in season_to_month:
            return None, f"Invalid season: '{season_name}'. Available seasons: {', '.join(seasons)}"
        month = season_to_month[season_name]
    
    if season_name is None and month is not None:
        try:
            month = int(month)
            if month < 1 or month > 12:
                return None, f"Invalid month: {month}. Please enter a month between 1 and 12."
            season_name = month_to_season[month]
        except (ValueError, TypeError):
            return None, f"Invalid month: {month}. Please enter a month between 1 and 12."
    elif season_name is None and month is None:
        return None, "Please provide either a season or month."
    
    crop_index = crop_to_index[last_crop_name]
    
    original_state = (month, crop_index)
    
    print(f"DEBUG: Original state (month, crop): {original_state}")
    
    recommendations = []
    
    available_months = extract_available_months(q_table)
    print(f"DEBUG: Available months in Q-table: {available_months}")
    
    state_actions = {}
    for (s, a), q_value in q_table.items():
        if s == original_state:
            state_actions[a] = q_value
            print(f"DEBUG: Found action {a} with Q-value {q_value}")
    
    if not state_actions and available_months:
        closest_month = find_closest_month(month, available_months)
        if closest_month:
            print(f"DEBUG: Using closest month {closest_month}")
            alternative_state = (closest_month, crop_index)
            
            for (s, a), q_value in q_table.items():
                if s == alternative_state:
                    state_actions[a] = q_value
                    print(f"DEBUG: Found action {a} with Q-value {q_value} using closest month {closest_month}")
    
    if not state_actions:
        alt_state = (crop_index, season_to_index[season_name])
        print(f"DEBUG: Trying with (crop, season): {alt_state}")
        
        for (s, a), q_value in q_table.items():
            if s == alt_state:
                state_actions[a] = q_value
                print(f"DEBUG: Found action {a} with Q-value {q_value}")
    
    if not state_actions:
        crop_actions = defaultdict(list)
        
        for (s, a), q_value in q_table.items():
            if isinstance(s, tuple) and len(s) >= 2 and s[1] == crop_index:
                crop_actions[a].append(q_value)
        
        for action, values in crop_actions.items():
            state_actions[action] = sum(values) / len(values)
            print(f"DEBUG: Using averaged Q-value {state_actions[action]} for action {action}")
    
    if not state_actions:
        return None, f"No recommendations found for crop '{last_crop_name}' in {season_name} season (month {month})."
    
    sorted_actions = sorted(state_actions.items(), key=lambda x: x[1], reverse=True)
    print(f"DEBUG: Found {len(sorted_actions)} possible recommendations")
    
    for action, q_value in sorted_actions:
        if q_value < min_q_value:
            continue
        
        if action not in index_to_crop:
            continue
            
        crop_name = index_to_crop[action]
        crop_info = crop_data.get(crop_name, {})
        
        recommendation = {
            "crop": crop_name,
            "confidence": q_value,
            "image_url": crop_info.get("image_url", "No image available"),
            "family": crop_info.get("family", "Unknown"),
            "planting_months": crop_info.get("planting_months", []),
            "grow_duration": crop_info.get("grow_duration", "Unknown"),
            "successor_crops": crop_info.get("successor_crops", [])
        }
        
        recommendations.append(recommendation)
        
        if len(recommendations) >= max_recommendations:
            break
    
    if not recommendations:
        return None, f"No suitable recommendations found for crop '{last_crop_name}' in {season_name} season."
    
    return recommendations, None

def format_planting_months(months):
    """Format month numbers as month names"""
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    return ", ".join(month_names[m-1] for m in months) if months else "Unknown"

def main():
    print("Smart Crop Rotation Assistant")
    
    if not q_table:
        print("ERROR: Q-table is empty. Please check your Q-table file.")
        return
    
    print("DEBUG: Analyzing Q-table structure:")
    state_counts = defaultdict(int)
    crop_counts = defaultdict(int)
    month_counts = defaultdict(int)
    
    for (state, action), _ in q_table.items():
        state_counts[state] += 1
        if isinstance(state, tuple) and len(state) >= 2:
            month = state[0]
            crop_idx = state[1]
            
            if 1 <= month <= 12:
                month_counts[month] += 1
            
            if crop_idx in index_to_crop:
                crop_name = index_to_crop[crop_idx]
                crop_counts[crop_name] += 1
    
    print(f"Found data for {len(crop_counts)} crops in Q-table")
    print(f"Crops with data: {', '.join(sorted(crop_counts.keys()))}")
    print(f"Top 5 crops by entry count: {sorted(crop_counts.items(), key=lambda x: x[1], reverse=True)[:5]}")
    print(f"Month distribution: {dict(sorted(month_counts.items()))}")
    
    last_crop = input("What was the last crop planted? ")
    season = input("Enter current season (leave blank for month): ")
    
    if not season:
        month = input("Enter current month (1-12): ")
        recommendations, error = get_recommendations(last_crop, month=month)
    else:
        recommendations, error = get_recommendations(last_crop, season_name=season)
    
    if error:
        print(f"\n{error}")
    else:
        print("\nRecommended crops:")
        print("---------------------")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['crop']} (Confidence: {rec['confidence']:.2f})")
            print(f"   Planting Months: {format_planting_months(rec['planting_months'])}")
            print(f"   Grow Duration: {rec['grow_duration']}")
            print(f"   Successor Crops: {', '.join(rec['successor_crops'])}")
            print(f"   Image URL: {rec['image_url']}")
            print()

if __name__ == '__main__':
    main()