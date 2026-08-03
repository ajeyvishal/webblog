import os

from block_markdown import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("No h1 heading found")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} "
        f"to {dest_path} using {template_path}"
    )

    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    destination_directory = os.path.dirname(dest_path)

    if destination_directory:
        os.makedirs(destination_directory, exist_ok=True)

    with open(dest_path, "w") as destination_file:
        destination_file.write(full_html)

def generate_pages_recursive(
    dir_path_content,
    template_path,
    dest_dir_path,
):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        destination_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path):
            if not entry.endswith(".md"):
                continue

            destination_path = os.path.splitext(destination_path)[0] + ".html"

            generate_page(
                source_path,
                template_path,
                destination_path,
            )
        else:
            generate_pages_recursive(
                source_path,
                template_path,
                destination_path,
            )