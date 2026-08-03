import sys

from copystatic import copy_directory
from page_generator import generate_pages_recursive


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    copy_directory("static", "docs")

    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        basepath,
    )


if __name__ == "__main__":
    main()