import os
import time


X = lambda s: os.system(s)
X('git add .')
X(f'git commit -m "Make changes - {time.ctime()}"')
X('git push origin master')

