#!/usr/bin/python

import sys, os

predict_name = ''
python_path = ''
inference_script = ''
arg_list = []

for arg in sys.argv[1:]:
    if arg.startswith('--inference_script='): inference_script=arg[len('--inference_script='):]
    elif arg.startswith('--python_path='): python_path=arg[len('--python_path='):]
    elif arg.startswith('--predict_name='): predict_name=arg[len('--predict_name='):]
    else: arg_list.append(arg)

dir = os.path.dirname(inference_script)
if not dir: dir = '.'
args = ' '.join('"'+arg+'"' for arg in arg_list)
cmd = 'cd %s; export PYTHONPATH="%s"; python "%s" %s' % (dir, python_path, inference_script, args)


if not predict_name: predict_name = 'Inference Tool'
try:
    from pyspark import SparkConf, SparkContext
    spark = SparkContext(appName=predict_name)
except:
    spark = None

print("Running", cmd)
os.system(cmd)

if spark: spark.stop()
