from recipe_loader import load_recipes
from hill_climbing import hill_climb
from simulated_annealing import simulated_annealing
from genetic_algorithm import genetic_algorithm
from scoring import score_meal_plan, get_score_breakdown
from neighbors import random_initial_plan


def print_score_breakdown(plan, weights):
    # Get the detailed score information for the current meal plan
    breakdown = get_score_breakdown(plan, weights)

    print("Key Metrics:")
    print(f"  Protein: {breakdown['total_protein']}")
    print(f"  Vegetables: {breakdown['total_vegetables']}")
    print(f"  Prep Time: {breakdown['total_prep_time']}")
    print(f"  Unique Cuisines: {breakdown['unique_cuisines']}")
    print(f"  Repetition Count: {breakdown['repetition_count']}")
    print(f"  Final Score: {breakdown['score']:.2f}")


def print_plan(title, plan, weights):
    # print a section title, then list the meals in the plan
    print(f"\n{title}")
    print("=" * 50)

    # print each meal in the meal plan
    for i, meal in enumerate(plan.meals, start=1):
        print(f"{i}. {meal['name']} | {meal['cuisine']} | {meal['prep_time']} min")

    # show the score breakdown right under the meal list
    print_score_breakdown(plan, weights)


def compare_results(initial_plan, hc_plan, sa_plan, ga_plan, weights):
    # score the starting random plan and all three final algorithm outputs
    initial_score = score_meal_plan(initial_plan, weights)
    hc_score = score_meal_plan(hc_plan, weights)
    sa_score = score_meal_plan(sa_plan, weights)
    ga_score = score_meal_plan(ga_plan, weights)

    print("\nSearch Comparison")
    print("=" * 50)
    print(f"Initial Score: {initial_score:.2f}")
    print(f"Hill Climbing Score: {hc_score:.2f}")
    print(f"Simulated Annealing Score: {sa_score:.2f}")
    print(f"Genetic Algorithm Score: {ga_score:.2f}")

    # compare only the algorithms, not the initial random baseline
    scores = {
        "Hill Climbing": hc_score,
        "Simulated Annealing": sa_score,
        "Genetic Algorithm": ga_score
    }

    best_score = max(scores.values())
    winners = [name for name, score in scores.items() if score == best_score]

    if len(winners) == 1:
        print(f"Best algorithm in this run: {winners[0]}")
    else:
        print("Tie between:", ", ".join(winners))


def run_mode(mode_name, recipes, weights):
    # run one full demo for one preference mode
    print(f"\n\n{mode_name}")
    print("#" * 60)

    # first create one random starting meal plan before optimization
    initial_plan = random_initial_plan(recipes)
    print_plan("Initial Random Plan", initial_plan, weights)

    # run all three algorithms using the same recipes and weight setting
    hc_plan = hill_climb(recipes, weights)
    sa_plan = simulated_annealing(recipes, weights)
    ga_plan = genetic_algorithm(recipes, weights)

    # print the optimized results from all three algorithms
    print_plan("Hill Climbing Result", hc_plan, weights)
    print_plan("Simulated Annealing Result", sa_plan, weights)
    print_plan("Genetic Algorithm Result", ga_plan, weights)

    # print the score comparison at the end of this mode
    compare_results(initial_plan, hc_plan, sa_plan, ga_plan, weights)


def main():
    # load the recipe dataset from the JSON file
    recipes = load_recipes("data/recipes.json")

    # Health-focused mode:
    # reward protein and vegetables more strongly
    health_weights = {
        "protein": 1.0,
        "vegetables": 3.0,
        "accessibility": 1.5,
        "authenticity": 1.5,
        "cuisine_diversity": 3.0,
        "prep_time": 0.20,
        "repetition": 12.0,
    }

    # Convenience-focused mode:
    # reward accessibility and low prep time more strongly
    convenience_weights = {
        "protein": 0.7,
        "vegetables": 2.0,
        "accessibility": 3.0,
        "authenticity": 1.2,
        "cuisine_diversity": 2.0,
        "prep_time": 0.45,
        "repetition": 10.0,
    }

    # Cultural-exploration mode:
    # reduce protein importance and reward authenticity + cuisine diversity more
    cultural_weights = {
        "protein": 0.45,
        "vegetables": 2.0,
        "accessibility": 1.2,
        "authenticity": 4.0,
        "cuisine_diversity": 6.5,
        "prep_time": 0.2,
        "repetition": 12.0,
    }

    # run the planner for all three preference modes
    run_mode("HEALTH-FOCUSED MODE", recipes, health_weights)
    run_mode("CONVENIENCE-FOCUSED MODE", recipes, convenience_weights)
    run_mode("CULTURAL-EXPLORATION MODE", recipes, cultural_weights)


if __name__ == "__main__":
    main()