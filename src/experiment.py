import math
from recipe_loader import load_recipes
from hill_climbing import hill_climb
from simulated_annealing import simulated_annealing
from scoring import score_meal_plan


def safe_average(scores):
    valid_scores = [score for score in scores if math.isfinite(score)]
    if not valid_scores:
        return None
    return round(sum(valid_scores) / len(valid_scores), 2)


def format_scores(scores):
    formatted = []
    for score in scores:
        if math.isfinite(score):
            formatted.append(round(score, 2))
        else:
            formatted.append("-inf")
    return formatted


def run_experiment(mode_name, recipes, weights, runs=5):
    hc_scores = []
    sa_scores = []

    for _ in range(runs):
        hc_plan = hill_climb(recipes, weights)
        sa_plan = simulated_annealing(recipes, weights)

        hc_score = score_meal_plan(hc_plan, weights)
        sa_score = score_meal_plan(sa_plan, weights)

        hc_scores.append(hc_score)
        sa_scores.append(sa_score)

    hc_valid = [score for score in hc_scores if math.isfinite(score)]
    sa_valid = [score for score in sa_scores if math.isfinite(score)]

    hc_avg = safe_average(hc_scores)
    sa_avg = safe_average(sa_scores)

    print(f"\n{mode_name}")
    print("=" * 50)
    print(f"Runs: {runs}")

    print("\nHill Climbing Scores:", format_scores(hc_scores))
    print(f"Valid HC Runs: {len(hc_valid)}/{runs}")
    print("Average HC Score:", hc_avg if hc_avg is not None else "No valid runs")

    print("\nSimulated Annealing Scores:", format_scores(sa_scores))
    print(f"Valid SA Runs: {len(sa_valid)}/{runs}")
    print("Average SA Score:", sa_avg if sa_avg is not None else "No valid runs")

    if hc_avg is None and sa_avg is None:
        overall = "No valid comparison"
    elif hc_avg is None:
        overall = "Simulated Annealing"
    elif sa_avg is None:
        overall = "Hill Climbing"
    elif sa_avg > hc_avg:
        overall = "Simulated Annealing"
    elif hc_avg > sa_avg:
        overall = "Hill Climbing"
    else:
        overall = "Tie"

    print(f"\nOverall better in {mode_name}: {overall}")

    return {
        "mode": mode_name,
        "hc_avg": hc_avg,
        "sa_avg": sa_avg,
        "winner": overall,
        "hc_valid": len(hc_valid),
        "sa_valid": len(sa_valid),
    }


if __name__ == "__main__":
    recipes = load_recipes("data/recipes.json")

    health_weights = {
        "protein": 1.2,
        "vegetables": 3.0,
        "accessibility": 2.0,
        "authenticity": 2.0,
        "cuisine_diversity": 4.0,
        "prep_time": 0.3,
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

    cultural_weights = {
        "protein": 0.7,
        "vegetables": 2.0,
        "accessibility": 1.5,
        "authenticity": 3.0,
        "cuisine_diversity": 5.0,
        "prep_time": 0.2,
        "repetition": 12.0,
    }

    summaries = []
    summaries.append(run_experiment("HEALTH-FOCUSED MODE", recipes, health_weights, runs=5))
    summaries.append(run_experiment("CONVENIENCE-FOCUSED MODE", recipes, convenience_weights, runs=5))
    summaries.append(run_experiment("CULTURAL-EXPLORATION MODE", recipes, cultural_weights, runs=5))

    print("\n\nFINAL SUMMARY")
    print("=" * 50)
    for result in summaries:
        print(
            f"{result['mode']}: "
            f"HC Avg = {result['hc_avg']}, "
            f"SA Avg = {result['sa_avg']}, "
            f"Winner = {result['winner']}"
        )