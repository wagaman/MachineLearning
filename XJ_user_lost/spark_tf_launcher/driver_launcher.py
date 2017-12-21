#!/usr/bin/python

import sys, os

app_name = ''
python_path = ''
app_script = ''
arg_list = []

for arg in sys.argv[1:]:
    if arg.startswith('--app_script='): app_script=arg[len('--app_script='):]
    elif arg.startswith('--python_path='): python_path=arg[len('--python_path='):]
    elif arg.startswith('--app_name='): app_name=arg[len('--app_name='):]
    else: arg_list.append(arg)

dir = os.path.dirname(app_script)
if not dir: dir = '.'
args = ' '.join('"'+arg+'"' for arg in arg_list)
cmd = 'cd %s; export PYTHONPATH="%s"; python "%s" %s' % (dir, python_path, app_script, args)


if not app_name: app_name = 'Spark App Tool'
try:
    from pyspark import SparkConf, SparkContext
    spark = SparkContext(appName=app_name)
except:
    spark = None

print("Running", cmd)
os.system(cmd)

if spark: spark.stop()
