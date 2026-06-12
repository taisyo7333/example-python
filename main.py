from dataclasses import dataclass


@dataclass(frozen=True)
class Sale:
    item: str
    category: str
    price: int
    quantity: int


def subtotal(sale: Sale) -> int:
    return sale.price * sale.quantity


def summarize_by_category(sales: list[Sale]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for sale in sales:
        totals[sale.category] = totals.get(sale.category, 0) + subtotal(sale)
    return totals


def main() -> None:
    sales = [
        Sale(item="Apple", category="Fruit", price=120, quantity=4),
        Sale(item="Banana", category="Fruit", price=80, quantity=6),
        Sale(item="Carrot", category="Vegetable", price=60, quantity=5),
        Sale(item="Tomato", category="Vegetable", price=150, quantity=3),
    ]

    print("Sales summary")
    print("-" * 30)

    grand_total = 0
    for sale in sales:
        amount = subtotal(sale)
        grand_total += amount
        print(f"{sale.item:10} x {sale.quantity:<2} = {amount:>4} yen")

    print("-" * 30)
    for category, amount in summarize_by_category(sales).items():
        print(f"{category:10}: {amount:>4} yen")

    print("-" * 30)
    print(f"Total      : {grand_total:>4} yen")


if __name__ == "__main__":
    main()