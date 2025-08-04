import argparse

def create_cli():
    parser = argparse.ArgumentParser(description="Getting info on the chosen products.")
    parser.add_argument("unit", help="The product you search for.")
    parser.add_argument("--printer", default="console", type=str, help="The printer.")
    parser.add_argument("--city", default="Moscow", type=str, help="The city of your search.")

    return parser.parse_args()


args = create_cli()
print(args.unit, args.printer)
