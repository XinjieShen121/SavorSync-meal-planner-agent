# SavorSync: Culturally-Aware Meal Planning Agent

This project is a CS5100 final project that models weekly meal planning as a search and optimization problem inspired by an earlier HCI project idea.

## Project Idea

The goal of this project is to build an intelligent meal-planning agent that generates and improves weekly meal plans under multiple objectives and constraints.

Instead of recommending one recipe at a time, the system treats an entire weekly meal plan as a single search state. The agent then evaluates that state with a weighted utility function and improves it using search and optimization methods.


## AI Concepts Used:

- **state representation**: a full weekly meal plan is one search state
- **actions / neighbors**: meal plans are modified through local changes such as replacement, cuisine-aware substitution, prep-time reduction, and vegetable improvement
- **utility-based evaluation**: plans are scored based on multiple weighted factors
- **hard constraints**: invalid plans are rejected
- **local search**: hill climbing and simulated annealing are used to improve plans
- **evolutionary search**: a genetic algorithm is used as a third optimization method
- **preference modeling**: different user priorities are represented through different weight settings
- **experimental evaluation**: repeated runs are used to compare algorithm performance
- **convergence analysis**: score histories are tracked and visualized over time


## What the current version does

The current version includes:

- an expanded recipe dataset in JSON with multiple cuisines and varied nutrition / prep-time profiles
- a weekly meal-plan state representation
- a weighted utility / scoring function
- hard nutrition and diversity constraints
- a score-breakdown system for interpretable output
- multiple neighbor-generation actions
- three search algorithms:
  - hill climbing
  - simulated annealing
  - genetic algorithm
- three user preference modes:
  - health-focused
  - convenience-focused
  - cultural-exploration-focused
- an experiment script for repeated multi-run algorithm comparison
- convergence visualization for comparing algorithm behavior over time

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
3. different search algorithms can improve a random initial meal plan
4. different user preference modes produce meaningfully different plans
5. hill climbing, simulated annealing, and a genetic algorithm behave differently across repeated trials
6. convergence visualizations reveal different exploration-exploitation patterns across algorithms

At this stage, the project is still a research prototype rather than a consumer-facing application, but it already demonstrates the core AI planning and evaluation framework.


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
│   ├── genetic_algorithm.py
│   ├── main.py
│   ├── experiment.py
│   └── visualize.py
├── README.md
└── .gitignore
```

## File Overview

### `data/recipes.json`

Recipe dataset used by the planner. Each recipe contains:
-	cuisine
-	prep time
-	ingredient accessibility
-	cultural authenticity
-	nutrition values

### `src/recipe_loader.py`
Loads the recipe dataset from JSON.

### `src/meal_plan.py`
Defines the meal-plan state.

### `src/scoring.py`
Implements the weighted utility function, hard constraints, and score-breakdown logic.

### `src/neighbors.py`
Creates neighboring meal plans through actions such as replacement, cuisine-aware substitution, prep-time reduction, diversity improvement, and vegetable improvement.

### `src/hill_climbing.py`
Implements hill climbing as a baseline greedy local search method. It can also optionally return score history for convergence visualization.

### `src/simulated_annealing.py`
Implements simulated annealing as a stochastic local search method that can escape local optima. It can also optionally return score history for convergence visualization.

### `src/genetic_algorithm.py`
Implements a genetic algorithm using tournament selection, crossover, and mutation. It can also optionally return score history by generation.

### `src/main.py`
Runs the planner in the three preference modes and prints meal plans, key metrics, and algorithm comparisons.

### `src/experiment.py`
Runs repeated experiments to compare hill climbing, simulated annealing, and the genetic algorithm across preference modes.

### `src/visualize.py`
Generates convergence plots for hill climbing, simulated annealing, and the genetic algorithm across preference modes.

## Setup Instructions

### 1. Create and activate a virtual environment

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install pandas matplotlib
```

## How to Run the Project

### Run the main planner
From the project root folder, run: 

```bash
python3 src/main.py
```

### Run the experiment script
To compare hill climbing, simulated annealing, and the genetic algorithm across repeated trials, run: 

```bash
python3 src/experiment.py
```

### Generate convergence plots
To generate convergence plots for hill climbing, simulated annealing, and the genetic algorithm across all preference modes, run:

```bash
python3 src/visualize.py
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
- a genetic algorithm result
- key metrics
- a score comparison

### Example Output Style

```text
HEALTH-FOCUSED MODE
############################################################

Initial Random Plan
==================================================
1. Bean Burrito Bowl | Mexican | 20 min
2. Vegetable Curry | Indian | 40 min
3. Chicken Wrap | American | 15 min
4. Ethiopian Lentil Plate | African | 35 min
5. Bulgogi Bowl | Korean | 30 min
6. Roasted Chickpea Wrap | Mediterranean | 15 min
7. Kimchi Fried Rice | Korean | 20 min
8. Spanish Veggie Paella | Spanish | 40 min
9. Teriyaki Salmon | Japanese | 20 min
10. Salmon Quinoa Bowl | American | 25 min
Key Metrics:
  Protein: 199
  Vegetables: 25
  Prep Time: 260
  Unique Cuisines: 8
  Repetition Count: 0
  Final Score: 269.91

Hill Climbing Result
==================================================
1. Mediterranean Salmon Plate | Mediterranean | 25 min
2. Chicken Tikka Bowl | Indian | 35 min
3. Greek Chicken Plate | Greek | 30 min
4. Chicken Rice Bowl | Japanese | 20 min
5. Grilled Chicken Salad | American | 20 min
6. Chicken Breast Veggie Plate | American | 25 min
7. Grilled Steak Bowl | American | 30 min
8. Peruvian Chicken Bowl | South American | 30 min
9. Chicken Stir Fry | Chinese | 25 min
10. Salmon Quinoa Bowl | American | 25 min
Key Metrics:
  Protein: 304
  Vegetables: 24
  Prep Time: 265
  Unique Cuisines: 7
  Repetition Count: 0
  Final Score: 367.56

Simulated Annealing Result
==================================================
1. Peruvian Chicken Bowl | South American | 30 min
2. Mediterranean Salmon Plate | Mediterranean | 25 min
3. Chicken Breast Veggie Plate | American | 25 min
4. Grilled Steak Bowl | American | 30 min
5. Shrimp Rice Bowl | Vietnamese | 20 min
6. Grilled Chicken Salad | American | 20 min
7. Chicken Stir Fry | Chinese | 25 min
8. Greek Chicken Plate | Greek | 30 min
9. Chicken Rice Bowl | Japanese | 20 min
10. Salmon Quinoa Bowl | American | 25 min
Key Metrics:
  Protein: 297
  Vegetables: 25
  Prep Time: 250
  Unique Cuisines: 7
  Repetition Count: 0
  Final Score: 366.76

Genetic Algorithm Result
==================================================
1. Grilled Chicken Salad | American | 20 min
2. Chicken Breast Veggie Plate | American | 25 min
3. German Chicken Schnitzel Plate | German | 35 min
4. Thai Basil Chicken | Thai | 20 min
5. Mediterranean Salmon Plate | Mediterranean | 25 min
6. Greek Chicken Plate | Greek | 30 min
7. Peruvian Chicken Bowl | South American | 30 min
8. Chicken Stir Fry | Chinese | 25 min
9. Chicken Rice Bowl | Japanese | 20 min
10. Salmon Quinoa Bowl | American | 25 min
Key Metrics:
  Protein: 296
  Vegetables: 24
  Prep Time: 255
  Unique Cuisines: 8
  Repetition Count: 0
  Final Score: 364.99

Search Comparison
==================================================
Initial Score: 269.91
Hill Climbing Score: 367.56
Simulated Annealing Score: 366.76
Genetic Algorithm Score: 364.99
Best algorithm in this run: Hill Climbing
```

### How to Interpret the Output

If an algorithm’s final score is higher than the initial random plan score, that means the search algorithm successfully improved the meal plan according to the current utility function.

The key metrics make it easier to explain why one plan scores better than another. For example:
- higher protein and vegetables usually help in health-focused mode
- lower prep time is especially important in convenience-focused mode
- higher cuisine diversity and authenticity matter more in cultural-exploration mode

#### A short way to read the output is:

- Initial Random Plan: the starting point before optimization
- Hill Climbing Result: a greedily improved plan that only accepts better local moves
- Simulated Annealing Result: a more flexible search result that can sometimes escape poorer local optima
- Genetic Algorithm Result: an evolutionary search result built from population-based selection, crossover, and mutation
- Search Comparison: a summary of which algorithm produced the highest final score in that run

### Experimental Evaluation
The experiment script runs multiple trials and reports:
-	hill climbing scores across runs
-	simulated annealing scores across runs
- genetic algorithm scores across runs
-	valid run counts
-	average scores
-	the better-performing algorithm in each mode

This helps evaluate whether one search method is more effective than the others under different user preferences.

## Experimental Results Summary

Repeated experiments show that hill climbing, simulated annealing, and the genetic algorithm all generate valid high-scoring meal plans. In most runs, simulated annealing achieves the strongest or near-strongest average performance, suggesting that its ability to escape local optima is especially useful in this problem.

Hill climbing often performs competitively and converges quickly, while the genetic algorithm provides stable performance but generally underperforms the best local-search results under the current crossover and mutation design.

The genetic algorithm serves as a meaningful evolutionary baseline, although under the current crossover and mutation design it generally remains slightly below the strongest local-search results.

These results suggest that hill climbing and simulated annealing are the strongest methods overall, while the genetic algorithm provides a meaningful evolutionary baseline.

## Convergence Analysis
The convergence plots provide additional insight into algorithm behavior over time.
-	Hill Climbing improves rapidly in early iterations but often plateaus, showing its greedy tendency to get stuck in local optima.
-	Simulated Annealing is more variable because it sometimes accepts worse intermediate solutions, allowing broader exploration of the search space.
- Genetic Algorithm improves quickly in early generations through population-based search, though it may lose diversity after early convergence.

These plots help illustrate the different exploration-exploitation trade-offs across the three optimization methods.

## Why Results May Vary Across Runs

Because the planner uses randomized initialization and stochastic search behavior, results vary slightly across runs. This is expected for local search methods and evolutionary search.

Even with this variability, all three algorithms consistently improve meal plans and usually produce strong valid solutions.

## Current Limitations

This project is currently a Python-based research prototype rather than a user-facing application. Additional limitations include:
- the genetic algorithm may require further tuning to outperform local search methods consistently
- the scoring function uses fixed preference weights rather than adaptive or learned preferences
- the planner operates at the weekly level and does not model explicit day-by-day meal structure such as breakfast, lunch, and dinner
- ingredient substitution is handled at a heuristic cuisine-group level rather than a full ingredient-knowledge level
- the system does not yet support dynamic user input beyond predefined preference modes

## Future Work

Potential future improvements include:

- more advanced crossover and mutation operators for the genetic algorithm
- adaptive or learned preference weights
- more realistic scheduling constraints across days and meal types
- richer ingredient-level substitution logic
- exporting experiment results to cleaner tables or files
- optional integration into a lightweight user-facing application

## Summary

This project builds a culturally-aware meal planning agent that formulates weekly meal planning as a search and optimization problem. Candidate meal plans are evaluated with a weighted utility function and improved using three different search strategies: hill climbing, simulated annealing, and a genetic algorithm. The final system includes multiple preference modes, interpretable score breakdowns, repeated experiments, and convergence visualizations, enabling a full comparative study across greedy local search, stochastic local search, and evolutionary search.