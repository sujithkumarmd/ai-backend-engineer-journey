DEVELOPER_TOKENS = 30   # the developer message, sent on every turn
USER_TOKENS = 20        # a typical user message
REPLY_TOKENS = 60       # a typical assistant reply
TURNS = 10

with_history_total = 0
without_history_total = 0

print("turn | input tokens WITH history | input tokens WITHOUT history")
for turn in range(1, TURNS + 1):
    previous_turns = turn - 1
    with_history = DEVELOPER_TOKENS + previous_turns * (USER_TOKENS + REPLY_TOKENS) + USER_TOKENS
    without_history = DEVELOPER_TOKENS + USER_TOKENS

    with_history_total += with_history
    without_history_total += without_history
    print(f"{turn:>4} | {with_history:>25} | {without_history:>28}")

print(f"\nTotal input tokens over {TURNS} turns: {with_history_total} with history, "
      f"{without_history_total} without ({with_history_total / without_history_total:.1f}× more)")
