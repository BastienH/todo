import os

cmd = "start /b python done_list.py &"\
      "start /b python todo_list.py &"\
      "start /b python get_screenshots.py"

os.system(cmd)

