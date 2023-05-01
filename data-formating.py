import os
import patoolib
import shutil
import glob
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')


ROOT_DIR = os.getcwd()
DATA_DIR = "Data"
TEMPD = "Temp_dir"


if os.path.exists(TEMPD):
    shutil.rmtree(TEMPD)

os.mkdir(TEMPD)
data_path = os.path.join(ROOT_DIR, TEMPD)

def data_extract():
    for i in os.listdir(ROOT_DIR):
        # if os.path.exists(data_path):
        #     shutil.rmtree(data_path)
        if i.endswith(".zip"):
            patoolib.extract_archive(i, outdir=os.path.join("./",TEMPD))
            os.remove(i)
    return ()


def filename():
    for i in os.listdir(data_path):
        for f in os.listdir(os.path.join(data_path, i)):
            {}
    name = f[8:]
    return (name)

def main():
    data_extract()
    combined_csv = pd.DataFrame()
    new_file_name = filename()
    for i in os.listdir(data_path):
        for file in os.listdir(os.path.join(data_path, i)):
            df = pd.read_csv(os.path.join(data_path, i, file))
            combined_csv = combined_csv.append(df, ignore_index=True)
    combined_csv.to_csv(os.path.join(DATA_DIR, new_file_name), index=False, encoding='utf-8')
    shutil.rmtree(TEMPD)
    return ()


if __name__ == '__main__':
    main()
