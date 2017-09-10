import unittest


def calculate_subtotal():
    print('Calculate subtotal')
    return 400.0


def calculate_taxable_subtotal():
    print('Calculate taxable subtotal')
    return 600.0


def calculate_total():
    print('Calculate total')
    return calculate_subtotal() + calculate_taxable_subtotal() * 0.15 \
        - (calculate_subtotal() * 0.1 if calculate_subtotal() > 100 else 0)


if __name__ == "__main__":
    total = calculate_total()
    print('Total: {}'.format(total))
    