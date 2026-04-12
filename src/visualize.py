import matplotlib.pyplot as plt
from recipe_loader import load_recipes
from hill_climbing import hill_climb
from simulated_annealing import simulated_annealing
from genetic_algorithm import genetic_algorithm


def plot_convergence(recipes, weights, mode_name, iterations=500, generations=500):
    # run hill climbing and return both the final plan and score history
    hc_plan, hc_history = hill_climb(
        recipes,
        weights,
        iterations=iterations,
        return_history=True
    )

    # Run simulated annealing and return both the final plan and score history
    sa_plan, sa_history = simulated_annealing(
        recipes,
        weights,
        iterations=iterations,
        return_history=True
    )

    # run genetic algorithm and return both the final plan and score history
    ga_plan, ga_history = genetic_algorithm(
        recipes,
        weights,
        generations=generations,
        return_history=True
    )

    # create the figure
    plt.figure(figsize=(10, 6))

    # plot score history for all three algorithms
    plt.plot(hc_history, label="Hill Climbing", linewidth=2)
    plt.plot(sa_history, label="Simulated Annealing", alpha=0.7)
    plt.plot(ga_history, label="Genetic Algorithm", linewidth=2)

    # add labels and title
    plt.title(f"Convergence Comparison: {mode_name}")
    plt.xlabel("Iteration / Generation")
    plt.ylabel("Utility Score")
    plt.legend()
    plt.grid(True)

    # Save the figure as a PNG
    filename = f"{mode_name.lower().replace(' ', '_')}_convergence.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved convergence plot: {filename}")


def main():
    recipes = load_recipes("data/recipes.json")

    # health-focused mode
    health_weights = {
        "protein": 1.0,
        "vegetables": 3.0,
        "accessibility": 1.5,
        "authenticity": 1.5,
        "cuisine_diversity": 3.0,
        "prep_time": 0.20,
        "repetition": 12.0,
    }

    # convenience-focused mode
    convenience_weights = {
        "protein": 0.7,
        "vegetables": 2.0,
        "accessibility": 3.0,
        "authenticity": 1.2,
        "cuisine_diversity": 2.0,
        "prep_time": 0.45,
        "repetition": 10.0,
    }

    # cultural-exploration mode
    cultural_weights = {
        "protein": 0.45,
        "vegetables": 2.0,
        "accessibility": 1.2,
        "authenticity": 4.0,
        "cuisine_diversity": 6.5,
        "prep_time": 0.2,
        "repetition": 12.0,
    }

    # generate one plot for each preference mode
    plot_convergence(recipes, health_weights, "Health Focused Mode")
    plot_convergence(recipes, convenience_weights, "Convenience Focused Mode")
    plot_convergence(recipes, cultural_weights, "Cultural Exploration Mode")


if __name__ == "__main__":
    main()