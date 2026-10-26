# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|------------|-------------------|-----------------|------------------------|-------------------------|
|Made a 2nd guess|The 2nd guess appears in the game history|The 2nd guess did not appear in the history| No error, logic bug| app.py lines 114-119 (history shown in debug expander before the submit block at 147-156 runs, so it lags one guess behind) |
| Made a 3rd guess of 95 |Guess 95 appears in the game history |95 was not recorded in the history |No error, logic bug | app.py lines 114-119 vs 156 (same stale-render cause as above) |
|Guessed 99, then guessed 100 (valid range is 1-100) | Both hints are consistent with the same secret number (99 and 100 can’t both be wrong in opposite directions) | 99 returned “go higher,” then 100 returned “go lower” |No error, logic bug | app.py lines 158-161 (secret converted to str on even attempts) and check_guess lines 41-47 (falls back to string comparison) |
| Guessed 105 (outside the 1-100 range)|An error or warning that the guess is out of range | No error message or feedback of any kind|No error, missing input validation | app.py parse_guess, lines 14-29 (no range check against low/high) |
| Secret number was 47; guessed several numbers higher than 47 | Hint says “Go lower” every time | Hint said “Go higher” | No error, logic bug (hint direction reversed) | app.py check_guess, lines 37-40 (HIGHER/LOWER messages swapped; also 45-47) |
| Clicked “New Game” button | A fresh game starts and the old history is cleared | No new game started, and the first game’s history stayed visible | No error, logic bug (likely game state not reset) | app.py lines 134-138 (only attempts and secret reset; history, score and status are not, so status "won"/"lost" triggers st.stop() at 140-145) |
| Used all 8 attempts for the game | Game ends and shows 0 attempts left | Display said I still had 8 attempts left | No error, logic bug | app.py lines 109-112 (attempts-left rendered before submit updates attempts), plus attempts starting at 1 (line 96) but reset to 0 (line 135) |
| Started with 8 attempts, history showed only 7 guesses | History shows 8 guesses and “out of attempts” appears after the 8th attempt | Told I ran out of attempts only after the game records 7 number guesses | No error, logic bug | app.py line 96 (attempts starts at 1) and line 182 (attempts >= attempt_limit ends game one guess early) |

**Related suspects not yet in the log (found while tracing the above)**

- `update_score` (50-65): the win bonus uses `attempt_number + 1` (extra penalty), and "Too High" gives +5 on even attempts but −5 on odd ones, so a wrong guess can raise the score.
- `get_range_for_difficulty` (4-11): Hard is 1-50, which is narrower (easier) than Normal's 1-100.
- `logic_utils.py`: every function is a `NotImplementedError` stub and `app.py` doesn't import it, so none of the fixes can be tested through `logic_utils` until the logic is moved there.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - **Correct suggestion:** For the stale "Attempts left" text and the lagging History, Claude suggested reserving the spots with `st.empty()` placeholders where the display used to be, then filling them from a `render_status()` function called after the submit block. That was correct because Streamlit runs the script top to bottom. The old code drew those values before the submit block updated `attempts` and `history`, so they were always one guess behind. Rendering after the state changes fixed the cause instead of working around it, and I also had it call `render_status()` before `st.stop()` so the display still appears once a game is won or lost. I ran and tested the game to make sure the tests checked out.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
  - **Suggestion that went beyond what I asked:** I asked Claude to move only `check_guess` into `logic_utils.py`. When I then asked for tests on the range bug, Claude also moved `parse_guess` (with new `low` and `high` arguments) so the range check could be tested, because importing `app.py` in a test would launch the Streamlit UI. That was out of scope for what I had asked, so I treated it as a change to review and not just accept. It told me what it had done so I could revert it. I kept it because the range-check tests could not exist without it, and I moved `get_range_for_difficulty` and `update_score` afterwards to match. I ran and tested the game to make sure the tests checked out.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I counted a bug as fixed only when it no longer reproduced the way I logged it in section 1 and a test covered it. For the bugs that live in the UI code, such as the stale history and attempts display and the New Game reset, I reran the same steps in the game and checked the result.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - I ran `pytest` on `tests/test_game_logic.py`. At first the three starter tests failed because they compared the whole `(outcome, message)` tuple from `check_guess` to a string. That showed me the tests were wrong, not the game, and I fixed them to unpack the tuple. The new regression tests check that a guess above the secret says "Go LOWER!", that `check_guess(100, 99)` always returns "Too High", and that `parse_guess` rejects 0, 101, 105 and -5 with the difficulty's range in the message. All 15 tests now pass, and I ran and tested the game to make sure the tests checked out.
- Did AI help you design or understand any tests? How?
  - Yes. Claude wrote the regression tests, and it explained that the existing ones failed because of the tuple return. It also pointed out that the attempts off-by-one, the New Game reset and the stale displays have no tests, because that logic lives in the Streamlit UI code. Testing it would mean pulling it out into functions. Claude also helped me understand my initial bugs in my code I needed to fix.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
