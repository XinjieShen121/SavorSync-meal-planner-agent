from recipe_loader import load_recipes
from hill_climbing import hill_climb
from simulated_annealing import simulated_annealing
from scoring import score_meal_plan, get_score_breakdown
from neighbors import random_initial_plan


def print_score_breakdown(plan, weights):
    breakdown = get_score_breakdown(plan, weights)

    print("Key Metrics:")
    print(f"  Protein: {breakdown['total_protein']}")
    print(f"  Vegetables: {breakdown['total_vegetables']}")
    print(f"  Prep Time: {breakdown['total_prep_time']}")
    print(f"  Unique Cuisines: {breakdown['unique_cuisines']}")
    print(f"  Repetition Count: {breakdown['repetition_count']}")
    print(f"  Final Score: {breakdown['score']:.2f}")


def print_plan(title, plan, weights):
    print(f"\n{title}")
    print("=" * 50)
    for i, meal in enumerate(plan.meals, start=1):
        print(f"{i}. {meal['name']} | {meal['cuisine']} | {meal['prep_time']} min")

    print_score_breakdown(plan, weights)


def compare_results(initial_plan, hc_plan, sa_plan, weights):
    initial_score = score_meal_plan(initial_plan, weights)
    hc_score = score_meal_plan(hc_plan, weights)
    sa_score = score_meal_plan(sa_plan, weights)

    print("\nSearch Comparison")
    print("=" * 50)
    print(f"Initial Score: {initial_score:.2f}")
    print(f"Hill Climbing Score: {hc_score:.2f}")
    print(f"Simulated Annealing Score: {sa_score:.2f}")

    if sa_score > hc_score:
        print("Better algorithm in this run: Simulated Annealing")
    elif hc_score > sa_score:
        print("Better algorithm in this run: Hill Climbing")
    else:
        print("Both algorithms achieved the same score in this run.")

 # function runs one full experiment for one preference mode
def run_mode(mode_name, recipes, weights):
    print(f"\n\n{mode_name}")
    print("#" * 60)

    initial_plan = random_initial_plan(recipes)
    print_plan("Initial Random Plan", initial_plan, weights)

    hc_plan = hill_climb(recipes, weights)
    sa_plan = simulated_annealing(recipes, weights)

    print_plan("Hill Climbing Result", hc_plan, weights)
    print_plan("Simulated Annealing Result", sa_plan, weights)

    compare_results(initial_plan, hc_plan, sa_plan, weights)


def main():
    recipes = load_recipes("data/recipes.json")

    health_weights = {
        "protein": 1.0,
        "vegetables": 3.0,
        "accessibility": 1.5,
        "authenticity": 1.5,
        "cuisine_diversity": 3.0,
        "prep_time": 0.20,
        "repetition": 12.0,
    }

    convenience_weights = {
        "protein": 0.7,
        "vegetables": 2.0,
        "accessibility": 3.0,
        "authenticity": 1.2,
        "cuisine_diversity": 2.0,
        "prep_time": 0.45,
        "repetition": 10.0,
    }

    # cultural_weights = {
    #     "protein": 0.7,
    #     "vegetables": 2.0,
    #     "accessibility": 1.5,
    #     "authenticity": 3.0,
    #     "cuisine_diversity": 5.0,
    #     "prep_time": 0.20,
    #     "repetition": 12.0,
    # }

    cultural_weights = {
    "protein": 0.45,
    "vegetables": 2.0,
    "accessibility": 1.2,
    "authenticity": 4.0,
    "cuisine_diversity": 6.5,
    "prep_time": 0.2,
    "repetition": 12.0,
}

    run_mode("HEALTH-FOCUSED MODE", recipes, health_weights)
    run_mode("CONVENIENCE-FOCUSED MODE", recipes, convenience_weights)
    run_mode("CULTURAL-EXPLORATION MODE", recipes, cultural_weights)


if __name__ == "__main__":
    main()