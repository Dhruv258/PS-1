'''
Global arguments
'''
import os 

# maximum filesize in megabytes
file_mb_max = 100
# encryption key
app_key = 'upload'
# full path destination for our upload files
UPLOADS_FOLDER = 'uploads_folder'

# list of allowed allowed extensions
extensions = ['csv', 'xlsx']

os.chmod('uploads_folder', 0o777)
def file_valid(file):
  return '.' in file and \
    file.rsplit('.', 1)[1] in extensions

