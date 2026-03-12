from recipe_loader import load_recipes
from hill_climbing import hill_climb
from simulated_annealing import simulated_annealing
from scoring import score_meal_plan
from neighbors import random_initial_plan


def print_plan(title, plan, weights):
    print(f"\n{title}")
    print("=" * 50)

    # Go through each meal in the plan and print its name, cuisine, and prep time
    for i, meal in enumerate(plan.meals, start=1):
        print(f"{i}. {meal['name']} | {meal['cuisine']} | {meal['prep_time']} min")
    
    # Score the full meal plan using the utility function
    print("Score:", score_meal_plan(plan, weights))


def compare_results(initial_plan, hc_plan, sa_plan, weights):
    # Compute scores for the initial plan and the two search results
    initial_score = score_meal_plan(initial_plan, weights)
    hc_score = score_meal_plan(hc_plan, weights)
    sa_score = score_meal_plan(sa_plan, weights)

    print("\nSearch Comparison")
    print("=" * 50)
    print(f"Initial Score: {initial_score}")
    print(f"Hill Climbing Score: {hc_score}")
    print(f"Simulated Annealing Score: {sa_score}")

    # Compare the two search methods
    if sa_score > hc_score:
        print("Better algorithm in this run: Simulated Annealing")
    elif hc_score > sa_score:
        print("Better algorithm in this run: Hill Climbing")
    else:
        print("Both algorithms achieved the same score in this run.")


def main():
    # Load the recipe dataset
    recipes = load_recipes("data/recipes.json")

    # Define the utility weights used by the scoring function
    weights = {
        "protein": 0.8,
        "vegetables": 2.5,
        "accessibility": 2.0,
        "authenticity": 2.0,
        "cuisine_diversity": 4.0,
        "prep_time": 0.25,
        "repetition": 12.0,
    }

    # Create and print a random starting meal plan
    initial_plan = random_initial_plan(recipes)
    print_plan("Initial Random Plan", initial_plan, weights)

    # Run hill climbing and simulated annealing to improve the plan
    hc_plan = hill_climb(recipes, weights)
    sa_plan = simulated_annealing(recipes, weights)

    # Print the final meal plans found by each search algorithm
    print_plan("Hill Climbing Result", hc_plan, weights)
    print_plan("Simulated Annealing Result", sa_plan, weights)

    compare_results(initial_plan, hc_plan, sa_plan, weights)


if __name__ == "__main__":  ## run the full experiment
    main() 