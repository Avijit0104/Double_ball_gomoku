# Double Ball Gomoku

A two-role twist on Gomoku (five in a row), built with **Python**, **Pygame** and **NumPy**.

On a 15×15 board, stones don't belong to a player — **on every turn you may place either colour**:

| Mouse | Stone |
|---|---|
| Left click | White (football) |
| Right click | Black |

One side is the **Attacker**, the other the **Defender**:

- **Attacker wins** as soon as **any five identical stones** line up — horizontally, vertically or diagonally, in either colour, no matter who placed the last stone.
- **Defender wins** if the board fills up without a five.

The attacker always moves first. Because the defender's stones can also be used by the attacker, blocking is a careful choice: blocking a black line with a white stone also builds white lines.

## Game modes

Run the menu and pick a mode:

| Button | You play | Opponent |
|---|---|---|
| **Vs AI (defender)** | Attacker | Defender AI |
| **Vs AI (attacker)** | Defender | Attacker AI |
| **2 player** | P1 = Attacker, P2 = Defender | each other, same computer |

## Getting started

Requires Python 3 (tested on Python 3.14 on Windows).

```bash
git clone https://github.com/Avijit0104/Double_ball_gomoku.git
cd Double_ball_gomoku

python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Windows (cmd):         .venv\Scripts\activate
# macOS / Linux:         source .venv/bin/activate

pip install -r requirements.txt
python start.py
```

> **Why `pygame-ce`?** `requirements.txt` uses [pygame-ce](https://pyga.me/), the community edition of Pygame. It is a drop-in replacement (the code still does `import pygame`) and, unlike classic `pygame`, provides wheels for Python 3.14.

You can also start a mode directly with `python main.py`, `python my_ai.py` or `python my_ai_attacker.py`.

## How the AI works

Both AIs share one way of judging a position (`ai_eval.py`). Every 5-cell line on the board is a "window" where a five could still appear. A window containing stones of only one colour is scored by how many it holds (0, 1, 10, 100, 1000); a window containing both colours can never become five and scores 0. The total over all windows is the board's **danger** — the attacker wants it high, the defender wants it low.

**Defender AI** (`ai_move.py`)
Tries every empty cell with both colours, keeps the moves that lower the danger the most, then looks one attacker reply ahead and picks the safest one. It never completes a five itself unless every move would.

**Attacker AI** (`ai_attacker.py`)
Opens in the centre and completes a five whenever it can. Otherwise it tries every empty cell with both colours, keeps the moves that raise the danger the most, then looks one defender reply ahead — a move that leaves a five the defender can't stop (for example two threats at once) is preferred.

> **Balance note:** the attacker never has to defend, can build in either colour and can reuse the defender's stones, so a strong attacker is very hard to stop. In testing, the attacker AI beats the defender AI in about 18 moves; as a human defender, expect a tough game.

The original design write-up is in `DOUBLE BALL GOMOKU.pdf` / `.docx`; both AIs have since been rewritten as described above.

## Project structure

| File | Purpose |
|---|---|
| `start.py` | Menu window — pick a mode and play it in the same window |
| `main.py` | Starts 2-player mode directly |
| `my_ai.py` | Starts "you attack, defender AI" directly |
| `my_ai_attacker.py` | Starts "attacker AI, you defend" directly |
| `game_ui.py` | Game window shared by all modes: drawing, mouse input, turns, AI players |
| `game_arr.py` | Rules: click → board cell, five-in-a-row check, game result |
| `ai_eval.py` | Position scoring shared by both AIs |
| `ai_move.py` | Defender AI |
| `ai_attacker.py` | Attacker AI |
| `football.png`, `black.png` | Stone images |
| `requirements.txt` | Python dependencies |
