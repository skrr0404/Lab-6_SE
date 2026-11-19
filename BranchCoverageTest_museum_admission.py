"""
Lab 6 - Branch coverage tests for museum_admission.py
S Kushal Raju | PES2UG24AM139 | L6_L7_54 Museum Admission

Goal: make every decision (if / elif) evaluate to both True and False,
and test the boundary value on each side of every comparison.
Each test name says which branch outcome it forces.
"""
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ======================= ticket_price =======================
# Decisions: category valid? | age < 0? | age < 5? | monday? | weekend? |
#            guided tour? | student (inside guided tour)?

def test_category_invalid_true():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("vip", 30, "tuesday", False)


def test_category_is_case_sensitive():
    # "Adult" is not a key in BASE_PRICE, so it takes the invalid branch
    with pytest.raises(ValueError):
        ticket_price("Adult", 30, "tuesday", False)


def test_age_negative_true():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_age_zero_is_valid_and_free():
    # boundary: age < 0 False, age < 5 True
    assert ticket_price("child", 0, "tuesday", False) == 0


def test_age_four_free_boundary():
    assert ticket_price("child", 4, "saturday", True) == 0


def test_age_five_pays_boundary():
    # boundary: age < 5 False
    assert ticket_price("child", 5, "tuesday", False) == 100


@pytest.mark.parametrize("category, expected", [
    ("adult", 150), ("student", 75), ("child", 50), ("senior", 100),
])
def test_monday_true_half_price(category, expected):
    assert ticket_price(category, 30, "monday", False) == expected


@pytest.mark.parametrize("day", ["saturday", "sunday"])
def test_monday_false_weekend_true(day):
    assert ticket_price("adult", 30, day, False) == 350


@pytest.mark.parametrize("day", ["tuesday", "wednesday", "thursday", "friday"])
def test_monday_false_weekend_false(day):
    assert ticket_price("adult", 30, day, False) == 300


def test_day_is_case_sensitive():
    # "Monday" does not match "monday", so no discount is applied
    assert ticket_price("adult", 30, "Monday", False) == 300


def test_guided_true_student_true():
    assert ticket_price("student", 20, "tuesday", True) == 200


@pytest.mark.parametrize("category, expected", [
    ("adult", 400), ("child", 200), ("senior", 300),
])
def test_guided_true_student_false(category, expected):
    assert ticket_price(category, 30, "tuesday", True) == expected


def test_guided_false():
    assert ticket_price("senior", 70, "tuesday", False) == 200


def test_monday_with_guided_tour_combined():
    # discount applied first, then the tour fee
    assert ticket_price("adult", 30, "monday", True) == 250


def test_weekend_student_with_guided_tour_combined():
    assert ticket_price("student", 19, "sunday", True) == 250


# ======================= group_discount =======================
# Decisions: size < 1? | school? | school size >= 20? |
#            public size >= 15? | public size >= 8?

@pytest.mark.parametrize("size", [0, -5])
def test_group_size_invalid_true(size):
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(size, False)


def test_group_size_one_valid_boundary():
    assert group_discount(1, False) == 0


def test_school_true_size_20_boundary():
    assert group_discount(20, True) == 40


def test_school_true_size_19_boundary():
    assert group_discount(19, True) == 25


def test_school_true_single_student():
    assert group_discount(1, True) == 25


def test_school_false_size_15_boundary():
    assert group_discount(15, False) == 20


def test_school_false_size_14_boundary():
    assert group_discount(14, False) == 10


def test_school_false_size_8_boundary():
    assert group_discount(8, False) == 10


def test_school_false_size_7_boundary():
    assert group_discount(7, False) == 0


def test_school_false_very_large_group():
    assert group_discount(500, False) == 20


# ======================= gallery_entry =======================
# Decisions: inside >= capacity? | (>= 90% full AND no timed slot)?

def test_full_true_exact_capacity():
    assert gallery_entry(100, 100, False) == "wait"


def test_full_true_over_capacity():
    assert gallery_entry(120, 100, True) == "wait"


def test_full_true_even_with_timed_slot():
    assert gallery_entry(100, 100, True) == "wait"


def test_ninety_percent_no_slot_queue_boundary():
    # exactly 90% full: 90*10 >= 100*9 is True
    assert gallery_entry(90, 100, False) == "queue"


def test_ninety_percent_with_slot_enter():
    # >= 90% but has a timed slot, so the compound condition is False
    assert gallery_entry(90, 100, True) == "enter"


def test_just_below_ninety_percent_enter_boundary():
    assert gallery_entry(89, 100, False) == "enter"


def test_empty_gallery_enter():
    assert gallery_entry(0, 100, False) == "enter"


def test_small_capacity_rounding():
    # capacity 10: 9 inside is exactly 90% -> queue without a slot
    assert gallery_entry(9, 10, False) == "queue"
    assert gallery_entry(8, 10, False) == "enter"
