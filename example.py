import os, shutil
for fi in os.listdir(os.getcwd()):
	if fi.endswith('.mp3'):
		shutil.move(fi,'./mp3')