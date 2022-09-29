from BLACK_MAGIC import trick as black_magic
import os

black_magic.encrypt_file(file_name='input')
os.system('rm -r SOURCE/input') 
os.system('touch SOURCE/input')