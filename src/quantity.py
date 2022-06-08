from decimal import Decimal

def quantity_mod(ingredients):
    while True:
        try:
            ratio = Decimal(input('Enter a ratio (0.5 for half, 2 for double): '))
        except ValueError:
            print("Please enter a valid decimal.")
        else:
            break

    for ingredient in ingredients:
        if ingredient["quantity"]:
            ingredient["quantity"] = str(Decimal(ingredient["quantity"].strip(' "')) * ratio)
