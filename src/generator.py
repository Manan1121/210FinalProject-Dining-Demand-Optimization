import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_data(start_date="2025-11-01", days=21):
    """
    Generates simulated datasets for Menu, Traffic, Weather, and Events.
    Follows logic from Interim Report[cite: 508, 515, 523].
    """
    dates = [datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i) for i in range(days)]
    halls = ["Livingston", "Busch"] # [cite: 505]
    meals = ["Breakfast", "Lunch", "Dinner"]
    
    # 1. Menu Data Generation [cite: 506-509]
    menu_data = []
    items_pool = {
        "Entree": ["Grilled Chicken", "Pasta Primavera", "Tacos", "Burger", "Tofu Stir Fry"],
        "Side": ["Fries", "Salad", "Steamed Veggies", "Rice", "Soup"],
        "Dessert": ["Cookie", "Ice Cream", "Brownie"]
    }
    
    for date in dates:
        for hall in halls:
            for meal in meals:
                # Generate ~10 items per meal [cite: 508]
                for _ in range(10):
                    cat = random.choice(list(items_pool.keys()))
                    item = random.choice(items_pool[cat])
                    # Random tags assignment
                    tags = []
                    if random.random() > 0.7: tags.append("Vegetarian")
                    if random.random() > 0.8: tags.append("Vegan")
                    if random.random() > 0.9: tags.append("GF")
                    
                    menu_data.append({
                        "hall_name": hall,
                        "date": date.strftime("%Y-%m-%d"),
                        "meal_period": meal,
                        "item_name": item,
                        "category": cat,
                        "tags": ",".join(tags) if tags else "None"
                    })

    # 2. Traffic Data Simulation [cite: 512-519]
    traffic_data = []
    base_traffic = {"Breakfast": 150, "Lunch": 400, "Dinner": 300} # 
    
    for date in dates:
        is_weekend = date.weekday() >= 5
        # Weekday multiplier 1.0, Weekend 0.7 [cite: 516]
        day_multiplier = 0.7 if is_weekend else 1.0
        
        for hall in halls:
            for meal in meals:
                base = base_traffic[meal]
                # Add +/- 10% variation [cite: 518]
                variation = random.uniform(0.9, 1.1)
                count = int(base * day_multiplier * variation)
                
                traffic_data.append({
                    "hall_name": hall,
                    "date": date.strftime("%Y-%m-%d"),
                    "meal_period": meal,
                    "traffic_count": count
                })

    # 3. Weather Data Simulation [cite: 521-525]
    # Simulating API response format
    weather_data = []
    for date in dates:
        for meal in meals:
            # Simulating late autumn temp (40-60F)
            temp = random.uniform(40, 60)
            precip = 0.0 if random.random() > 0.3 else random.uniform(0.1, 5.0)
            
            weather_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "meal_period": meal,
                "avg_temp": round(temp, 1),
                "precipitation_mm": round(precip, 2)
            })

    # 4. Events Data 
    events_data = []
    # Create random events on some days
    for date in dates:
        if random.random() > 0.7: # 30% chance of event
            events_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "event_type": random.choice(["Football Game", "Career Fair", "Concert"]),
                "expected_attendance": random.randint(500, 5000),
                "nearby_hall": random.choice(halls)
            })

    return (pd.DataFrame(menu_data), pd.DataFrame(traffic_data), 
            pd.DataFrame(weather_data), pd.DataFrame(events_data))

if __name__ == "__main__":
    m, t, w, e = generate_data()
    print(f"Generated {len(m)} menu items, {len(t)} traffic records.")
