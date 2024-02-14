""" Main entry point for classifypdf """
import argparse
from importlib.metadata import version
import sys

from classifypdf._util import MyException, RawFormatter

class Classifypdf:
    """ Main class """
    parser = None
    version=None
    verbose=False

    def __init__(self):
        pass

    def make_cmd_line_parser(self):
        """Set up the command line parser"""
        self.parser = argparse.ArgumentParser(
            formatter_class=RawFormatter,
            description="Classify PDFs for Devonthink",
        )
        self.parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=version("dml-classifypdf"),
            help="Print the version number",
        )
        self.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            default=False,
            help="Verbose output",
        )
 
    def parse_args(self):
        """Parse the command line arguments"""
        args = self.parser.parse_args()

        self.verbose = args.verbose
 
    def run(self):
        """ Main entry point """
        self.make_cmd_line_parser()
        self.parse_args()

def main():
    """Main entry point"""
    try:
        Classifypdf().run()
    except MyException as e:
        print(e.msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
