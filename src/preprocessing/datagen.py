# from sklearn.preprocessing import LabelEncoder
# from keras.preprocessing import sequence
# import numpy as np
# import gzip
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from csv import DictWriter


def load(fname):

    with zipfile.ZipFile(fname) as datazip:
        print([(i.filename, i.file_size) for i in datazip.infolist()])

        # Create a TSV from each XML in this zip file
        for fname in datazip.namelist():
            # Use the filename stem to create a tsv version
            stem = Path(fname).stem

            with datazip.open(fname, "r") as xmlfile, open(
                stem + ".tsv", "w", newline=""
            ) as tsvfile:
                writer = DictWriter(
                    tsvfile,
                    fieldnames=["id", "hyperpartisan", "bias", "labeled-by", "url"],
                    delimiter="\t"
                )
                writer.writeheader()

                for event, elem in ET.iterparse(xmlfile):
                    print(elem.attrib)
                    if elem.attrib:
                        writer.writerow(elem.attrib)
                    elem.clear()


# from timeit import Timer
# t = Timer(
#     "filepath = './data/published/articles-training-bypublisher-20181122.zip'; \
#     extract_to = './data/published/training'; \
#     from zipfile import ZipFile; \
#     ZipFile(filepath).extractall(path=extract_to)"
# )
# t = Timer(
#     """filepath = './data/published/articles-training-bypublisher-20181122.zip'
# from zipfile import ZipFile
# files = []
# with open(filepath) as f:
#     files = [(i.filename, i.file_size) for i in ZipFile(filepath).infolist()];
# print(files)"""
# )

# t.timeit(1)


# def load_data(data_path, max_len=200):


# def unzip_member_f3(zip_filepath, filename, dest):
#     with open(zip_filepath, 'rb') as f:
#         zf = zipfile.ZipFile(f)
#         zf.extract(filename, dest)
#     fn = os.path.join(dest, filename)
#     return _count_file(fn)
#
#
#
# def f3(fn, dest):
#     with open(fn, 'rb') as f:
#         zf = zipfile.ZipFile(f)
#         futures = []
#         with concurrent.futures.ProcessPoolExecutor() as executor:
#             for member in zf.infolist():
#                 futures.append(
#                     executor.submit(
#                         unzip_member_f3,
#                         fn,
#                         member.filename,
#                         dest,
#                     )
#                 )
#             total = 0
#             for future in concurrent.futures.as_completed(futures):
#                 total += future.result()
#     return total


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Enter an XML file to convert to TSV")
    parser.add_argument("-f", "--fname", help="path to filename")
    args = parser.parse_args()
    load(args.fname)
