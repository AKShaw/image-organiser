import logging
import pathlib
import argparse

from services.organiser import OrganiserService


def get_args():
    arg_parser = argparse.ArgumentParser(description="Image organiser argument helper")
    arg_parser.add_argument('-i', '--input', type=pathlib.Path, required=True)
    arg_parser.add_argument('-o', '--output', type=pathlib.Path, required=True)
    arg_parser.add_argument('-f', '--faces', action='store_true')
    arg_parser.add_argument('-d', '--debug', action='store_true')
    return arg_parser.parse_args()


def main():
    args = get_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    organiser = OrganiserService(source=args.input,
                                 destination=args.output)
    organiser.organise_images_by_date(args.faces)


if __name__ == "__main__":
    main()
