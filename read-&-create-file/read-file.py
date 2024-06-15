import os
import json
import pandas as pd


def read_text_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def read_csv_file(file_path):
    if file_path.split(".")[len(file_path.split(".")) - 1] == "csv":
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    return df.to_string()


def read_json_file(file_path):
    with open(file_path, "r") as file:
        content = json.load(file)
    return json.dumps(content, indent=4)


def read_file(file_path):
    if not os.path.isfile(file_path):
        return f"Error: The file {file_path} does not exist."

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".txt":
        return read_text_file(file_path)
    elif file_extension == ".csv" or ".clsx":
        return read_csv_file(file_path)
    elif file_extension == ".json":
        return read_json_file(file_path)
    else:
        return f"Unsupported file type: {file_extension}"


if __name__ == "__main__":
    # Replace with the path to the file you want to read
    file_path = input("Enter the name file with its extension:\n")
    content = read_file(file_path)
    print(content)
