import pytest

from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_hint_says_go_lower():
    # Regression: the hint messages were swapped, so a guess above the secret said "Go HIGHER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_hint_says_go_higher():
    # Regression: a guess below the secret used to say "Go LOWER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message
    assert "LOWER" not in message

def test_check_guess_int_secret_is_consistent_across_attempts():
    # Regression: the secret was turned into a string on even attempts, flipping the comparison.
    # With an int secret every call must use numeric comparison, so 100 vs 99 is always "Too High".
    for _ in range(4):
        outcome, message = check_guess(100, 99)
        assert outcome == "Too High"
        assert "LOWER" in message

def test_check_guess_does_not_fall_back_to_string_comparison():
    # Regression: the str fallback made "100" < "99". A str secret is now a misuse and must raise.
    with pytest.raises(TypeError):
        check_guess(100, "99")

@pytest.mark.parametrize("raw", ["0", "101", "105", "-5"])
def test_parse_guess_rejects_out_of_range(raw):
    # Regression: no range check, so 105 was accepted
    ok, value, err = parse_guess(raw, 1, 100)
    assert not ok
    assert value is None
    assert "between 1 and 100" in err

@pytest.mark.parametrize("raw, expected", [("1", 1), ("100", 100), ("50", 50)])
def test_parse_guess_accepts_boundaries_and_inside(raw, expected):
    assert parse_guess(raw, 1, 100) == (True, expected, None)

def test_parse_guess_uses_difficulty_range():
    # Regression: range text/check was hardcoded to 1-100; Easy is 1-20
    ok, _, err = parse_guess("50", 1, 20)
    assert not ok
    assert "between 1 and 20" in err
