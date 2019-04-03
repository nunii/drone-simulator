import glob
import os

os.chdir("_path_to_datasets_dir")
for files in glob.glob("*.csv"):
        print(files)

f_out = open("Final_data_set.csv", "a")
for file in glob.glob("*.csv"):
    f = open(file)
    f.next()  # skip the header
    for line in f:
        f_out.write(line)
    f.close()
f_out.close()
