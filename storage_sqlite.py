"""
storage_sqlite.py — SQLite-backed data models and all database read/write operations.

Drop-in replacement for storage.py. Exposes the same public interface so that
commands.py requires only a single import change to switch backends.

Database file: v2/wooyoo.db
Schema is created automatically on first run.
"""

from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "wooyoo.db")


# ---------------------------------------------------------------------------
# Enums (identical to storage.py)
# ---------------------------------------------------------------------------

class ItemStatus(str, Enum):
    OPEN = "OPEN"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"
    FULFILLED = "FULFILLED"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


# ---------------------------------------------------------------------------
# Dataclasses (identical to storage.py, with note added to Booth)
# ---------------------------------------------------------------------------

@dataclass
class Trip:
    id: int
    name: str
    destination: str
    created_at: str
    metadata: dict = field(default_factory=dict)


@dataclass
class Booth:
    id: int
    trip_id: int
    name: str
    visit_order: int
    created_at: str
    note: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class Item:
    id: int
    booth_id: int
    name: str
    price: int
    quantity: int
    remaining: int
    minutes: int
    deadline: str
    created_at: str
    metadata: dict = field(default_factory=dict)

    def get_status(self) -> ItemStatus:
        """Dynamically compute item status at runtime — never stored in DB."""
        if self.metadata.get("fulfilled"):
            return ItemStatus.FULFILLED
        if self.metadata.get("force_closed"):
            return ItemStatus.CLOSED
        if datetime.fromisoformat(self.deadline) < datetime.now():
            return ItemStatus.EXPIRED
        return ItemStatus.OPEN


@dataclass
class Order:
    id: int
    item_id: int
    buyer_name: str
    buyer_phone: str
    quantity: int
    status: str
    created_at: str
    metadata: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _init_db() -> None:
    """Create tables if they don't exist."""
    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS trips (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                destination TEXT    NOT NULL,
                created_at  TEXT    NOT NULL,
                metadata    TEXT    NOT NULL DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS booths (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id     INTEGER NOT NULL REFERENCES trips(id),
                name        TEXT    NOT NULL,
                visit_order INTEGER NOT NULL,
                created_at  TEXT    NOT NULL,
                note        TEXT    NOT NULL DEFAULT '',
                metadata    TEXT    NOT NULL DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS items (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                booth_id    INTEGER NOT NULL REFERENCES booths(id),
                name        TEXT    NOT NULL,
                price       INTEGER NOT NULL,
                quantity    INTEGER NOT NULL,
                remaining   INTEGER NOT NULL,
                minutes     INTEGER NOT NULL,
                deadline    TEXT    NOT NULL,
                created_at  TEXT    NOT NULL,
                metadata    TEXT    NOT NULL DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS orders (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id     INTEGER NOT NULL REFERENCES items(id),
                buyer_name  TEXT    NOT NULL,
                buyer_phone TEXT    NOT NULL,
                quantity    INTEGER NOT NULL,
                status      TEXT    NOT NULL,
                created_at  TEXT    NOT NULL,
                metadata    TEXT    NOT NULL DEFAULT '{}'
            );
        """)


# Initialize DB on module import
_init_db()


import json as _json

def _row_to_trip(row: sqlite3.Row) -> Trip:
    return Trip(
        id=row["id"],
        name=row["name"],
        destination=row["destination"],
        created_at=row["created_at"],
        metadata=_json.loads(row["metadata"]),
    )


def _row_to_booth(row: sqlite3.Row) -> Booth:
    return Booth(
        id=row["id"],
        trip_id=row["trip_id"],
        name=row["name"],
        visit_order=row["visit_order"],
        created_at=row["created_at"],
        note=row["note"],
        metadata=_json.loads(row["metadata"]),
    )


def _row_to_item(row: sqlite3.Row) -> Item:
    return Item(
        id=row["id"],
        booth_id=row["booth_id"],
        name=row["name"],
        price=row["price"],
        quantity=row["quantity"],
        remaining=row["remaining"],
        minutes=row["minutes"],
        deadline=row["deadline"],
        created_at=row["created_at"],
        metadata=_json.loads(row["metadata"]),
    )


def _row_to_order(row: sqlite3.Row) -> Order:
    return Order(
        id=row["id"],
        item_id=row["item_id"],
        buyer_name=row["buyer_name"],
        buyer_phone=row["buyer_phone"],
        quantity=row["quantity"],
        status=row["status"],
        created_at=row["created_at"],
        metadata=_json.loads(row["metadata"]),
    )


# ---------------------------------------------------------------------------
# Trip CRUD
# ---------------------------------------------------------------------------

def create_trip(name: str, destination: str) -> Trip:
    """Insert a new Trip and return the created object."""
    now = datetime.now().isoformat()
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO trips (name, destination, created_at, metadata) VALUES (?, ?, ?, ?)",
            (name, destination, now, "{}"),
        )
        return Trip(id=cur.lastrowid, name=name, destination=destination, created_at=now)


def list_trips() -> list[Trip]:
    """Return all trips ordered by id."""
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM trips ORDER BY id").fetchall()
    return [_row_to_trip(r) for r in rows]


def get_trip(trip_id: int) -> Optional[Trip]:
    """Return a Trip by id, or None if not found."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM trips WHERE id = ?", (trip_id,)).fetchone()
    return _row_to_trip(row) if row else None


# ---------------------------------------------------------------------------
# Booth CRUD
# ---------------------------------------------------------------------------

def add_booth(trip_id: int, name: str, visit_order: int, note: str = "") -> Booth:
    """Insert a new Booth and return the created object."""
    now = datetime.now().isoformat()
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO booths (trip_id, name, visit_order, created_at, note, metadata) VALUES (?, ?, ?, ?, ?, ?)",
            (trip_id, name, visit_order, now, note, "{}"),
        )
        return Booth(id=cur.lastrowid, trip_id=trip_id, name=name, visit_order=visit_order, created_at=now, note=note)


def list_booths(trip_id: int) -> list[Booth]:
    """Return all booths for a given trip, sorted by visit_order."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM booths WHERE trip_id = ? ORDER BY visit_order", (trip_id,)
        ).fetchall()
    return [_row_to_booth(r) for r in rows]


def get_booth(booth_id: int) -> Optional[Booth]:
    """Return a Booth by id, or None if not found."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM booths WHERE id = ?", (booth_id,)).fetchone()
    return _row_to_booth(row) if row else None


# ---------------------------------------------------------------------------
# Item CRUD
# ---------------------------------------------------------------------------

def add_item(booth_id: int, name: str, price: int, quantity: int, minutes: int) -> Item:
    """Insert a new Item and return the created object."""
    now = datetime.now()
    deadline = now + timedelta(minutes=minutes)
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO items
               (booth_id, name, price, quantity, remaining, minutes, deadline, created_at, metadata)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (booth_id, name, price, quantity, quantity, minutes,
             deadline.isoformat(), now.isoformat(), "{}"),
        )
        return Item(
            id=cur.lastrowid, booth_id=booth_id, name=name, price=price,
            quantity=quantity, remaining=quantity, minutes=minutes,
            deadline=deadline.isoformat(), created_at=now.isoformat(),
        )


def list_items(booth_id: int) -> list[Item]:
    """Return all items for a given booth, sorted by id."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM items WHERE booth_id = ? ORDER BY id", (booth_id,)
        ).fetchall()
    return [_row_to_item(r) for r in rows]


def get_item(item_id: int) -> Optional[Item]:
    """Return an Item by id, or None if not found."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    return _row_to_item(row) if row else None


def update_item_remaining(item_id: int, delta: int) -> None:
    """Adjust remaining stock of an item by delta (negative to decrease)."""
    with _connect() as conn:
        result = conn.execute(
            "UPDATE items SET remaining = remaining + ? WHERE id = ?", (delta, item_id)
        )
        if result.rowcount == 0:
            raise ValueError(f"Item ID {item_id} not found")


def close_item(item_id: int) -> Item:
    """Set force_closed flag on an item, transitioning it to CLOSED status."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if row is None:
            raise ValueError(f"Item ID {item_id} not found")
        metadata = _json.loads(row["metadata"])
        metadata["force_closed"] = True
        conn.execute(
            "UPDATE items SET metadata = ? WHERE id = ?",
            (_json.dumps(metadata), item_id),
        )
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    return _row_to_item(row)


def fulfill_item(item_id: int) -> Item:
    """Set fulfilled flag on an item, transitioning it to FULFILLED status."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if row is None:
            raise ValueError(f"Item ID {item_id} not found")
        metadata = _json.loads(row["metadata"])
        metadata["fulfilled"] = True
        conn.execute(
            "UPDATE items SET metadata = ? WHERE id = ?",
            (_json.dumps(metadata), item_id),
        )
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    return _row_to_item(row)


# ---------------------------------------------------------------------------
# Order CRUD
# ---------------------------------------------------------------------------

def place_order(item_id: int, buyer_name: str, buyer_phone: str, quantity: int) -> Order:
    """Insert a new Order and return the created object."""
    now = datetime.now().isoformat()
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO orders (item_id, buyer_name, buyer_phone, quantity, status, created_at, metadata)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (item_id, buyer_name, buyer_phone, quantity, OrderStatus.PENDING.value, now, "{}"),
        )
        return Order(
            id=cur.lastrowid, item_id=item_id, buyer_name=buyer_name,
            buyer_phone=buyer_phone, quantity=quantity,
            status=OrderStatus.PENDING.value, created_at=now,
        )


def list_orders(item_id: int) -> list[Order]:
    """Return all orders for a given item, sorted by id."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM orders WHERE item_id = ? ORDER BY id", (item_id,)
        ).fetchall()
    return [_row_to_order(r) for r in rows]


def get_order(order_id: int) -> Optional[Order]:
    """Return an Order by id, or None if not found."""
    with _connect() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return _row_to_order(row) if row else None


def confirm_order(order_id: int) -> Order:
    """Mark an order as PAID and return the updated object."""
    with _connect() as conn:
        result = conn.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (OrderStatus.PAID.value, order_id),
        )
        if result.rowcount == 0:
            raise ValueError(f"Order ID {order_id} not found")
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return _row_to_order(row)


def cancel_order(order_id: int) -> Order:
    """Mark an order as CANCELLED and return the updated object."""
    with _connect() as conn:
        result = conn.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (OrderStatus.CANCELLED.value, order_id),
        )
        if result.rowcount == 0:
            raise ValueError(f"Order ID {order_id} not found")
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return _row_to_order(row)


def update_order_quantity(order_id: int, new_qty: int) -> Order:
    """Update the quantity of a PENDING order and return the updated object."""
    with _connect() as conn:
        result = conn.execute(
            "UPDATE orders SET quantity = ? WHERE id = ?",
            (new_qty, order_id),
        )
        if result.rowcount == 0:
            raise ValueError(f"Order ID {order_id} not found")
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return _row_to_order(row)


# ---------------------------------------------------------------------------
# Trip summary (v2.0 new — cross-layer aggregation)
# ---------------------------------------------------------------------------

def get_trip_summary(trip_id: int) -> dict:
    """
    Return a summary dict for a trip, aggregating across all booths, items, and orders.

    Structure:
    {
        "trip": Trip,
        "booths": [
            {
                "booth": Booth,
                "items": [
                    {"item": Item, "status": ItemStatus}
                ]
            }
        ],
        "paid_total": int,       # sum of price * quantity for PAID orders
        "paid_count": int,
        "pending_count": int,
    }
    """
    with _connect() as conn:
        trip_row = conn.execute("SELECT * FROM trips WHERE id = ?", (trip_id,)).fetchone()
        if trip_row is None:
            return {}

        booth_rows = conn.execute(
            "SELECT * FROM booths WHERE trip_id = ? ORDER BY visit_order", (trip_id,)
        ).fetchall()

        booths_data = []
        paid_total = 0
        paid_count = 0
        pending_count = 0

        for b_row in booth_rows:
            booth = _row_to_booth(b_row)
            item_rows = conn.execute(
                "SELECT * FROM items WHERE booth_id = ? ORDER BY id", (booth.id,)
            ).fetchall()

            items_data = []
            for i_row in item_rows:
                item = _row_to_item(i_row)
                status = item.get_status()
                items_data.append({"item": item, "status": status})

                order_rows = conn.execute(
                    "SELECT * FROM orders WHERE item_id = ?", (item.id,)
                ).fetchall()
                for o_row in order_rows:
                    order = _row_to_order(o_row)
                    if order.status == OrderStatus.PAID.value:
                        paid_total += item.price * order.quantity
                        paid_count += 1
                    elif order.status == OrderStatus.PENDING.value:
                        pending_count += 1

            booths_data.append({"booth": booth, "items": items_data})

    return {
        "trip": _row_to_trip(trip_row),
        "booths": booths_data,
        "paid_total": paid_total,
        "paid_count": paid_count,
        "pending_count": pending_count,
    }
