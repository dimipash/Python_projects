import bcrypt
from database import init_db, get_db
from models import User, Workout, NutritionLog
from datetime import datetime, timedelta
from collections import defaultdict
from getpass import getpass

class FitnessTracker:
    def __init__(self):
        self.current_user = None
        init_db()
        self.db = next(get_db())

    def register_user(self, username, password, name, age, weight, height):
        # Check if user exists
        if self.db.query(User).filter(User.username == username).first():
            print("Username already exists!")
            return False
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create new user
        new_user = User(
            username=username,
            password_hash=password_hash.decode('utf-8'),
            name=name,
            age=age,
            weight=weight,
            height=height
        )
        
        self.db.add(new_user)
        self.db.commit()
        print("User registered successfully!")
        return True

    def login(self, username, password):
        user = self.db.query(User).filter(User.username == username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            self.current_user = user
            print(f"Welcome back, {user.name}!")
            return True
        print("Invalid username or password!")
        return False

    def log_workout(self, workout_type, duration, intensity, calories_burned):
        if not self.current_user:
            print("Please login first!")
            return
        
        workout = Workout(
            user_id=self.current_user.id,
            type=workout_type,
            duration=duration,
            intensity=intensity,
            calories_burned=calories_burned,
            date=datetime.now()
        )
        
        self.db.add(workout)
        self.db.commit()
        print("Workout logged successfully!")

    def log_nutrition(self, food_name, calories, protein, carbs, fats):
        if not self.current_user:
            print("Please login first!")
            return
        
        nutrition = NutritionLog(
            user_id=self.current_user.id,
            food_name=food_name,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats,
            date=datetime.now()
        )
        
        self.db.add(nutrition)
        self.db.commit()
        print("Nutrition logged successfully!")

    def view_progress(self):
        if not self.current_user:
            print("Please login first!")
            return
        
        # Get workout data for the last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)
        workouts = self.db.query(Workout).filter(
            Workout.user_id == self.current_user.id,
            Workout.date >= seven_days_ago
        ).all()
        
        # Organize workouts by date
        workout_by_date = defaultdict(list)
        for workout in workouts:
            date_str = workout.date.strftime('%Y-%m-%d')
            workout_by_date[date_str].append(workout)
        
        print("\n=== Your Progress (Last 7 Days) ===")
        total_calories = 0
        total_duration = 0
        
        for date in sorted(workout_by_date.keys()):
            day_workouts = workout_by_date[date]
            day_calories = sum(w.calories_burned for w in day_workouts)
            day_duration = sum(w.duration for w in day_workouts)
            
            print(f"\n{date}:")
            print(f"  Total Workouts: {len(day_workouts)}")
            print(f"  Total Duration: {day_duration} minutes")
            print(f"  Calories Burned: {day_calories}")
            
            total_calories += day_calories
            total_duration += day_duration
        
        if workouts:
            print("\nSummary:")
            print(f"Total Workouts: {len(workouts)}")
            print(f"Total Duration: {total_duration} minutes")
            print(f"Total Calories Burned: {total_calories}")
            print(f"Average Daily Calories: {total_calories / 7:.1f}")
        else:
            print("\nNo workouts recorded in the last 7 days.")

def main():
    tracker = FitnessTracker()
    
    while True:
        if not tracker.current_user:
            print("\n=== Fitness Tracker ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                username = input("Username: ")
                password = getpass("Password: ")
                name = input("Name: ")
                age = int(input("Age: "))
                weight = float(input("Weight (kg): "))
                height = float(input("Height (cm): "))
                tracker.register_user(username, password, name, age, weight, height)
            
            elif choice == "2":
                username = input("Username: ")
                password = getpass("Password: ")
                tracker.login(username, password)
            
            elif choice == "3":
                print("Thank you for using Fitness Tracker!")
                break
            
            else:
                print("Invalid choice! Please try again.")
        else:
            print(f"\n=== {tracker.current_user.name}'s Dashboard ===")
            print("1. Log Workout")
            print("2. Log Nutrition")
            print("3. View Progress")
            print("4. View Profile")
            print("5. Logout")
            print("6. Exit")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == "1":
                workout_type = input("Workout type: ")
                duration = int(input("Duration (minutes): "))
                intensity = input("Intensity (low/medium/high): ")
                calories = int(input("Calories burned: "))
                tracker.log_workout(workout_type, duration, intensity, calories)
            
            elif choice == "2":
                food_name = input("Food name: ")
                calories = int(input("Calories: "))
                protein = float(input("Protein (g): "))
                carbs = float(input("Carbs (g): "))
                fats = float(input("Fats (g): "))
                tracker.log_nutrition(food_name, calories, protein, carbs, fats)
            
            elif choice == "3":
                tracker.view_progress()
            
            elif choice == "4":
                print(f"\n=== Profile Information ===")
                print(f"Name: {tracker.current_user.name}")
                print(f"Age: {tracker.current_user.age}")
                print(f"Weight: {tracker.current_user.weight} kg")
                print(f"Height: {tracker.current_user.height} cm")
                input("\nPress Enter to continue...")
            
            elif choice == "5":
                print(f"Goodbye, {tracker.current_user.name}!")
                tracker.current_user = None
            
            elif choice == "6":
                print("Thank you for using Fitness Tracker!")
                break
            
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
