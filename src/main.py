from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node, extract_title
import os
import shutil


def main():
    # Remove anything in the public directory
    public_dir = "public"
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_directory_recursive("static", public_dir)
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )


def copy_directory_recursive(src, dest):
    # Delete all contents of the destination directory
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)

    # Walk through the source directory
    for root, dirs, files in os.walk(src):
        # Calculate the relative path and destination path
        rel_path = os.path.relpath(root, src)
        dest_path = os.path.join(dest, rel_path)

        # Create directories in the destination
        os.makedirs(dest_path, exist_ok=True)

        # Copy each file
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_path, file)
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {src_file} -> {dest_file}")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read the template
    with open(template_path, "r") as template_file:
        template = template_file.read()
    # Read the markdown file
    with open(from_path, "r") as md_file:
        markdown = md_file.read()
    # Convert markdown to HTML
    html = markdown_to_html_node(markdown).to_html()
    # Replace the placeholder in the template with the generated HTML
    page = template.replace("{{ Title }}", extract_title(markdown))
    page = page.replace("{{ Content }}", html)

    print(f"Writing page to {dest_path}")
    # Write the generated page to the destination path
    with open(dest_path, "w") as dest_file:
        dest_file.write(page)


if __name__ == "__main__":
    # Generate the index page
    main()
