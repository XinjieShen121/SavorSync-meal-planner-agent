from typing import Dict
from meal_plan import MealPlan


def score_meal_plan(plan: MealPlan, weights: Dict[str, float]) -> float:
    # Compute total values across the whole weekly meal plan
    total_prep = sum(meal["prep_time"] for meal in plan.meals)
    total_access = sum(meal["ingredient_accessibility"] for meal in plan.meals)
    total_auth = sum(meal["cultural_authenticity"] for meal in plan.meals)
    total_protein = sum(meal["nutrition"]["protein"] for meal in plan.meals)
    total_veg = sum(meal["nutrition"]["vegetables"] for meal in plan.meals)
    total_calories = sum(meal["nutrition"]["calories"] for meal in plan.meals)

    # Count repeated meals to discourage too much duplication
    names = [meal["name"] for meal in plan.meals]
    unique_names = len(set(names))
    repetition_penalty = len(names) - unique_names

    # Count how many different cuisines appear in the plan
    cuisines = [meal["cuisine"] for meal in plan.meals]
    unique_cuisines = len(set(cuisines))

    # Hard constraints
    if total_protein < 180:
        return float("-inf")
    if total_veg < 15:
        return float("-inf")
    if unique_names < 7:
        return float("-inf")

    # Start building the weighted utility score
    score = 0.0
    score += weights["protein"] * total_protein
    score += weights["vegetables"] * total_veg
    score += weights["accessibility"] * total_access
    score += weights["authenticity"] * total_auth
    score += weights["cuisine_diversity"] * unique_cuisines
    score -= weights["prep_time"] * total_prep
    score -= weights["repetition"] * repetition_penalty

    # Soft calorie regularization
    if total_calories > 4800:
        score -= (total_calories - 4800) * 0.02

    return score