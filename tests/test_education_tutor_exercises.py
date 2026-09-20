from persian_math.domain import Difficulty, EducationalLevel, UserProfile
from persian_math.education import curriculum_for, recommended_difficulty
from persian_math.exercises import ExerciseSpec, generate, validate_exercise
from persian_math.tutor import check_answer, next_hint, start_session


def test_curriculum_and_tutor():
    user = UserProfile("u1", EducationalLevel.HIGH_SCHOOL)
    assert curriculum_for(user).max_difficulty == Difficulty.MEDIUM
    session = start_session(user)
    assert next_hint(session, "معادله").action.value == "hint"
    assert check_answer(session, True).action.value == "check"


def test_generated_exercises_are_valid():
    exercises = generate(ExerciseSpec("algebra", Difficulty.EASY, count=5, seed=2))
    assert len(exercises) == 5
    assert all(validate_exercise(item) for item in exercises)


def test_adaptive_difficulty():
    user = UserProfile("u2", EducationalLevel.HIGH_SCHOOL)
    assert recommended_difficulty(user, 0.30) == Difficulty.EASY
    assert recommended_difficulty(user, 0.70) == Difficulty.MEDIUM
