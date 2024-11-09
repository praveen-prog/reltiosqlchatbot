import shutil
import os

source_path = os.getcwd()
destination_path = os.path.join(source_path,'src')
source_file = os.path.join(source_path,'patients.db')
destination_file  = os.path.join(destination_path,'patients.db')

shutil.move(source_file, destination_file)