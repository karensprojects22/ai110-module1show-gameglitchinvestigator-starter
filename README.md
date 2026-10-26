# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Entered a guess of 37
2. Game returns "Go Higher"
3. Enters a guess of 56
4. Game returns "Go Higher"
5. Enters a guess of 78
6. Game returns "Go Higher"
7. Enters guess of 90
8. Game returns "Go Higher"
9. Enters guesss of 99
10. Game returns "Go Lower"
11. Enters guess of 95
12. Game returns "Go Lower"
13. Enters guess of 97
14. Game enters "Go Lower"
15. Enters guess of 92
16. Ran out of attempts. Was told the secret number was 93. And my score is in the negatives. 

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python3 -m pytest tests -v
============================= test session starts ==============================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/karenalabi/source/CodePath/foundations-of-ai-engineering/ai110-module1show-gameglitchinvestigator-starter
collecting ... collected 15 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 20%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 26%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 33%]
tests/test_game_logic.py::test_check_guess_int_secret_is_consistent_across_attempts PASSED [ 40%]
tests/test_game_logic.py::test_check_guess_does_not_fall_back_to_string_comparison PASSED [ 46%]
tests/test_game_logic.py::test_parse_guess_rejects_out_of_range[0] PASSED [ 53%]
tests/test_game_logic.py::test_parse_guess_rejects_out_of_range[101] PASSED [ 60%]
tests/test_game_logic.py::test_parse_guess_rejects_out_of_range[105] PASSED [ 66%]
tests/test_game_logic.py::test_parse_guess_rejects_out_of_range[-5] PASSED [ 73%]
tests/test_game_logic.py::test_parse_guess_accepts_boundaries_and_inside[1-1] PASSED [ 80%]
tests/test_game_logic.py::test_parse_guess_accepts_boundaries_and_inside[100-100] PASSED [ 86%]
tests/test_game_logic.py::test_parse_guess_accepts_boundaries_and_inside[50-50] PASSED [ 93%]
tests/test_game_logic.py::test_parse_guess_uses_difficulty_range PASSED  [100%]

============================== 15 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
