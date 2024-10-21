#!/usr/bin/env python3

"""argparse.py at https://github.com/wilsonmar/python-samples/blob/main/argparse.py
STATUS: AttributeError: module 'argparse' has no attribute 'ArgumentParser'
"v001 new :argparse.py"
Tested on macOS 14.5 (23F79) using Python 3.13.
flake8  E501 line too long, E222 multiple spaces after operator

This program is an example of how to specify command line arguments into this program.
per https://docs.python.org/3/library/argparse.html#module-argparse
From https://github.com/JacobCallahan/Understanding/blob/master/Python/argparse_cli/pizza_builder.py
explained by John Callahan at https://www.youtube.com/watch?v=J51vxXAWigI and also:
https://www.youtube.com/watch?v=znuocj_7PMc by Real Python "Getting Started Building a Python CLI With argparse"
https://www.youtube.com/watch?v=88pl8TuuKz0 by NeuralNine
https://www.youtube.com/watch?v=w5Q_e4Nrw9c by Andrew Mallet
https://www.youtube.com/watch?v=aGy7U5ItLRk by Idently
https://www.youtube.com/watch?v=idq6rTYqvkY by codebasics

"""

# pip install argparse
import argparse

SIZES = {
    "s": "Small",
    "m": "Medium",
    "l": "Large",
    "xl": "Extra large",
    "xxl": "Extra extra large"
}

CRUSTS = {"normal": "", "thin": " thin crust", "deep": " deep dish"}


def build_pizza(order):
    pizza = f"{SIZES[order.size]}{CRUSTS[order.crust]}"
    if order.toppings:
        pizza +=  " with " + ", ".join(order.toppings)
    if order.cheese:
        pizza += " plus extra cheese"
    if order.sauce:
        pizza += " and extra sauce"
    return pizza


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # FIXME: AttributeError: module 'argparse' has no attribute 'ArgumentParser'
#    parser = argparse.ArgumentParser(description="Welcome to the pizza builder, let's build a pizza!!")

#    parser.add_argument('-f', '--foo', help='Description for foo argument', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")  # on/off flag
        # See https://docs.python.org/3/library/argparse.html#action

    parser.add_argument(
        "size",
        type=str,
        choices=SIZES.keys(),
        help="Size of your pizza"
    )
    parser.add_argument(
        "crust",
        type=str,
        choices=CRUSTS.keys(),
        help="Type of pizza crust"
    )
    parser.add_argument(
        "-t", "--toppings",
        type=str,
        nargs="+",
        help="One or more toppings for your pizza"
    )
    parser.add_argument(
        "--extra-cheese",
        action="store_true",
        dest="cheese",
        help="Add extra cheese to your pizza"
    )
    parser.add_argument(
        "--extra-sauce",
        action="store_true",
        dest="sauce",
        help="Add extra sauce to your pizza"
    )
    parsed_args = parser.parse_args()
    pizza = build_pizza(parsed_args)

    if args.verbose:
        print(f"{args.x} {args.operation} {args.y} = {result}")
    else:
        print(f"Your pizza is: {pizza}!!")
