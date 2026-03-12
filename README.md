# SavorSync: Culturally-Aware Meal Planning Agent

This project is a CS5100 final project that models weekly meal planning as a search and optimization problem inspired by an earlier HCI project idea.

## Project Idea

The goal of this project is to build an intelligent meal-planning agent that generates and improves weekly meal plans under multiple objectives and constraints.

Instead of recommending one recipe at a time, the system treats an entire weekly meal plan as a single search state. The agent then evaluates that state with a weighted utility function and improves it using local search.

The current prototype focuses on these ideas from AI:

- **state representation**: a full weekly meal plan is one state
- **actions / neighbors**: meal plans are modified by replacing one meal or swapping meals
- **utility-based evaluation**: plans are scored based on multiple factors
- **hard constraints**: invalid plans are rejected
- **local search**: hill climbing and simulated annealing are used to improve plans

## What the current version does

The current MVP includes:

- a small recipe dataset in JSON
- a weekly meal-plan state representation
- a weighted utility / scoring function
- hard nutrition constraints
- two search algorithms:
  - hill climbing
  - simulated annealing

The scoring function currently considers:

- protein
- vegetables
- ingredient accessibility
- cultural authenticity
- preparation time
- repetition penalty

## What the program is testing

This project is currently testing whether:

1. a weekly meal plan can be represented as a search state
2. a utility function can evaluate whether one plan is better than another
3. local search algorithms can improve a random initial meal plan
4. hard constraints and preference weights meaningfully shape the result

At this stage, the output does **not** need to be a perfect final meal plan. The main purpose is to verify that the AI search framework is working correctly.

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
│   └── main.py
├── README.md
└── .gitignore
```

## File Overview

### `data/recipes.json`
A small starter recipe dataset. Each recipe contains:
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
Implements the utility function and hard constraints.

### `src/neighbors.py`
Creates neighboring meal plans by replacing or swapping meals.

### `src/hill_climbing.py`
Implements hill climbing as a baseline local search method.

### `src/simulated_annealing.py`
Implements simulated annealing to help escape poor local optima.

### `src/main.py`
Runs the planner and prints the results.

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

From the project root folder, run: 

```bash
PYTHONPATH=src python3 src/main.py
```

## What You Should See
 
The program prints:
- an initial random meal plan
- a hill climbing result
- a simulated annealing result
- a score for each plan

### Example Output

```text
Initial Random Plan
==================================================
1. Green Curry Tofu | Thai | 30 min
2. Banh Mi Plate | Vietnamese | 20 min
3. Teriyaki Salmon | Japanese | 20 min
4. Ratatouille Plate | French | 35 min
5. Kimchi Fried Rice | Korean | 20 min
6. Pho Bowl | Vietnamese | 35 min
7. Grilled Chicken Salad | American | 20 min
8. Greek Chicken Plate | Greek | 30 min
9. Bulgogi Bowl | Korean | 30 min
10. Pasta Primavera | Italian | 30 min
Score: 219.74

Hill Climbing Result
==================================================
1. Greek Chicken Plate | Greek | 30 min
2. Grilled Chicken Salad | American | 20 min
3. Chicken Stir Fry | Chinese | 25 min
4. Thai Basil Chicken | Thai | 20 min
5. Bulgogi Bowl | Korean | 30 min
6. Chicken Tikka Bowl | Indian | 35 min
7. Fish Tacos | Mexican | 25 min
8. Falafel Bowl | Middle Eastern | 25 min
9. Chicken Alfredo | Italian | 30 min
10. Teriyaki Salmon | Japanese | 20 min
Score: 267.7

Simulated Annealing Result
==================================================
1. Fish Tacos | Mexican | 25 min
2. Greek Chicken Plate | Greek | 30 min
3. Chicken Stir Fry | Chinese | 25 min
4. Pho Bowl | Vietnamese | 35 min
5. Chicken Alfredo | Italian | 30 min
6. Bulgogi Bowl | Korean | 30 min
7. Teriyaki Salmon | Japanese | 20 min
8. Chicken Tikka Bowl | Indian | 35 min
9. Thai Basil Chicken | Thai | 20 min
10. Grilled Chicken Salad | American | 20 min
Score: 269.0

Search Comparison
==================================================
Initial Score: 219.74
Hill Climbing Score: 267.7
Simulated Annealing Score: 269.0
Better algorithm in this run: Simulated Annealing
```

### How to Interpret the Output

If the hill climbing or simulated annealing score is higher than the initial random plan score, that means the search algorithm successfully improved the meal plan according to the current utility function.

The program also prints a direct comparison of the final scores for both search methods. This makes it easier to see which algorithm performed better in a given run.

For example:

- Initial Score = 219.74
- Hill Climbing Score = 267.7
- Simulated Annealing Score = 269.0

In this example, simulated annealing produced the highest-scoring meal plan under the current utility function. This means the search framework is working.

## Important Note About Current Behavior

The current version may still produce somewhat repetitive meal plans. This does not mean the code is broken. It usually means the scoring function is still rewarding some recipes too strongly.

For example, if one recipe has:

- high protein
- decent accessibility
- strong authenticity
- low prep time

the search may keep selecting it.

This is a normal early-stage result. The next step is to refine the scoring function so the planner better balances:

- diversity
- nutrition
- practicality
- cultural factors

## Why Results May Vary Across Runs

Because the planner uses randomized initialization and stochastic neighbor exploration, results vary slightly across runs. This is expected for local search methods, especially simulated annealing. Despite this variability, the algorithms consistently improve the score of the initial candidate meal plan, showing that the search framework is functioning as intended.

## Current Limitations

This is still an early prototype. The current version does not yet include:

- more advanced ingredient substitution logic
- user-specific cuisine preference weights
- realistic nutrition totals by meal type
- explanation output for why a plan was chosen
- detailed evaluation plots

## Next Steps

Planned improvements include:

- expanding the recipe dataset
- strengthening diversity rules
- adding cuisine preference by country
- improving substitution and neighbor operators
- comparing hill climbing vs simulated annealing more systematically
- logging score improvement over time

## Summary

This prototype already demonstrates the core AI idea of the project:

A weekly meal plan can be modeled as a search state, evaluated with a utility function, constrained by nutritional requirements, and improved through local search methods.