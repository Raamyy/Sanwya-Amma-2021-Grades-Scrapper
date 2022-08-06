import pickle
import pandas as pd
import os


def load_pickle(file_name):
    pickle_file = open(file_name,"rb")
    pickle_data = pickle.load(pickle_file)
    pickle_file.close()
    return pickle_data

def array_to_pandas(array):
    return pd.DataFrame(array)

def pandas_to_csv(pandas_array, file_name):
    pd.DataFrame(pandas_array).to_csv(file_name)
    
def get_directory_file_names(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def main():
    pickle_files = get_directory_file_names("data")
    students = []

    for pickle_file in pickle_files:
        students.extend(load_pickle(pickle_file))

    print(len(students))
    pdarr = array_to_pandas(students)  
    pandas_to_csv(pdarr, "students_data4.csv")

main()