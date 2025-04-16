from rotation_planner import generate_crop_rotation_plan

print("AI Crop Rotation Planner (Terminal Edition)")
start_crop = input("Enter starting crop (case-sensitive): ")
month_input = input("Enter starting month (1–12, default=1): ")
start_month = int(month_input) if month_input.strip() else 1

plan = generate_crop_rotation_plan("indian_crop_dataset.json", start_crop, start_month)

print("\nGenerated Crop Rotation Plan:\n")
for entry in plan:
    print(f"{entry['Crop']} → {entry['Start Month']} to {entry['End Month']}")
