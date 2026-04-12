import math
from recipe_loader import load_recipes
from hill_climbing import hill_climb
from simulated_annealing import simulated_annealing
from genetic_algorithm import genetic_algorithm
from scoring import score_meal_plan


def safe_average(scores):
    # here i only average the scores that are actually valid numbers
    valid_scores = [score for score in scores if math.isfinite(score)]

    # if no valid scores exist, just return None
    if not valid_scores:
        return None

    ## Round to 2 decimals so the printed summary looks cleaner
    return round(sum(valid_scores) / len(valid_scores), 2)


def format_scores(scores):
    # Format scores nicely before printing them
    formatted = []
    for score in scores:
        if math.isfinite(score):
            formatted.append(round(score, 2)) # valid scores get rounded
        else:
            formatted.append("-inf") #invalid ones show up as "-inf"
    return formatted


def run_experiment(mode_name, recipes, weights, runs=5):
    # store final scores for all three algorithms across repeated runs
    hc_scores = []
    sa_scores = []
    ga_scores = []

    # run several trials because search contains randomness
    for _ in range(runs):
        # oenerate plans using all three algorithms
        hc_plan = hill_climb(recipes, weights)
        sa_plan = simulated_annealing(recipes, weights)
        ga_plan = genetic_algorithm(recipes, weights)

        # score each final plan using the same utility function
        hc_score = score_meal_plan(hc_plan, weights)
        sa_score = score_meal_plan(sa_plan, weights)
        ga_score = score_meal_plan(ga_plan, weights)

        # save the scores so I can compare them after all runs finish
        hc_scores.append(hc_score)
        sa_scores.append(sa_score)
        ga_scores.append(ga_score)

    # count how many runs were valid for each algorithm
    hc_valid = [score for score in hc_scores if math.isfinite(score)]
    sa_valid = [score for score in sa_scores if math.isfinite(score)]
    ga_valid = [score for score in ga_scores if math.isfinite(score)]

    # Compute average scores using only valid runs
    hc_avg = safe_average(hc_scores)
    sa_avg = safe_average(sa_scores)
    ga_avg = safe_average(ga_scores)

    # Print experiment results for this mode
    print(f"\n{mode_name}")
    print("=" * 50)
    print(f"Runs: {runs}")

    print("\nHill Climbing Scores:", format_scores(hc_scores))
    print(f"Valid HC Runs: {len(hc_valid)}/{runs}")
    print("Average HC Score:", hc_avg if hc_avg is not None else "No valid runs")

    print("\nSimulated Annealing Scores:", format_scores(sa_scores))
    print(f"Valid SA Runs: {len(sa_valid)}/{runs}")
    print("Average SA Score:", sa_avg if sa_avg is not None else "No valid runs")

    print("\nGenetic Algorithm Scores:", format_scores(ga_scores))
    print(f"Valid GA Runs: {len(ga_valid)}/{runs}")
    print("Average GA Score:", ga_avg if ga_avg is not None else "No valid runs")

    # Decide which algorithm performed best on average
    averages = {
        "Hill Climbing": hc_avg,
        "Simulated Annealing": sa_avg,
        "Genetic Algorithm": ga_avg
    }

    # ignore any algorithm that had no valid average.
    valid_averages = {name: avg for name, avg in averages.items() if avg is not None}

    if not valid_averages:
        overall = "No valid comparison"
    else:
        best_score = max(valid_averages.values())
        winners = [name for name, avg in valid_averages.items() if avg == best_score]

        # If more than one algorithm has the same best average, report a tie.
        if len(winners) == 1:
            overall = winners[0]
        else:
            overall = "Tie: " + ", ".join(winners)

    print(f"\nOverall better in {mode_name}: {overall}")

    # Return summary dictionary for final summary print
    return {
        "mode": mode_name,
        "hc_avg": hc_avg,
        "sa_avg": sa_avg,
        "ga_avg": ga_avg,
        "winner": overall,
        "hc_valid": len(hc_valid),
        "sa_valid": len(sa_valid),
        "ga_valid": len(ga_valid),
    }


if __name__ == "__main__":
    # Load the full recipe dataset once before running experiments
    recipes = load_recipes("data/recipes.json")

    # Health-focused mode where i put more weight on nutrition
    health_weights = {
        "protein": 1.0,
        "vegetables": 3.0,
        "accessibility": 1.5,
        "authenticity": 1.5,
        "cuisine_diversity": 3.0,
        "prep_time": 0.20,
        "repetition": 12.0,
    }

    # Convenience-focused mode cares more about accessibility and lower prep time
    convenience_weights = {
        "protein": 0.7,
        "vegetables": 2.0,
        "accessibility": 3.0,
        "authenticity": 1.2,
        "cuisine_diversity": 2.0,
        "prep_time": 0.45,
        "repetition": 10.0,
    }

    # Cultural-exploration mode puts more emphasis on diversity and authenticity
    cultural_weights = {
        "protein": 0.45,
        "vegetables": 2.0,
        "accessibility": 1.2,
        "authenticity": 4.0,
        "cuisine_diversity": 6.5,
        "prep_time": 0.2,
        "repetition": 12.0,
    }

    # run experiments for all three preference modes
    summaries = []
    summaries.append(run_experiment("HEALTH-FOCUSED MODE", recipes, health_weights, runs=5))
    summaries.append(run_experiment("CONVENIENCE-FOCUSED MODE", recipes, convenience_weights, runs=5))
    summaries.append(run_experiment("CULTURAL-EXPLORATION MODE", recipes, cultural_weights, runs=5))

    # print one final summary so it is easy to compare modes in one places
    print("\n\nFINAL SUMMARY")
    print("=" * 50)
    for result in summaries:
        print(
            f"{result['mode']}: "
            f"HC Avg = {result['hc_avg']}, "
            f"SA Avg = {result['sa_avg']}, "
            f"GA Avg = {result['ga_avg']}, "
            f"Winner = {result['winner']}"
        )