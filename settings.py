import json

def create_dump():
    from string import ascii_lowercase
    for c in ascii_lowercase:
        file_name = "dump/word2doc/"+c+".json"
        write_json(file_name, dict(),'w+')

'''        f= open(file_name, 'w+')
        f.close()
        with open(file_name, 'w') as file_new:
            json.dump(dict(), file_new)
            file_new.close()'''

def reset_buffer():
    from string import ascii_lowercase
    for c in ascii_lowercase:
        buffer_dict[c] = dict()


def read_zip(zipfname, code):
    import zipfile
    archive = zipfile.ZipFile(zipfname)
    file = archive.read('WEBPAGES_RAW/'+code)
    return file
    


def write_json(file_path, data_dump, attr):
    import os
    path, file_name = os.path.split(file_path)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(file_path, attr) as file:
        json.dump(data_dump, file)
        file.close()


def write_as_file(file_path, data, attr):
    with open(file_path, attr) as file:
        for idx in enumerate(data):
            file.write(str(idx[0]+1)+'. '+idx[1]+'\n')
        file.close()


def read_json(file_path):
    json_obj = {}
    with open(file_path, 'r+') as file:
        json_obj = json.loads(file.read())
        file.close()
    return json_obj


def take_backup(src):
    import shutil
    import errno
    dest = 'backup/'+src
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


def load_data():
    print('Loading Data')
    global code2url
    global total_files
    global doc_freq
    code2url = read_json(book_keeping_path)
    doc_freq = read_json(doc_freq_path)
    total_files = read_json(total_files_path)

def init():
    global buffer_dict
    global code2url
    global doc_freq
    global zip_path
    global total_files
    global batch_size
    code2url = dict()
    buffer_dict = dict()
    doc_freq = dict()
    reset_buffer()
    create_dump()  

zip_path = "data/webpages.zip"
book_keeping_path = "dump/bookkeeping.json"
doc_freq_path = "dump/file_df/file_df.json"
file_tf_path = "dump/file_tf/"
total_files_path = "dump/file_df/total_files.json"
batch_size = 1000