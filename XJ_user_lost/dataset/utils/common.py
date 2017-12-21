import log
import logging
import os
import sys
import time
import os.path
import shutil
import platform
import subprocess
import utils

logger = logging.getLogger('utils.common')

'''
Create directory recursively
'''
def mkdir(d, clean=False):
    """
    Safely create a directory

    Arguments:
    d -- the directory name

    Keyword arguments:
    clean -- if True and the directory already exists, it will be deleted and recreated
    """
    if os.path.exists(d):
        if clean:
            shutil.rmtree(d)
            logger.warn('Will remove all the contents under diretory: %s' % d)
        else:
           return
    os.makedirs(d)
    logger.debug('Create directory %s successfully.' % d)
    #os.mkdir(d)

'''
Remove a directory
'''
def rmdir(d):
    """
    Remove a directory

    Arguments:
    d -- the directory name
    """
    if os.path.exists(d):
        shutil.rmtree(d)
        logger.debug('Remove directory %s successfully.' % d)  
    else:
        logger.warn('The specified directory %s is not existing.' % d)      

'''
Copy files tree
'''
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

'''
Copy a file or directory to destition
'''
def copy(src, dest):
    """
    Copy a file or directory to destition

    Arguments:
    src -- the source file or directory
    dest -- the destition directory
    """
    if not os.path.isdir(dest):
        logger.warn('The destition must be a directory')
        return

    if not os.path.exists(src):
        logger.warn('The source file or directory is not existing.') 
        return  

    if os.path.isdir(src):
        dest_dir = '%s/%s' % (dest, os.path.basename(src))
        logger.debug('The final dest dir is: %s' % dest_dir)
        mkdir(dest_dir, clean=True)
        copytree(src, dest_dir)
        #shutil.copytree(src, dest) 
    if os.path.isfile(src):
        shutil.copy(src, dest)
    logger.debug('Copy file or directory successfully.')  

"""
Create subprocess with args list
"""
def create_subprocess(args_list):
    count = 0
    for pargs in args_list:
        if len(pargs) > 0:
            logger.info('The subprocess#%d is started.' % count)
            logger.info('Create subprocess#%d with args: %s' % (count, ' '.join(pargs)))
            logger.info('')
            env = os.environ.copy()
            p = subprocess.Popen(pargs,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd='/tmp',
                close_fds=False if platform.system() == 'Windows' else True,
                env=env,
                )

            while p.poll() is None:
                for line in utils.nonblocking_readlines(p.stdout):
                    if line is not None:
                        # Remove whitespace
                        line = line.strip()

                    if line:
                        print line.strip()
                        #logger.info('%s: %s' % ('create_db.py', line.strip()))
                    else:
                        time.sleep(0.05)

            logger.info('The subprocess#%d is completed, return code: [%s]' % (count, p.returncode))
            count = count + 1
            logger.info('')
            time.sleep(1)            
        else:
            continue 
"""
"""                 