

from typing import Dict
from meal_plan import MealPlan


# add a new function to calculate all the useful totals
def get_score_breakdown(plan: MealPlan, weights: Dict[str, float]) -> Dict[str, float]:
    total_prep = sum(meal["prep_time"] for meal in plan.meals)
    total_access = sum(meal["ingredient_accessibility"] for meal in plan.meals)
    total_auth = sum(meal["cultural_authenticity"] for meal in plan.meals)
    total_protein = sum(meal["nutrition"]["protein"] for meal in plan.meals)
    total_veg = sum(meal["nutrition"]["vegetables"] for meal in plan.meals)
    total_calories = sum(meal["nutrition"]["calories"] for meal in plan.meals)

    names = [meal["name"] for meal in plan.meals]
    unique_names = len(set(names))
    repetition_count = len(names) - unique_names

    cuisines = [meal["cuisine"] for meal in plan.meals]
    unique_cuisines = len(set(cuisines))

    # Check hard constraints first
    hard_constraint_failed = (
        total_protein < 180 or
        total_veg < 15 or
        unique_names < 7
    )

    score = 0.0
    if not hard_constraint_failed:
        score += weights["protein"] * total_protein
        score += weights["vegetables"] * total_veg
        score += weights["accessibility"] * total_access
        score += weights["authenticity"] * total_auth
        score += weights["cuisine_diversity"] * unique_cuisines
        score -= weights["prep_time"] * total_prep
        score -= weights["repetition"] * repetition_count

        # Soft calorie regularization
        if total_calories > 4800:
            score -= (total_calories - 4800) * 0.02
    else:
        score = float("-inf")

    return {
        "total_protein": total_protein,
        "total_vegetables": total_veg,
        "total_calories": total_calories,
        "total_prep_time": total_prep,
        "total_accessibility": total_access,
        "total_authenticity": total_auth,
        "unique_meals": unique_names,
        "unique_cuisines": unique_cuisines,
        "repetition_count": repetition_count,
        "score": score,
    }


# breakdown and returns the final score
def score_meal_plan(plan: MealPlan, weights: Dict[str, float]) -> float:
    breakdown = get_score_breakdown(plan, weights)
    return breakdown["score"]