# Meal Recommendation System - MRS

## Project Overview

The Meal Recommendation System is a Python-based command-line application designed to solve the everyday dilemma of "what to eat." The system intelligently recommends dishes based on user preferences and past selections while maintaining recommendation variety and freshness.

Key features include:
- Support for multiple cuisines and dishes
- Smart recommendation algorithm balancing user preferences and exploration
- Persistent storage of user preference data
- Interactive command-line interface

## Installation & Running

### Requirements
- Python 3.6 or higher
- No additional packages required (uses only Python standard library)

### Running the Application
1. Download the project files
2. Navigate to the project directory in command line
3. Execute the following command:
   ```
   python MealRec.py
   ```

## Features

### 1. Menu Management
The system stores dish data in a text file with the format "Cuisine,Dish Name". Upon startup, the program automatically loads the menu or creates a default one if the file doesn't exist.

### 2. User Preference Tracking
The system records the frequency of user dish selections and recommendation counts, storing this data in a JSON file. This data is used to optimize future recommendations.

### 3. Intelligent Recommendation Algorithm
- **Early Stage Strategy**: When a user has made fewer than 10 selections, the system prioritizes recommending dishes that haven't been recommended before, encouraging exploration
- **Personalized Strategy**: After 10 selections, the system provides a mix of frequently selected dishes (2) and low-frequency or never-recommended dishes (5)

### 4. Interactive Features
- Random cuisine recommendations for selection
- Dish recommendations based on selected cuisine
- Selection via index number or name
- Support for user-entered dishes not in recommendations
- User preference data reset capability
- System sleep and wake functionality

## User Guide

### Basic Commands
- `yes` - Start the recommendation process
- `no` - Put the system into sleep mode
- `reset` - Reset user preference data
- `exit` - Exit the system

### Usage Flow
1. Start the system; if existing user data exists, you'll be asked if you want to reset it
2. Enter `yes` to begin the recommendation process
3. Select a cuisine from the recommended list or enter another cuisine name
4. Select a dish from the recommended list or enter another dish name
5. The system records your choice to optimize future recommendations
6. Enter `no` to temporarily put the system to sleep; any input will wake it up
7. Enter `exit` at any time to quit the system

## File Descriptions

- MealRec.py - Main program file
- `menu.txt` - Menu storage file
- `user_preference.json` - User preference data storage file

## Customizing Your Menu

You can edit the `menu.txt` file to customize your menu. The file format is one dish record per line, with cuisine and dish name separated by a comma:
```
Chinese Cuisine,Dumplings
Chinese Cuisine,Kung Pao Chicken
Western Cuisine,Steak
Japanese Cuisine,Sushi
```

## Advanced Features

### User Preference Reset
If you want to try a fresh recommendation experience, use the `reset` command to clear all preference data.

### Cross-Cuisine Search
When you enter a dish that isn't in the currently selected cuisine, the system automatically searches other cuisines to find matching dishes.

## Troubleshooting

**Q: What if the system recommends too few dishes?**  
A: Edit the menu file to add more dishes; the system will load them on next startup.

**Q: How do I start completely fresh?**  
A: Enter `reset` after starting the program and confirm, or simply delete the `user_preference.json` file.

**Q: Can I add new cuisines?**  
A: Yes, simply add new cuisine and dish entries in the `menu.txt` file.

---

Hope this simple Meal Recommendation System helps solve your "what to eat" dilemmas!  
Bon appétit !