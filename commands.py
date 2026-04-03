"""
commands.py — Business logic validation and formatted output.

All user-facing messages are printed here.
v2.0 switches storage backend to SQLite via storage_sqlite (drop-in replacement).
"""

import sys
import storage_sqlite as storage


# ---------------------------------------------------------------------------
# Trip commands
# ---------------------------------------------------------------------------

def cmd_trip_create(name: str, destination: str) -> None:
    """Create a new proxy-shopping trip and print confirmation."""
    trip = storage.create_trip(name, destination)
    print(f"Created trip [{trip.id}]: {trip.name} → {trip.destination}")


def cmd_trip_list() -> None:
    """Print all trips."""
    trips = storage.list_trips()
    if not trips:
        print("No trips found.")
        return
    print(f"{'ID':<5} {'Name':<20} {'Destination':<15} {'Created At'}")
    print("-" * 60)
    for t in trips:
        print(f"{t.id:<5} {t.name:<20} {t.destination:<15} {t.created_at}")


# ---------------------------------------------------------------------------
# Booth commands
# ---------------------------------------------------------------------------

def cmd_booth_add(trip_id: int, name: str, visit_order: int, note: str = "") -> None:
    """Validate trip existence, add a booth with optional note, and print confirmation."""
    trip = storage.get_trip(trip_id)
    if trip is None:
        print(f"Error: Trip ID {trip_id} not found")
        sys.exit(1)

    booth = storage.add_booth(trip_id, name, visit_order, note)
    print(f"Added booth [{booth.id}]: {booth.name} (order={booth.visit_order}) to trip '{trip.name}'")


def cmd_booth_list(trip_id: int) -> None:
    """Print all booths for a trip."""
    trip = storage.get_trip(trip_id)
    if trip is None:
        print(f"Error: Trip ID {trip_id} not found")
        sys.exit(1)

    booths = storage.list_booths(trip_id)
    if not booths:
        print(f"No booths found for trip '{trip.name}'.")
        return
    print(f"Booths for trip '{trip.name}':")
    print(f"{'ID':<5} {'Name':<25} {'Order':<8} {'Note':<20} {'Created At'}")
    print("-" * 75)
    for b in booths:
        note_str = b.note if b.note else "-"
        print(f"{b.id:<5} {b.name:<25} {b.visit_order:<8} {note_str:<20} {b.created_at}")


# ---------------------------------------------------------------------------
# Item commands
# ---------------------------------------------------------------------------

def cmd_item_add(booth_id: int, name: str, price: int, qty: int, minutes: int) -> None:
    """Validate booth existence, add an item, and print confirmation."""
    booth = storage.get_booth(booth_id)
    if booth is None:
        print(f"Error: Booth ID {booth_id} not found")
        sys.exit(1)

    item = storage.add_item(booth_id, name, price, qty, minutes)
    print(
        f"Added item [{item.id}]: {item.name} | "
        f"Price: {item.price} | Qty: {item.quantity} | "
        f"Open for: {item.minutes} min | Deadline: {item.deadline}"
    )


def cmd_item_list(booth_id: int) -> None:
    """Print all items for a booth including their dynamic status."""
    booth = storage.get_booth(booth_id)
    if booth is None:
        print(f"Error: Booth ID {booth_id} not found")
        sys.exit(1)

    items = storage.list_items(booth_id)
    if not items:
        print(f"No items found for booth '{booth.name}'.")
        return
    print(f"Items for booth '{booth.name}':")
    print(f"{'ID':<5} {'Name':<20} {'Price':>7} {'Qty':>5} {'Left':>5} {'Status':<12} {'Deadline'}")
    print("-" * 80)
    for it in items:
        status = it.get_status().value
        print(
            f"{it.id:<5} {it.name:<20} {it.price:>7} {it.quantity:>5} "
            f"{it.remaining:>5} {status:<12} {it.deadline}"
        )


# ---------------------------------------------------------------------------
# Order commands
# ---------------------------------------------------------------------------

def cmd_order_place(item_id: int, buyer_name: str, buyer_phone: str, qty: int) -> None:
    """Validate item availability, place an order, and print confirmation."""
    item = storage.get_item(item_id)
    if item is None:
        print(f"Error: Item ID {item_id} not found")
        sys.exit(1)

    status = item.get_status()
    if status != storage.ItemStatus.OPEN:
        print(f"Error: Item is not open for orders (status: {status.value})")
        sys.exit(1)

    if qty > item.remaining:
        print(f"Error: Not enough stock. Available: {item.remaining}")
        sys.exit(1)

    order = storage.place_order(item_id, buyer_name, buyer_phone, qty)
    storage.update_item_remaining(item_id, -qty)
    print(
        f"Order placed [{order.id}]: {buyer_name} ordered {qty}x '{item.name}' | "
        f"Status: {order.status} | Phone: {order.buyer_phone}"
    )


def cmd_order_list(item_id: int) -> None:
    """Print all orders for an item."""
    item = storage.get_item(item_id)
    if item is None:
        print(f"Error: Item ID {item_id} not found")
        sys.exit(1)

    orders = storage.list_orders(item_id)
    if not orders:
        print(f"No orders found for item '{item.name}'.")
        return
    print(f"Orders for item '{item.name}':")
    print(f"{'ID':<5} {'Buyer':<15} {'Phone':<15} {'Qty':>5} {'Status':<12} {'Created At'}")
    print("-" * 70)
    for o in orders:
        print(
            f"{o.id:<5} {o.buyer_name:<15} {o.buyer_phone:<15} "
            f"{o.quantity:>5} {o.status:<12} {o.created_at}"
        )


def cmd_order_confirm(order_id: int) -> None:
    """Mark an order as PAID and print confirmation."""
    order = storage.get_order(order_id)
    if order is None:
        print(f"Error: Order ID {order_id} not found")
        sys.exit(1)

    if order.status == storage.OrderStatus.PAID.value:
        print(f"Error: Order ID {order_id} is already confirmed (PAID)")
        sys.exit(1)

    if order.status == storage.OrderStatus.CANCELLED.value:
        print(f"Error: Order ID {order_id} is already cancelled")
        sys.exit(1)

    updated = storage.confirm_order(order_id)
    print(f"Confirmed order [{updated.id}]: {updated.buyer_name} | Status: {updated.status} (PAID)")


def cmd_order_cancel(order_id: int) -> None:
    """Cancel an order and print confirmation."""
    order = storage.get_order(order_id)
    if order is None:
        print(f"Error: Order ID {order_id} not found")
        sys.exit(1)

    if order.status == storage.OrderStatus.CANCELLED.value:
        print(f"Error: Order ID {order_id} is already cancelled")
        sys.exit(1)

    updated = storage.cancel_order(order_id)
    storage.update_item_remaining(updated.item_id, updated.quantity)
    print(f"Cancelled order [{updated.id}]: {updated.buyer_name} | Status: {updated.status} | Stock restored: +{updated.quantity}")


# ---------------------------------------------------------------------------
# Item state transition commands
# ---------------------------------------------------------------------------

def cmd_item_close(item_id: int) -> None:
    """Manually close an item for new orders (OPEN → CLOSED)."""
    item = storage.get_item(item_id)
    if item is None:
        print(f"Error: Item ID {item_id} not found")
        sys.exit(1)

    if item.get_status() == storage.ItemStatus.FULFILLED:
        print(f"Error: Item ID {item_id} is already fulfilled")
        sys.exit(1)

    if item.get_status() == storage.ItemStatus.CLOSED:
        print(f"Error: Item ID {item_id} is already closed")
        sys.exit(1)

    updated = storage.close_item(item_id)
    print(f"Closed item [{updated.id}]: '{updated.name}' | Status: {updated.get_status().value}")


def cmd_item_fulfill(item_id: int) -> None:
    """Mark an item as fulfilled (shipped). Transitions to FULFILLED."""
    item = storage.get_item(item_id)
    if item is None:
        print(f"Error: Item ID {item_id} not found")
        sys.exit(1)

    if item.get_status() == storage.ItemStatus.FULFILLED:
        print(f"Error: Item ID {item_id} is already fulfilled")
        sys.exit(1)

    updated = storage.fulfill_item(item_id)
    print(f"Fulfilled item [{updated.id}]: '{updated.name}' | Status: {updated.get_status().value}")


# ---------------------------------------------------------------------------
# v2.0 new commands
# ---------------------------------------------------------------------------

def cmd_order_update(order_id: int, new_qty: int) -> None:
    """Update the quantity of a PENDING order and adjust stock accordingly."""
    order = storage.get_order(order_id)
    if order is None:
        print(f"Error: Order ID {order_id} not found")
        sys.exit(1)

    if order.status == storage.OrderStatus.PAID.value:
        print(f"Error: Order ID {order_id} is already paid and cannot be modified")
        sys.exit(1)

    if order.status == storage.OrderStatus.CANCELLED.value:
        print(f"Error: Order ID {order_id} is already cancelled and cannot be modified")
        sys.exit(1)

    item = storage.get_item(order.item_id)
    delta = new_qty - order.quantity
    if delta > 0 and delta > item.remaining:
        print(f"Error: Not enough stock. Available: {item.remaining}")
        sys.exit(1)

    storage.update_order_quantity(order_id, new_qty)
    storage.update_item_remaining(order.item_id, -delta)
    print(f"Updated order [{order_id}]: {order.buyer_name} | Qty: {order.quantity} → {new_qty}")


def cmd_trip_summary(trip_id: int) -> None:
    """Print a cross-layer summary of a trip including revenue and pending orders."""
    summary = storage.get_trip_summary(trip_id)
    if not summary:
        print(f"Error: Trip ID {trip_id} not found")
        sys.exit(1)

    trip = summary["trip"]
    print(f"Trip Summary: [{trip.id}] {trip.name} → {trip.destination}")
    print("=" * 60)

    if not summary["booths"]:
        print("No booths found for this trip.")
    else:
        for b_data in summary["booths"]:
            booth = b_data["booth"]
            note_str = f" | Note: {booth.note}" if booth.note else ""
            print(f"\nBooth [{booth.id}]: {booth.name}{note_str}")
            print(f"  {'Item':<20} {'Status':<12} {'Price':>7} {'Left':>5}")
            print(f"  {'-' * 50}")
            if not b_data["items"]:
                print("  No items.")
            for i_data in b_data["items"]:
                item = i_data["item"]
                status = i_data["status"].value
                print(f"  {item.name:<20} {status:<12} {item.price:>7} {item.remaining:>5}")

    print("\n" + "=" * 60)
    if summary["paid_count"] == 0 and summary["pending_count"] == 0:
        print("No orders found for this trip.")
    else:
        print(f"PAID   : {summary['paid_count']} order(s) | Total: NT${summary['paid_total']}")
        print(f"PENDING: {summary['pending_count']} order(s) awaiting payment confirmation")


