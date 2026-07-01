#!/usr/bin/env python3
"""
board.py — NicheVault Kanban Board Helper

Operations on ~/nichevault/board.json: add cards, move cards between
columns, inspect column contents, and print a board summary.

Usage:
    python3 board.py              # show_board()
    python3 board.py add <title>  # add_card(title)
    python3 board.py add <title> <column>  # add_card(title, column)
"""

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

BOARD_PATH = Path.home() / "nichevault" / "board.json"


def _load() -> dict:
    with open(BOARD_PATH, "r") as f:
        return json.load(f)


def _save(board: dict) -> None:
    with open(BOARD_PATH, "w") as f:
        json.dump(board, f, indent=2)


def add_card(title: str, column: str = "Ideas", meta: dict = None) -> dict:
    """Add a new card to *column* (defaults to Ideas).  Returns the new card."""
    board = _load()
    if column not in board["columns"]:
        valid = ", ".join(board["columns"])
        raise ValueError(f"Unknown column '{column}'. Valid: {valid}")

    card = {
        "id": uuid.uuid4().hex[:12],
        "title": title,
        "column": column,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "locked_by": None,
        "locked_at": None,
        "history": [],
        "moves": [],
        "meta": meta or {},
    }
    board["cards"].append(card)
    _save(board)
    return card


def move_card(card_id: str, to_column: str, agent: str = "hermes-agent") -> dict:
    """Move a card to *to_column*, logging the move with a timestamp and agent name."""
    board = _load()
    if to_column not in board["columns"]:
        valid = ", ".join(board["columns"])
        raise ValueError(f"Unknown column '{to_column}'. Valid: {valid}")

    for card in board["cards"]:
        if card["id"] == card_id:
            now = datetime.now(timezone.utc).isoformat()
            move_record = {
                "from": card["column"],
                "to": to_column,
                "at": now,
            }
            history_entry = {
                "timestamp": now,
                "action": "move",
                "from_column": card["column"],
                "to_column": to_column,
                "agent": agent,
            }
            card["moves"].append(move_record)
            card["history"].append(history_entry)
            card["column"] = to_column
            _save(board)
            return card

    raise ValueError(f"Card '{card_id}' not found.")


def lock_card(card_id: str, agent: str = "hermes-agent") -> dict:
    """Lock a card so only *agent* can act on it."""
    board = _load()
    for card in board["cards"]:
        if card["id"] == card_id:
            now = datetime.now(timezone.utc).isoformat()
            card["locked_by"] = agent
            card["locked_at"] = now
            card["history"].append({
                "timestamp": now,
                "action": "lock",
                "from_column": card["column"],
                "to_column": card["column"],
                "agent": agent,
            })
            _save(board)
            return card
    raise ValueError(f"Card '{card_id}' not found.")


def unlock_card(card_id: str, agent: str = "hermes-agent") -> dict:
    """Unlock a card."""
    board = _load()
    for card in board["cards"]:
        if card["id"] == card_id:
            now = datetime.now(timezone.utc).isoformat()
            card["locked_by"] = None
            card["locked_at"] = None
            card["history"].append({
                "timestamp": now,
                "action": "unlock",
                "from_column": card["column"],
                "to_column": card["column"],
                "agent": agent,
            })
            _save(board)
            return card
    raise ValueError(f"Card '{card_id}' not found.")


def get_column(column_name: str) -> list:
    """Return all cards currently in *column_name*."""
    board = _load()
    if column_name not in board["columns"]:
        valid = ", ".join(board["columns"])
        raise ValueError(f"Unknown column '{column_name}'. Valid: {valid}")
    return [c for c in board["cards"] if c["column"] == column_name]


def show_board() -> None:
    """Print a clean board summary: column name → card count."""
    board = _load()
    header = f"╔══ NicheVault Kanban ══╗"
    sep = "╟" + "─" * (len(header) - 2) + "╢"
    footer = "╚" + "═" * (len(header) - 2) + "╝"
    print(f"\n{header}")
    for col in board["columns"]:
        cards_in = [c for c in board["cards"] if c["column"] == col]
        count = len(cards_in)
        label = f"  {col}"
        print(f"║ {label:<31} {count:>2} card(s) ║")
        for c in cards_in:
            print(f"║   └─ {c['title']:<35} ║")
    print(f"{footer}")
    total = len(board["cards"])
    print(f"  Total cards: {total}\n")


# ── CLI wrapper ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        show_board()
    elif args[0] == "add":
        title = args[1] if len(args) > 1 else "Untitled card"
        column = args[2] if len(args) > 2 else "Ideas"
        card = add_card(title, column)
        print(f"Added card [{card['id']}] \"{card['title']}\" → {card['column']}")
    else:
        print(f"Usage: {sys.argv[0]} [add <title> [column]]")
        print(f"       {sys.argv[0]}            # show board")
        sys.exit(1)
