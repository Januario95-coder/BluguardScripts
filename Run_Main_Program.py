import os
import logging
from mysql.connector import ProgrammingError




X = lambda s: os.system(s)
os.chdir('C:/Users/hayysoft/Documents/BluguardScripts')



try:
    logger = logging.getLogger('Run Server')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('C:/Users/hayysoft/Documents/LogFiles/Run_Main_Program.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('\nProgram started!')

    X('python Main_Program.py')
except KeyboardInterrupt as e:
    logger.exception(e)
except Exception as e:
    logger.exception(e)
finally:
    logger.info('Program Finished!\n')
    X('python Main_Program.py')


