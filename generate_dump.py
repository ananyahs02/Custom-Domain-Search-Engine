import settings


def read_texts(zipfname):
    import zipfile
    import os
    import tokenizer
    import json
    files = 0
    with zipfile.ZipFile(zipfname) as z:
        for filename in z.namelist():
            if not filename[-1] == '/' and '.tsv' not in filename and '.json' not in filename:
                print('Reading File No:' +str(files))
                tokenizer.parserMain(z.read(filename), filename[filename.index("/")+1:], files%(settings.batch_size))
                files +=1 
            elif '.json' in filename:
                json_data = z.read(filename)
                settings.code2url = json.loads(json_data.decode("utf-8"))
                settings.write_json(settings.book_keeping_path, settings.code2url, 'w')
    tokenizer.write_to_file()
    settings.write_json(settings.doc_freq_path, settings.doc_freq, 'w+')
    settings.total_files = files
    settings.write_json(settings.total_files_path, settings.total_files,'w+')
    print(files)


def convert_tf_vec():
    import glob
    import math
    for filename in glob.glob(settings.file_tf_path+'*/*.json'):
        file_tf = settings.read_json(filename)
        wt = 0.0
        for key in file_tf:
            file_tf[key] = (1 + math.log(file_tf[key])) * math.log((settings.total_files/settings.doc_freq[key]))
            wt = wt + file_tf[key]**2
        file_vec = (wt, file_tf)
        settings.write_json(filename, file_vec, 'w+')


#### Deprecated
if __name__ == "__main__":
    settings.init()
    read_texts(settings.zip_path)