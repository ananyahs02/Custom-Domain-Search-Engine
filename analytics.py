import settings


def get_unique_words():
    unique = 0
    from string import ascii_lowercase
    for c in ascii_lowercase:
        file_name = "dump/"+c+".json"
        data = settings.read_json(file_name)
        unique += len(data.keys())
    print(unique)
    return unique

get_unique_words()