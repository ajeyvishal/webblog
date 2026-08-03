from copystatic import copy_directory
from page_generator import generate_pages_recursive


def main():
    copy_directory("static", "public")

    generate_pages_recursive(
        "content",
        "template.html",
        "public",
    )


if __name__ == "__main__":
    main()