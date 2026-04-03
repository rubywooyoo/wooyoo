"""
storage.py — Data models (dataclass + Enum) and all JSON read/write operations.

This is the ONLY module that directly reads or writes data.json.
Replacing this module is sufficient to migrate to a different storage backend (e.g., SQLite).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


# ---------------------------------------------------------------------------
# Enums
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
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Trip:
    id: int
    name: str
    destination: str
    created_at: str
    metadata: dict = field(default_factory=dict)  # reserved for v2.0


@dataclass
class Booth:
    id: int
    trip_id: int
    name: str
    visit_order: int
    created_at: str
    metadata: dict = field(default_factory=dict)  # reserved for v2.0


@dataclass
class Item:
    id: int
    booth_id: int
    name: str
    price: int
    quantity: int
    remaining: int
    minutes: int
    deadline: str        # ISO format string; computed as created_at + minutes
    created_at: str
    metadata: dict = field(default_factory=dict)  # reserved for v2.0

    def get_status(self) -> ItemStatus:
        """Dynamically compute item status at runtime — never stored in JSON."""
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
    status: str          # OrderStatus value
    created_at: str
    metadata: dict = field(default_factory=dict)  # reserved for v2.0


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _empty_db() -> dict:
    return {"trips": [], "booths": [], "items": [], "orders": []}


def _load() -> dict:
    if not os.path.exists(DATA_FILE):
        return _empty_db()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(db: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def _next_id(records: list) -> int:
    if not records:
        return 1
    return max(r["id"] for r in records) + 1


# ---------------------------------------------------------------------------
# Trip CRUD
# ---------------------------------------------------------------------------

def create_trip(name: str, destination: str) -> Trip:
    """Insert a new Trip and return the created object."""
    db = _load()
    trip_id = _next_id(db["trips"])
    now = datetime.now().isoformat()
    record = {
        "id": trip_id,
        "name": name,
        "destination": destination,
        "created_at": now,
        "metadata": {},
    }
    db["trips"].append(record)
    _save(db)
    return Trip(**record)


def list_trips() -> list[Trip]:
    """Return all trips ordered by id."""
    db = _load()
    return [Trip(**r) for r in db["trips"]]


def get_trip(trip_id: int) -> Optional[Trip]:
    """Return a Trip by id, or None if not found."""
    db = _load()
    for r in db["trips"]:
        if r["id"] == trip_id:
            return Trip(**r)
    return None


# ---------------------------------------------------------------------------
# Booth CRUD
# ---------------------------------------------------------------------------

def add_booth(trip_id: int, name: str, visit_order: int) -> Booth:
    """Insert a new Booth and return the created object."""
    db = _load()
    booth_id = _next_id(db["booths"])
    now = datetime.now().isoformat()
    record = {
        "id": booth_id,
        "trip_id": trip_id,
        "name": name,
        "visit_order": visit_order,
        "created_at": now,
        "metadata": {},
    }
    db["booths"].append(record)
    _save(db)
    return Booth(**record)


def list_booths(trip_id: int) -> list[Booth]:
    """Return all booths for a given trip, sorted by visit_order."""
    db = _load()
    booths = [Booth(**r) for r in db["booths"] if r["trip_id"] == trip_id]
    return sorted(booths, key=lambda b: b.visit_order)


def get_booth(booth_id: int) -> Optional[Booth]:
    """Return a Booth by id, or None if not found."""
    db = _load()
    for r in db["booths"]:
        if r["id"] == booth_id:
            return Booth(**r)
    return None


# ---------------------------------------------------------------------------
# Item CRUD
# ---------------------------------------------------------------------------

def add_item(booth_id: int, name: str, price: int, quantity: int, minutes: int) -> Item:
    """Insert a new Item and return the created object."""
    db = _load()
    item_id = _next_id(db["items"])
    now = datetime.now()
    deadline = now + timedelta(minutes=minutes)
    record = {
        "id": item_id,
        "booth_id": booth_id,
        "name": name,
        "price": price,
        "quantity": quantity,
        "remaining": quantity,
        "minutes": minutes,
        "deadline": deadline.isoformat(),
        "created_at": now.isoformat(),
        "metadata": {},
    }
    db["items"].append(record)
    _save(db)
    return Item(**record)


def list_items(booth_id: int) -> list[Item]:
    """Return all items for a given booth, sorted by id."""
    db = _load()
    return [Item(**r) for r in db["items"] if r["booth_id"] == booth_id]


def get_item(item_id: int) -> Optional[Item]:
    """Return an Item by id, or None if not found."""
    db = _load()
    for r in db["items"]:
        if r["id"] == item_id:
            return Item(**r)
    return None


def update_item_remaining(item_id: int, delta: int) -> None:
    """Adjust remaining stock of an item by delta (negative to decrease)."""
    db = _load()
    for r in db["items"]:
        if r["id"] == item_id:
            r["remaining"] += delta
            _save(db)
            return
    raise ValueError(f"Item ID {item_id} not found")


def close_item(item_id: int) -> Item:
    """Set force_closed flag on an item, transitioning it to CLOSED status."""
    db = _load()
    for r in db["items"]:
        if r["id"] == item_id:
            r["metadata"]["force_closed"] = True
            _save(db)
            return Item(**r)
    raise ValueError(f"Item ID {item_id} not found")


def fulfill_item(item_id: int) -> Item:
    """Set fulfilled flag on an item, transitioning it to FULFILLED status."""
    db = _load()
    for r in db["items"]:
        if r["id"] == item_id:
            r["metadata"]["fulfilled"] = True
            _save(db)
            return Item(**r)
    raise ValueError(f"Item ID {item_id} not found")


# ---------------------------------------------------------------------------
# Order CRUD
# ---------------------------------------------------------------------------

def place_order(item_id: int, buyer_name: str, buyer_phone: str, quantity: int) -> Order:
    """Insert a new Order and return the created object."""
    db = _load()
    order_id = _next_id(db["orders"])
    now = datetime.now().isoformat()
    record = {
        "id": order_id,
        "item_id": item_id,
        "buyer_name": buyer_name,
        "buyer_phone": buyer_phone,
        "quantity": quantity,
        "status": OrderStatus.PENDING.value,
        "created_at": now,
        "metadata": {},
    }
    db["orders"].append(record)
    _save(db)
    return Order(**record)


def list_orders(item_id: int) -> list[Order]:
    """Return all orders for a given item, sorted by id."""
    db = _load()
    return [Order(**r) for r in db["orders"] if r["item_id"] == item_id]


def get_order(order_id: int) -> Optional[Order]:
    """Return an Order by id, or None if not found."""
    db = _load()
    for r in db["orders"]:
        if r["id"] == order_id:
            return Order(**r)
    return None


def confirm_order(order_id: int) -> Order:
    """Mark an order as PAID and return the updated object."""
    db = _load()
    for r in db["orders"]:
        if r["id"] == order_id:
            r["status"] = OrderStatus.PAID.value
            _save(db)
            return Order(**r)
    raise ValueError(f"Order ID {order_id} not found")


def cancel_order(order_id: int) -> Order:
    """Mark an order as CANCELLED and return the updated object."""
    db = _load()
    for r in db["orders"]:
        if r["id"] == order_id:
            r["status"] = OrderStatus.CANCELLED.value
            _save(db)
            return Order(**r)
    raise ValueError(f"Order ID {order_id} not found")
