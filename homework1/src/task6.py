def count_words(filename):
    with open(filename, "r") as file:
        text = file.read()
    return len(text.split())