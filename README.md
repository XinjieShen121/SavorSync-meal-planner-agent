# SavorSync: Culturally-Aware Meal Planning Agent

This project is a CS5100 final project that models weekly meal planning as a search and optimization problem inspired by an earlier HCI project idea.

## Project Idea

The goal of this project is to build an intelligent meal-planning agent that generates and improves weekly meal plans under multiple objectives and constraints.

Instead of recommending one recipe at a time, the system treats an entire weekly meal plan as a single search state. The agent then evaluates that state with a weighted utility function and improves it using local search.

The current system focuses on these ideas from AI:

- **state representation**: a full weekly meal plan is one search state
- **actions / neighbors**: meal plans are modified through local changes such as replacement, cuisine-aware substitution, prep-time reduction, and vegetable improvement
- **utility-based evaluation**: plans are scored based on multiple weighted factors
- **hard constraints**: invalid plans are rejected
- **local search**: hill climbing and simulated annealing are used to improve plans
- **preference modeling**: different user priorities are represented through different weight settings
- **experimental evaluation**: repeated runs are used to compare the two search algorithms

## What the current version does

The current version includes:

- an expanded recipe dataset in JSON with multiple cuisines and varied nutrition / prep-time profiles
- a weekly meal-plan state representation
- a weighted utility / scoring function
- hard nutrition and diversity constraints
- a score-breakdown system for interpretable output
- multiple neighbor-generation actions
- two search algorithms:
  - hill climbing
  - simulated annealing
- three user preference modes:
  - health-focused
  - convenience-focused
  - cultural-exploration-focused
- an experiment script for repeated algorithm comparison

The scoring function currently considers:

- protein
- vegetables
- ingredient accessibility
- cultural authenticity
- cuisine diversity
- preparation time
- repetition penalty

## What the program is testing

This project is currently testing whether:

1. a weekly meal plan can be represented as a search state
2. a utility function can evaluate whether one plan is better than another
3. local search algorithms can improve a random initial meal plan
4. different user preference modes produce meaningfully different plans
5. hill climbing and simulated annealing behave differently across repeated trials

At this stage, the project is still a prototype rather than a full product, but it already demonstrates the core AI planning framework.


## Project structure

```text
SavorSync-meal-planner-agent/
├── data/
│   └── recipes.json
├── src/
│   ├── recipe_loader.py
│   ├── meal_plan.py
│   ├── scoring.py
│   ├── neighbors.py
│   ├── hill_climbing.py
│   ├── simulated_annealing.py
│   ├── main.py
│   └── experiment.py
├── README.md
└── .gitignore
```

## File Overview

### `data/recipes.json`

Recipe dataset used by the planner. Each recipe contains:
- cuisine
- prep time
- ingredient accessibility
- cultural authenticity
- nutrition values

### `src/recipe_loader.py`
Loads the recipe dataset from JSON.

### `src/meal_plan.py`
Defines the meal-plan state.

### `src/scoring.py`
Implements the weighted utility function, hard constraints, and score-breakdown logic.

### `src/neighbors.py`
Creates neighboring meal plans through actions such as replacement, cuisine-aware substitution, prep-time reduction, diversity improvement, and vegetable improvement.

### `src/hill_climbing.py`
Implements hill climbing as a baseline local search method.

### `src/simulated_annealing.py`
Implements simulated annealing to help escape poor local optima.

### `src/main.py`
Runs the planner in the three preference modes and prints meal plans, key metrics, and algorithm comparisons.

### `src/experiment.py`
Runs repeated experiments to compare hill climbing and simulated annealing across preference modes.

## Setup Instructions

### 1. Create and activate a virtual environment

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install pandas
```

## How to Run the Project

### Run the main planner
From the project root folder, run: 

```bash
python3 src/main.py
```

### Run the experiment script
To compare hill climbing and simulated annealing across repeated trials, run: 

```bash
python3 src/experiment.py
```

## What You Should See
 
The main planner prints results for:
- health-focused mode
- convenience-focused mode
- cultural-exploration mode

For each mode, it prints:
- an initial random meal plan
- a hill climbing result
- a simulated annealing result
- key metrics
- a score comparison

### Example Output Style

```text
HEALTH-FOCUSED MODE
############################################################

Initial Random Plan
==================================================
1. Egg Fried Rice | Chinese | 20 min
2. Roasted Chickpea Wrap | Mediterranean | 15 min
3. Teriyaki Salmon | Japanese | 20 min
4. Vegetable Curry | Indian | 40 min
5. Falafel Bowl | Middle Eastern | 25 min
6. Lentil Soup | Middle Eastern | 35 min
7. Shrimp Rice Bowl | Vietnamese | 20 min
8. Mapo Tofu | Chinese | 30 min
9. Turkey Sandwich Plate | American | 15 min
10. Pho Bowl | Vietnamese | 35 min
Key Metrics:
  Protein: 187
  Vegetables: 19
  Prep Time: 255
  Unique Cuisines: 7
  Repetition Count: 0
  Final Score: 238.25

Hill Climbing Result
==================================================
1. Greek Chicken Plate | Greek | 30 min
2. Grilled Steak Bowl | American | 30 min
3. Fish Tacos | Mexican | 25 min
4. Mediterranean Salmon Plate | Mediterranean | 25 min
5. German Chicken Schnitzel Plate | German | 35 min
6. Grilled Chicken Salad | American | 20 min
7. Chicken Stir Fry | Chinese | 25 min
8. Chicken Breast Veggie Plate | American | 25 min
9. Salmon Quinoa Bowl | American | 25 min
10. Peruvian Chicken Bowl | South American | 30 min
Key Metrics:
  Protein: 300
  Vegetables: 25
  Prep Time: 270
  Unique Cuisines: 7
  Repetition Count: 0
  Final Score: 365.81

Simulated Annealing Result
==================================================
1. Chicken Rice Bowl | Japanese | 20 min
2. Salmon Quinoa Bowl | American | 25 min
3. Thai Basil Chicken | Thai | 20 min
4. Mediterranean Salmon Plate | Mediterranean | 25 min
5. Grilled Steak Bowl | American | 30 min
6. Chicken Stir Fry | Chinese | 25 min
7. Grilled Chicken Salad | American | 20 min
8. Greek Chicken Plate | Greek | 30 min
9. Chicken Breast Veggie Plate | American | 25 min
10. Peruvian Chicken Bowl | South American | 30 min
Key Metrics:
  Protein: 300
  Vegetables: 24
  Prep Time: 250
  Unique Cuisines: 7
  Repetition Count: 0
  Final Score: 366.79

Search Comparison
==================================================
Initial Score: 238.25
Hill Climbing Score: 365.81
Simulated Annealing Score: 366.79
Better algorithm in this run: Simulated Annealing


CONVENIENCE-FOCUSED MODE
############################################################

Initial Random Plan
==================================================
1. Thai Basil Chicken | Thai | 20 min
2. Mapo Tofu | Chinese | 30 min
3. Brazilian Black Bean Plate | South American | 35 min
4. Tuna Sandwich Plate | American | 10 min
5. Green Curry Tofu | Thai | 30 min
6. Moroccan Chickpea Stew | African | 40 min
7. Banh Mi Plate | Vietnamese | 20 min
8. Bibimbap | Korean | 35 min
9. Chana Masala | Indian | 30 min
10. Roasted Vegetable Plate | Mediterranean | 35 min
Key Metrics:
  Protein: 185
  Vegetables: 25
  Prep Time: 285
  Unique Cuisines: 9
  Repetition Count: 0
  Final Score: 102.88

Hill Climbing Result
==================================================
1. Salmon Quinoa Bowl | American | 25 min
2. Grilled Chicken Salad | American | 20 min
3. Mediterranean Salmon Plate | Mediterranean | 25 min
4. Grilled Steak Bowl | American | 30 min
5. Greek Chicken Plate | Greek | 30 min
6. Chicken Breast Veggie Plate | American | 25 min
7. Shrimp Rice Bowl | Vietnamese | 20 min
8. Chicken Stir Fry | Chinese | 25 min
9. Thai Basil Chicken | Thai | 20 min
10. Chicken Rice Bowl | Japanese | 20 min
Key Metrics:
  Protein: 296
  Vegetables: 24
  Prep Time: 240
  Unique Cuisines: 7
  Repetition Count: 0
  Final Score: 196.13

Simulated Annealing Result
==================================================
1. Chicken Stir Fry | Chinese | 25 min
2. Thai Basil Chicken | Thai | 20 min
3. Chicken Breast Veggie Plate | American | 25 min
4. Tuna Sandwich Plate | American | 10 min
5. Mediterranean Salmon Plate | Mediterranean | 25 min
6. Chicken Rice Bowl | Japanese | 20 min
7. Shrimp Rice Bowl | Vietnamese | 20 min
8. Grilled Steak Bowl | American | 30 min
9. Grilled Chicken Salad | American | 20 min
10. Salmon Quinoa Bowl | American | 25 min
Key Metrics:
  Protein: 290
  Vegetables: 23
  Prep Time: 220
  Unique Cuisines: 6
  Repetition Count: 0
  Final Score: 196.81

Search Comparison
==================================================
Initial Score: 102.88
Hill Climbing Score: 196.13
Simulated Annealing Score: 196.81
Better algorithm in this run: Simulated Annealing


CULTURAL-EXPLORATION MODE
############################################################

Initial Random Plan
==================================================
1. Chicken Rice Bowl | Japanese | 20 min
2. Baked Vegetable Casserole | French | 45 min
3. High-Protein Tofu Stir Fry | Chinese | 25 min
4. Teriyaki Salmon | Japanese | 20 min
5. Fish Tacos | Mexican | 25 min
6. Thai Basil Chicken | Thai | 20 min
7. Miso Soup Set | Japanese | 15 min
8. Shrimp Rice Bowl | Vietnamese | 20 min
9. Pho Bowl | Vietnamese | 35 min
10. Turkey Sandwich Plate | American | 15 min
Key Metrics:
  Protein: 223
  Vegetables: 20
  Prep Time: 240
  Unique Cuisines: 7
  Repetition Count: 0
  Final Score: 177.37

Hill Climbing Result
==================================================
1. Shrimp Rice Bowl | Vietnamese | 20 min
2. Zucchini Pasta Bowl | Italian | 25 min
3. Greek Chicken Plate | Greek | 30 min
4. German Chicken Schnitzel Plate | German | 35 min
5. Thai Basil Chicken | Thai | 20 min
6. Chicken Rice Bowl | Japanese | 20 min
7. Chicken Stir Fry | Chinese | 25 min
8. Mediterranean Salmon Plate | Mediterranean | 25 min
9. Peruvian Chicken Bowl | South American | 30 min
10. Salmon Quinoa Bowl | American | 25 min
Key Metrics:
  Protein: 270
  Vegetables: 24
  Prep Time: 255
  Unique Cuisines: 10
  Repetition Count: 0
  Final Score: 224.13

Simulated Annealing Result
==================================================
1. Bulgogi Bowl | Korean | 30 min
2. Peruvian Chicken Bowl | South American | 30 min
3. Chicken Rice Bowl | Japanese | 20 min
4. Fish Tacos | Mexican | 25 min
5. Shrimp Rice Bowl | Vietnamese | 20 min
6. Thai Basil Chicken | Thai | 20 min
7. Greek Chicken Plate | Greek | 30 min
8. Chicken Stir Fry | Chinese | 25 min
9. Chicken Breast Veggie Plate | American | 25 min
10. Veggie Buddha Bowl | Mediterranean | 20 min
Key Metrics:
  Protein: 266
  Vegetables: 24
  Prep Time: 245
  Unique Cuisines: 10
  Repetition Count: 0
  Final Score: 223.59

Search Comparison
==================================================
Initial Score: 177.37
Hill Climbing Score: 224.13
Simulated Annealing Score: 223.59
Better algorithm in this run: Hill Climbing
```

### How to Interpret the Output

If the hill climbing or simulated annealing score is higher than the initial random plan score, that means the search algorithm successfully improved the meal plan according to the current utility function.

The key metrics make it easier to explain why one plan scores better than another. For example:
- higher protein and vegetables usually help in health-focused mode
- lower prep time is especially important in convenience-focused mode
- higher cuisine diversity and authenticity matter more in cultural-exploration mode

A short way to read the output is:

- Initial Random Plan: the starting point before optimization
- Hill Climbing Result: a greedily improved plan that only accepts better local moves
- Simulated Annealing Result: a more flexible search result that can sometimes escape poorer local optima

#### Short explanation examples
- Initial Random Plan: This shows the starting meal plan before the search process improves it.
- Hill Climbing Result: This result shows how much the plan can improve through greedy local optimization.
- Simulated Annealing Result: This result shows how a more flexible search strategy may find a different or slightly stronger solution.
- Search Comparison: This summarizes which algorithm produced the higher final score in that run.

### Experimental Evaluation
The experiment script runs multiple trials and reports:
	•	hill climbing scores across runs
	•	simulated annealing scores across runs
	•	valid run counts
	•	average scores
	•	the better-performing algorithm in each mode

This helps evaluate whether one search method is more effective than the other under different user preferences.

## Experimental Results Summary

Repeated experiments show that both hill climbing and simulated annealing consistently produce strong valid meal plans. Their performance is often close, but the better-performing algorithm can vary by preference mode and random search path.

In general:
- simulated annealing often performs slightly better in health-focused mode
- hill climbing and simulated annealing perform similarly in convenience-focused mode
- both methods perform strongly in cultural-exploration mode, with small differences across runs

These results suggest that both search methods are effective for the meal-planning problem, while simulated annealing may have a slight advantage in more complex optimization settings.

## Why Results May Vary Across Runs

Because the planner uses randomized initialization and stochastic neighbor exploration, results vary slightly across runs. This is expected for local search methods, especially simulated annealing.

Even with this variability, both algorithms consistently improve meal plans and usually produce strong valid solutions.

## Current Limitations

This is still a prototype. The current version does not yet include:
- free-form user input for custom preferences
- ingredient-level substitution logic
- day-by-day meal scheduling (for example breakfast/lunch/dinner structure)
- automatic natural-language explanation generation inside the program output
- visualization of experimental results
- a front-end interface

## Next Steps

Planned improvements include:

- refining the distinction between preference modes even further
- improving cultural-mode behavior so it relies less on protein-heavy plans
- adding clearer natural-language explanations to the program output
- saving experiment summaries in a cleaner table or file
- optional visualization of score comparisons
- final polish for report and presentation

## Summary

This project builds a culturally-aware meal planning agent that treats a weekly meal plan as a search problem. The system evaluates candidate plans with a weighted utility function and improves them using local search methods, specifically hill climbing and simulated annealing. The current version supports multiple user preference modes, interpretable score breakdowns, richer neighbor actions, and repeated experiments comparing both algorithms.