import os
import shutil


def copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    copy_directory_contents(source, destination)


def copy_directory_contents(source, destination):
    for item_name in os.listdir(source):
        source_path = os.path.join(source, item_name)
        destination_path = os.path.join(destination, item_name)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            print(f"Creating directory: {destination_path}")
            os.mkdir(destination_path)

            copy_directory_contents(
                source_path,
                destination_path,
            )