import csv
import json
import os
from datetime import datetime

# ASSUMPTION: You changed spec to allow requests (Option D)
import requests

CSV_FILE = "clean.csv"
JSON_FILE = "summary.json"

HEADERS = ["name", "age", "city", "timestamp"]


def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def get_valid_name():
    while True:
        name = input("Enter name: ").strip()
        if name:
            return name
        print("Name cannot be empty. Try again.")


def get_valid_age():
    while True:
        raw = input("How old are you? ")
        try:
            age = int(raw)
        except ValueError:
            print("Age must be a whole number.")
            continue
        
        if 1 <= age <= 120:
            return age
        else:
            print("Age must be in the range of 1 and 120")


def is_valid_city(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "YourFinanceApp/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        return len(data) > 0
    except requests.exceptions.RequestException:
        # If internet is down or API fails, we can't validate
        # Fallback: accept anything (you might want to change this policy)
        print("Warning: Could not reach city validation API. Accepting input.")
        return True


def get_valid_city():
    while True:
        city = input("Enter city: ").strip()
        if not city:
            print("City cannot be empty. Try again.")
            continue
        
        if is_valid_city(city):
            return city.title()
        else:
            print(f"'{city}' not found as a real city. Try again.")


def add_user():
    print("\n=== Add New User ===")
    name = get_valid_name()
    age = get_valid_age()
    city = get_valid_city()
    
    timestamp = datetime.now().isoformat()
    
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, age, city, timestamp])
    
    print(f"Saved: {name}, {age}, {city}\n")


def generate_summary():
    summary = {
        "total_users": 0,
        "average_age": 0.0,
        "cities": {},
        "last_updated": datetime.now().isoformat()
    }
    
    ages = []
    cities = {}
    
    if not os.path.exists(CSV_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print("No data yet. Summary created.")
        return
    
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                age = int(row["age"])
                city = row["city"]
            except (ValueError, KeyError):
                # Skip corrupted rows silently (per your spec)
                continue
            
            ages.append(age)
            cities[city] = cities.get(city, 0) + 1
    
    if ages:
        summary["total_users"] = len(ages)
        summary["average_age"] = sum(ages) / len(ages)
        summary["cities"] = cities
    
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary: {JSON_FILE}")
    print(f"Total users: {summary['total_users']}")
    print(f"Average age: {summary['average_age']:.1f}")
    print(f"Cities: {summary['cities']}\n")


def view_all_users():
    print("\n=== All Users ===")
    if not os.path.exists(CSV_FILE):
        print("No users saved yet.\n")
        return
    
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            print(f"{row.get('name', 'N/A')} | Age: {row.get('age', 'N/A')} | City: {row.get('city', 'N/A')}")
            count += 1
    
    print(f"Total: {count} users\n")


def main():
    initialize_csv()
    
    while True:
        print("=== User Data Entry ===")
        print("1. Add User")
        print("2. View All Users")
        print("3. Generate Summary")
        print("4. Quit")
        
        choice = input("Choose (1-4): ").strip()
        
        if choice == "1":
            add_user()
        elif choice == "2":
            view_all_users()
        elif choice == "3":
            generate_summary()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()