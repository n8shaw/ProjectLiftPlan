import pandas as pd
from tabulate import tabulate

class plan:
    def __init__(self, time, timesPerWeek, gym):
        self.time = 60 #time in minutes
        self.timesPerWeek = 6 #times per week
        self.gym = True #if you have access to gym or gym equipment





def generate_split(days_per_week):
    split = []
    
    if days_per_week == 6:
        split = ["Push", "Pull", "Legs", "Push", "Pull", "Legs"]
    elif days_per_week == 5:
        split = ["Push", "Pull", "Legs", "Upper", "Lower"]
    elif days_per_week == 4:
        split = ["Upper", "Lower", "Upper", "Lower"]
    elif days_per_week == 3:
        split = ["Push", "Pull", "Legs"]
    else:
        split = ["Full Body (FB)"]
    
    return split

def lift_gen(split, Plan, df):
    numLifts = Plan.time // 10
    WorkoutPlan = pd.DataFrame(columns=['Day', 'Title', 'Description', 'Equipment'])

    for day_index, day in enumerate(split):
        if day == 'Push':
            priority = ['Chest', 'Triceps', 'Shoulders']
        elif day == 'Pull':
            priority = ['Lats', 'Middle Back', 'Biceps', 'Forearms', 'Traps']
        elif day == 'Legs' or day == 'Lower':
            priority = ['Quadriceps', 'Hamstrings', 'Calves', 'Abdominals', 'Adductors', 'Abductors']
        elif day == 'Upper':
            priority = ['Chest', 'Lats', 'Triceps', 'Biceps', 'Shoulders', 'Middle Back', 'Forearms']
        else:
            priority = ['Chest', 'Quadriceps', 'Lats', 'Hamstrings', 'Shoulders', 'Triceps', 'Biceps', 'Calves', 'Abdominals']

        for i in range(numLifts):
            if Plan.gym:
                # Ensure priority index wraps around within the range of the list
                muscle_group_index = i % len(priority)
                filtered_df = df[(df['BodyPart'] == priority[muscle_group_index]) & (df['Gym'] == True)]

                if not filtered_df.empty:
                    lift = filtered_df.sample(1).iloc[0]  # Select 1 random row
                    new_entry = {
                        'Day': day_index + 1,  # day_index starts from 0, so +1 to match days
                        'Title': lift['Title'],
                        'Description': lift['Desc'],
                        'Equipment': lift['Equipment']
                    }
                    WorkoutPlan = pd.concat([WorkoutPlan, pd.DataFrame([new_entry])], ignore_index=True)
            else:

                # Ensure priority index wraps around within the range of the list
                muscle_group_index = i % len(priority)
                filtered_df = df[(df['BodyPart'] == priority[muscle_group_index]) & (df['Gym'] == True)]

                if not filtered_df.empty:
                    lift = filtered_df.sample(1).iloc[0]  # Select 1 random row
                    new_entry = {
                        'Day': day_index + 1,  # day_index starts from 0, so +1 to match days
                        'Title': lift['Title'],
                        'Description': lift['Desc'],
                        'Equipment': lift['Equipment']
                    }
                    WorkoutPlan = pd.concat([WorkoutPlan, pd.DataFrame([new_entry])], ignore_index=True)

    return WorkoutPlan




def main():
    df = pd.read_pickle('processed_data.pkl')
    Weekly = input("How Many Times per Week? (1-6) ")
    duration = input("How much time per session? (In Minutes)")
    gyms = input("Do you have access to a gym or gym equipment? (True/False)")
    if gyms.lower() == "true":
        bool_value = True
    elif gyms.lower() == "false":
        bool_value = False
    user_plan = plan(int(duration), int(Weekly), bool_value)

    split = generate_split(user_plan.timesPerWeek)

    lift_plan = lift_gen(split, user_plan, df)

    print(lift_plan)

    



if __name__ == "__main__":
    main()