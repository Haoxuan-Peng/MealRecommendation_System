import os
import json
import random
import time
from collections import defaultdict

class FoodRecommendationSystem:
    def __init__(self, menu_file='menu.txt', preference_file='user_preference.json'):
        self.menu_file = menu_file
        self.preference_file = preference_file
        self.cuisines = []  # All cuisines
        self.dishes_by_cuisine = defaultdict(list)  # Dishes by cuisine
        self.all_dishes = set()  # All dishes
        self.user_preference = {'dishes': {}, 'total_selections': 0} # Store user preference
        self.needs_update = True
        
        # Initialize the system
        self.initialize()
        
    def initialize(self):
        '''Initialize the system, and check if the menu needs to be updated'''
        print('\nInitializing the system...')
        time.sleep(1) # Simulate loading time
        
        # Check if the menu file exists, if not create a default one
        if not os.path.exists(self.menu_file):
            self.create_default_menu()
            
        # Load the menu file
        self.load_menu()
            
        # Load user's preference
        self.load_user_preference()
        
        print('System initialized successfully!')
        
        # Ask if user wants to reset preferences
        if os.path.exists(self.preference_file) and self.user_preference['total_selections'] > 0:
            reset_choice = input('\nWould you like to reset your preferences? (yes/no): ').strip().lower()
            if reset_choice == 'yes':
                self.reset_user_preference()
            
    def create_default_menu(self):
        '''Create a default menu file'''
        with open(self.menu_file, 'w') as file:
            file.write('True\n')
            file.write('Chinese Cuisine,Dumplings\n')
            file.write('Chinese Cuisine,Tomato and Egg Noodles\n')
            file.write('Western Cuisine,Steak\n')
            file.write('Western Cuisine,Spaghetti\n')
            file.write('Japanese Cuisine,Sushi\n')
    
    def load_menu(self):
        '''Load the menu from the file'''
        self.cuisines = []
        self.dishes_by_cuisine = defaultdict(list)
        self.all_dishes = set()
        
        with open(self.menu_file, 'r') as file:
            # Get every line in the file
            for line in file:
                line = line.strip()
                if line:
                    cuisine, dish = line.split(',')
                    if cuisine not in self.cuisines:
                        self.cuisines.append(cuisine)
                    self.dishes_by_cuisine[cuisine].append(dish)
                    self.all_dishes.add(dish)

    def load_user_preference(self):
        '''Load user preference from the file, if it not exists, create a new one'''
        if os.path.exists(self.preference_file) and os.path.getsize(self.preference_file) > 0:
            with open(self.preference_file, 'r') as file:
                self.user_preference = json.load(file) # Load existing user preference
        else:
            # Create a new user preference file with default values
            self.user_preference = {'dishes': {}, 'total_selections': 0}
            for dish in self.all_dishes:
                self.user_preference['dishes'][dish] = {
                    'selection_count': 0,
                    'recommendation_count': 0
                }
            self.save_user_preference()
    
    def save_user_preference(self):
        '''Save user preference to the file'''
        dirname = os.path.dirname(self.preference_file)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        
        with open(self.preference_file, 'w') as file:
            json.dump(self.user_preference, file, indent=2)
    
    def update_user_preference(self, selected_dish):
        '''Update user preference based on selected dish'''
        if selected_dish in self.all_dishes: # User can only select dishes from the menu
            # Check if the dish has not been selected before
            if selected_dish not in self.user_preference['dishes']:
                self.user_preference['dishes'][selected_dish] = {
                    'selection_count': 0,
                    'recommendation_count': 0
                }
            
            self.user_preference['dishes'][selected_dish]['selection_count'] += 1
            self.user_preference['total_selections'] += 1
            self.save_user_preference()

    def reset_user_preference(self):
        '''Reset user preference to default values'''
        print('Resetting user preferences...')
        
        # Create new preference structure with default values
        self.user_preference = {'dishes': {}, 'total_selections': 0}
        
        # Save the reset preferences
        self.save_user_preference()
        
        print('User preferences have been reset successfully!')
        return
    
    def update_recommendation_count(self, recommended_dishes):
        '''Update recommendation count for recommended dishes'''
        for dish in recommended_dishes: # Iterate through recommended dishes given by the system
            if dish in self.user_preference['dishes']:
                self.user_preference['dishes'][dish]['recommendation_count'] += 1
        self.save_user_preference()
    
    def get_random_cuisines(self, count=5):
        '''Randomly select a few cuisines'''
        # If the number of cuisines is less than or equal to count, return all cuisines
        if len(self.cuisines) <= count:
            return self.cuisines
        return random.sample(self.cuisines, count) # Randomly select 5 cuisines
    
    def get_recommendations_by_cuisine(self, cuisine, count=5):
        '''Recommend dishes based on each cuisine'''
        if cuisine not in self.dishes_by_cuisine: # Check if the cuisine exists
            return []
        
        available_dishes = self.dishes_by_cuisine[cuisine]
        
        # If no dishes available, return empty list
        if not available_dishes:
            return []
        
        # If the number of selections is less than 10, recommend dishes that have not been selected
        if self.user_preference['total_selections'] < 10:
        # First priority: dishes that have never been recommended
            never_recommended = [dish for dish in available_dishes 
                                if dish in self.user_preference['dishes'] and 
                                self.user_preference['dishes'][dish]['recommendation_count'] == 0]
            
            # Second priority: dishes that have been recommended but not selected
            recommended_not_selected = [dish for dish in available_dishes 
                                        if dish in self.user_preference['dishes'] and
                                        self.user_preference['dishes'][dish]['recommendation_count'] > 0 and
                                        self.user_preference['dishes'][dish]['selection_count'] == 0]
            
            # Third priority: other dishes
            other_dishes = [dish for dish in available_dishes 
                            if dish not in never_recommended and dish not in recommended_not_selected]
            
            # Combine the lists with priority order
            prioritized_dishes = never_recommended + recommended_not_selected + other_dishes
            
            # Return at least 'count' dishes or all if less than 'count'
            if len(prioritized_dishes) <= count:
                result = prioritized_dishes
            else:
                # Randomly sample from prioritized list, but ensure diversity
                # Take more from never_recommended if available
                num_never = min(len(never_recommended), count-1)  # Leave at least one spot for other categories
                result = random.sample(never_recommended, num_never) if num_never > 0 else []
                
                # Fill the rest with recommended_not_selected and other_dishes
                remaining_count = count - len(result)
                if remaining_count > 0 and recommended_not_selected:
                    num_rec_not_sel = min(len(recommended_not_selected), remaining_count)
                    result.extend(random.sample(recommended_not_selected, num_rec_not_sel))
                    
                remaining_count = count - len(result)
                if remaining_count > 0 and other_dishes:
                    result.extend(random.sample(other_dishes, min(len(other_dishes), remaining_count)))
            
            # Update recommendation counts
            self.update_recommendation_count(result)
            return result
        
        # After 10 selections, recommend based on selection frequency
        # Sort all dishes, every recommendation includes 2 high-frequency and 5 low-frequency or unselected dishes
        all_cuisine_dishes = [(dish, 
                               self.user_preference['dishes'].get(dish, {'selection_count': 0, 'recommendation_count': 0})) 
                               for dish in available_dishes]
        
        # Sort by selection count descending, then by recommendation count ascending
        all_cuisine_dishes.sort(key=lambda x: (-x[1]['selection_count'], x[1]['recommendation_count']))
        
        # Select 2 high-frequency dishes
        high_frequency = [dish[0] for dish in all_cuisine_dishes[:2]]
        
        # Sort the remaining dishes by recommendation count ascending, then by selection count descending
        remaining_dishes = all_cuisine_dishes[2:]
        remaining_dishes.sort(key=lambda x: (x[1]['recommendation_count'], -x[1]['selection_count']))
        
        # Select 5 low-frequency or unselected dishes
        low_frequency = [dish[0] for dish in remaining_dishes[:5]]
        
        # Merge high-frequency and low-frequency dishes to recommend
        recommendations = high_frequency + low_frequency
        
        # If the number of recommendations is less than 7, fill with random dishes
        if len(recommendations) < 7:
            remaining_count = 7 - len(recommendations)
            remaining_pool = [dish for dish in available_dishes if dish not in recommendations]
            if remaining_pool and remaining_count > 0:
                if len(remaining_pool) <= remaining_count:
                    recommendations.extend(remaining_pool) # Fill with all remaining dishes
                else: # Randomly select remaining_count dishes
                    recommendations.extend(random.sample(remaining_pool, remaining_count))
        
        # Update recommendation count for the recommended dishes
        self.update_recommendation_count(recommendations)
        
        return recommendations[:7] # Return the first 7 recommendations
    
    def check_cuisine_exists(self, cuisine):
        '''Check if a cuisine exists'''
        for cuisine_name in self.cuisines:
            if cuisine_name.lower() == cuisine.lower():
                return True
        return False
    
    def check_dish_exists(self, dish, cuisine=None):
        '''Check if a dish exists in a specific cuisine or all cuisines'''
        if cuisine:
            return dish in self.dishes_by_cuisine[cuisine]
        return dish in self.all_dishes
    
    def get_cuisine_for_dish(self, dish):
        '''Search for the cuisine of a dish'''
        for cuisine, dishes in self.dishes_by_cuisine.items():
            for menu_dish in dishes:
                if dish == menu_dish.lower():
                    return cuisine
        return None
    
    def run(self):
        '''Run the recommendation system'''
        print('\n-----Welcome to the Meal Recommendation System!-----')
        print('-----Please enter \'exit\' to quit the system at any time.-----')
        print('-----Enter \'reset\' to reset your preferences.-----')
        
        while True:
            # Get user's input
            choice = input('\nAny recommendation? (yes/no/exit/reset): ').strip().lower()
            
            if choice == 'exit':
                print('Exiting the system...')
                break
            
            elif choice == 'reset':
                confirm = input('Are you sure you want to reset all your preferences? (yes/no): ').strip().lower()
                if confirm == 'yes':
                    self.reset_user_preference()
                else:
                    print('Reset cancelled.')
            
            elif choice == 'yes':
                # Provide a random cuisine
                random_cuisines = self.get_random_cuisines()
                print('\nThere are some cuisines I have chosen to recommend to you:')
                for i, cuisine in enumerate(random_cuisines, 1):
                    print(f'{i}. {cuisine}')
                
                
                while True:
                    # Ask user to select a cuisine
                    cuisine_choice = input('\nPlease select a cuisine(index or name), or enter another cuisine name you prefer(case sensitive): ').strip()
                    
                    if cuisine_choice == 'exit':
                        print('Exiting the system...')
                        exit()
                    
                    # Check if the input is a number
                    if cuisine_choice.isdigit():
                        idx = int(cuisine_choice) - 1
                        if 0 <= idx < len(random_cuisines):
                            cuisine_choice = random_cuisines[idx]
                        else:
                            print('Invalid index, please try again')
                            continue
                    
                    
                    # Check if the cuisine exists
                    if not self.check_cuisine_exists(cuisine_choice):
                        print(f'\'{cuisine_choice}\' is not a valid cuisine, please try again')
                        continue
                    
                    
                    # Get recommendations based on the selected cuisine
                    recommendations = self.get_recommendations_by_cuisine(cuisine_choice)
                    
                    if not recommendations:
                        print(f'There are no dishes in \'{cuisine_choice}\', please try another cuisine')
                        continue
                    
                    print(f'\nRecommended dishes of {cuisine_choice}:')
                    for i, dish in enumerate(recommendations, 1):
                        print(f'{i}. {dish}')
                    
                    
                    while True:
                        # Ask user to select a dish
                        dish_choice = input('\nPlease select a dish(index or name), or enter another dish name you prefer(case sensitive): ').strip()
                        
                        if dish_choice == 'exit':
                            print('Exiting the system...')
                            exit()
                        
                        # Check if the input is a number
                        selected_dish = dish_choice
                        if dish_choice.isdigit():
                            idx = int(dish_choice) - 1
                            if 0 <= idx < len(recommendations):
                                selected_dish = recommendations[idx]
                        
                        # Check if the dish exists in the selected cuisine
                        if not self.check_dish_exists(selected_dish, cuisine_choice):
                            # Not found in the selected cuisine, check if it exists in all cuisines
                            dish_cuisine = self.get_cuisine_for_dish(selected_dish)
                            if dish_cuisine:
                                print(f'\'{selected_dish}\' is found in \'{dish_cuisine}\'')
                                selected_dish = selected_dish
                                break
                            else:
                                print(f'There is no dish named \'{selected_dish}\', please try again')
                                continue
                        else:
                            # Dish found in the selected cuisine
                            print(f'You\'ve selected \'{selected_dish}\' from \'{cuisine_choice}\'')
                            break
                        
                    break # End of cuisine selection
                
                # Update user preference with the selected dish
                self.update_user_preference(selected_dish)
                print(f'\n-----You have chosen: {selected_dish}, enjoy your meal!-----')
                
            elif choice == 'no':
                print('zzzzz System is in sleep mode, enter anything to wake it up. zzzzz')
                input()
            
            else:
                print('Invalid input, please enter \'yes\' or \'no\'.')

# Main function to run the system
if __name__ == '__main__':
    MRS = FoodRecommendationSystem()
    MRS.run()