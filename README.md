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

You can also start a mode directly with `python main.py`, `python my_ai.py` or `python my_ai_attacker.py` (run them from the project folder so the images are found).

## How the AI works

**Defender AI** (`ai_move.py`)
Every 5-cell line on the board is a "window" where the attacker could still make five. A window containing only one colour is scored by how many stones it holds (0, 1, 10, 100, 1000); a window containing both colours can never become five and scores 0. The defender tries every empty cell with both colours, keeps the moves that lower the attacker's total score the most, then looks one attacker reply ahead and picks the safest move. It never completes a five itself unless every move would.

**Attacker AI** (`ai_attacker.py`)
Looks for 5-cell windows holding 4, then 3, 2, 1 stones of one colour and extends that line with the same colour; otherwise it plays next to an existing stone.

A full write-up of the original design is in `DOUBLE BALL GOMOKU.pdf` / `.docx`. (The defender AI has since been rewritten as described above.)

## Project structure

| File | Purpose |
|---|---|
| `start.py` | Menu window — launches the selected mode |
| `main.py` | 2-player mode |
| `my_ai.py` | Human attacker vs defender AI |
| `my_ai_attacker.py` | Attacker AI vs human defender |
| `game_arr.py` | Shared rules: click → board cell, five-in-a-row check, game result |
| `ai_move.py` | Defender AI |
| `ai_attacker.py` | Attacker AI |
| `football.png`, `black.png` | Stone images |
| `requirements.txt` | Python dependencies |
