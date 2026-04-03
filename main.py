"""
main.py — CLI entry point for Wooyoo.Studio v2.0.

Defines all typer command groups and routes each command to commands.py.
Contains NO business logic and NO direct data access.
"""

import typer
import commands

app = typer.Typer(
    name="wooyoo",
    help="Wooyoo.Studio v2.0 — 專為即時代購設計的交易管理工具。",
    no_args_is_help=True,
)

# ---------------------------------------------------------------------------
# Command groups
# ---------------------------------------------------------------------------

trip_app = typer.Typer(help="Manage proxy-shopping trips.")
booth_app = typer.Typer(help="Manage brand booths within a trip.")
item_app = typer.Typer(help="Manage items listed in a booth.")
order_app = typer.Typer(help="Manage buyer orders for an item.")

app.add_typer(trip_app, name="trip")
app.add_typer(booth_app, name="booth")
app.add_typer(item_app, name="item")
app.add_typer(order_app, name="order")


# ---------------------------------------------------------------------------
# trip commands
# ---------------------------------------------------------------------------

@trip_app.command("create")
def trip_create(
    name: str = typer.Option(..., "--name", help="Name of the trip (e.g., '首爾春季')"),
    dest: str = typer.Option(..., "--dest", help="Destination city or country"),
) -> None:
    """Create a new proxy-shopping trip."""
    commands.cmd_trip_create(name, dest)


@trip_app.command("list")
def trip_list() -> None:
    """List all proxy-shopping trips."""
    commands.cmd_trip_list()


# ---------------------------------------------------------------------------
# booth commands
# ---------------------------------------------------------------------------

@booth_app.command("add")
def booth_add(
    trip_id: int = typer.Option(..., "--trip-id", help="ID of the parent trip"),
    name: str = typer.Option(..., "--name", help="Brand booth name"),
    order: int = typer.Option(..., "--order", help="Visit order within the trip"),
    note: str = typer.Option("", "--note", help="Optional note for this booth"),
) -> None:
    """Add a brand booth to a trip."""
    commands.cmd_booth_add(trip_id, name, order, note)


@booth_app.command("list")
def booth_list(
    trip_id: int = typer.Option(..., "--trip-id", help="ID of the parent trip"),
) -> None:
    """List all booths for a trip."""
    commands.cmd_booth_list(trip_id)


# ---------------------------------------------------------------------------
# item commands
# ---------------------------------------------------------------------------

@item_app.command("add")
def item_add(
    booth_id: int = typer.Option(..., "--booth-id", help="ID of the parent booth"),
    name: str = typer.Option(..., "--name", help="Item name"),
    price: int = typer.Option(..., "--price", help="Price in NTD"),
    qty: int = typer.Option(..., "--qty", help="Total quantity available"),
    minutes: int = typer.Option(..., "--minutes", help="Minutes the item is open for ordering"),
) -> None:
    """Add an item to a booth."""
    commands.cmd_item_add(booth_id, name, price, qty, minutes)


@item_app.command("list")
def item_list(
    booth_id: int = typer.Option(..., "--booth-id", help="ID of the parent booth"),
) -> None:
    """List all items in a booth with their current status."""
    commands.cmd_item_list(booth_id)


@item_app.command("close")
def item_close(
    item_id: int = typer.Option(..., "--item-id", help="ID of the item to close"),
) -> None:
    """Manually close an item for new orders (OPEN → CLOSED)."""
    commands.cmd_item_close(item_id)


@item_app.command("fulfill")
def item_fulfill(
    item_id: int = typer.Option(..., "--item-id", help="ID of the item to mark as fulfilled"),
) -> None:
    """Mark an item as shipped/fulfilled (→ FULFILLED)."""
    commands.cmd_item_fulfill(item_id)


# ---------------------------------------------------------------------------
# order commands
# ---------------------------------------------------------------------------

@order_app.command("place")
def order_place(
    item_id: int = typer.Option(..., "--item-id", help="ID of the item to order"),
    buyer: str = typer.Option(..., "--buyer", help="Buyer's name"),
    phone: str = typer.Option(..., "--phone", help="Buyer's phone number"),
    qty: int = typer.Option(..., "--qty", help="Quantity to order"),
) -> None:
    """Place an order for an item."""
    commands.cmd_order_place(item_id, buyer, phone, qty)


@order_app.command("list")
def order_list(
    item_id: int = typer.Option(..., "--item-id", help="ID of the item"),
) -> None:
    """List all orders for an item."""
    commands.cmd_order_list(item_id)


@order_app.command("confirm")
def order_confirm(
    order_id: int = typer.Option(..., "--order-id", help="ID of the order to confirm"),
) -> None:
    """Confirm payment for an order (marks it as PAID)."""
    commands.cmd_order_confirm(order_id)


@order_app.command("cancel")
def order_cancel(
    order_id: int = typer.Option(..., "--order-id", help="ID of the order to cancel"),
) -> None:
    """Cancel an order and restore stock (→ CANCELLED)."""
    commands.cmd_order_cancel(order_id)


# ---------------------------------------------------------------------------
# v2.0 new commands
# ---------------------------------------------------------------------------

@trip_app.command("summary")
def trip_summary(
    trip_id: int = typer.Option(..., "--trip-id", help="ID of the trip to summarize"),
) -> None:
    """Show a revenue and order summary for a trip."""
    commands.cmd_trip_summary(trip_id)


@order_app.command("update")
def order_update(
    order_id: int = typer.Option(..., "--order-id", help="ID of the order to update"),
    qty: int = typer.Option(..., "--qty", help="New quantity"),
) -> None:
    """Update the quantity of a PENDING order."""
    commands.cmd_order_update(order_id, qty)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
