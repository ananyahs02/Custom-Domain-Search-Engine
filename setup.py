import generate_dump
import settings


if __name__ == "__main__":
    ## Initializes everything
    ## 1: Run everything
    ## 2: Only convert vec to idf
    choice =1
    if choice== 1:
        settings.init()
        generate_dump.read_texts(settings.zip_path)
    settings.load_data()
    settings.take_backup(settings.file_tf_path)
    generate_dump.convert_tf_vec()