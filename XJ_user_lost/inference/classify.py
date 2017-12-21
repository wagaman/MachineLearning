#!/usr/bin/env python
"""
classify.py configures and runs the Caffe reference model.
"""
import numpy as np
import os
import sys
import argparse
import glob
import time
import json
import matplotlib
matplotlib.use("Pdf")
from pyspark import SparkConf, SparkContext

CAFFE_HOME = '_CAFFE_HOME_/caffe-public/'
sys.path.insert(0, CAFFE_HOME + 'python')
import caffe


def main(argv):

    parser = argparse.ArgumentParser()
    # Required arguments: input and output files.
    parser.add_argument(
        "--input_dir",
        help="Input image, directory, or npy."
    )
    parser.add_argument(
        "--output_dir",
        help="Directory where to put the inference result."
    )
    parser.add_argument(
        "--output_file",
        help="File name of the inference result."
    )
    parser.add_argument(
        "--model_def",
        help="Model definition file."
    )
    parser.add_argument(
        "--pretrained_model",
        help="Trained model weights file."
    )
    parser.add_argument(
        "--label_file",
        help="Labels of the image classes."
    )
    # Optional arguments.
    parser.add_argument(
        "--gpu",
        action='store_true',
        help="Switch for gpu computation."
    )
    parser.add_argument(
        "--center_only",
        action='store_true',
        help="Switch for prediction from center crop alone instead of " +
             "averaging predictions across crops (default)."
    )
    parser.add_argument(
        "--images_dim",
        default='256,256',
        help="Canonical 'height,width' dimensions of input images."
    )
    parser.add_argument(
        "--mean_file",
        help="Data set image mean of [Channels x Height x Width] dimensions " +
             "(numpy array). Set to '' for no mean subtraction."
    )
    
    parser.add_argument(
        "--prob_thresh",
        type=float,
        default=0.1,
        help="Probability for predict."
    )
    parser.add_argument(
        "--input_scale",
        type=float,
        help="Multiply input features by this scale to finish preprocessing."
    )
    parser.add_argument(
        "--raw_scale",
        type=float,
        default=255.0,
        help="Multiply raw input by this scale before preprocessing."
    )
    parser.add_argument(
        "--channel_swap",
        default='2,1,0',
        help="Order to permute input channels. The default converts " +
             "RGB -> BGR since BGR is the Caffe default by way of OpenCV."
    )
    parser.add_argument(
        "--ext",
        default='jpg',
        help="Image file extension to take as input when a directory " +
             "is given as the input file."
    )
    args = parser.parse_args()
    
    spark = SparkContext(appName="Bluemind Predict Classify Tool")
    
    image_dims = [int(s) for s in args.images_dim.split(',')]

    mean, channel_swap = None, None
    if args.mean_file:
        MEAN_PROTO_PATH = args.mean_file + '/mean.binaryproto'
        MEAN_NPY_PATH = args.mean_file + '/mean.npy'
        blob = caffe.proto.caffe_pb2.BlobProto()
        data = open(MEAN_PROTO_PATH, 'rb' ).read()
        blob.ParseFromString(data)
        array = np.array(caffe.io.blobproto_to_array(blob))
        mean_npy = array[0]
        np.save(MEAN_NPY_PATH ,mean_npy)
        mean = np.load(MEAN_NPY_PATH).mean(1).mean(1)
    if args.channel_swap:
        channel_swap = [int(s) for s in args.channel_swap.split(',')]

    if args.gpu:
        caffe.set_mode_gpu()
        print("GPU mode")
    else:
        caffe.set_mode_cpu()
        print("CPU mode")

    # Make classifier.
    classifier = caffe.Classifier(args.model_def, args.pretrained_model,
            image_dims=image_dims, mean=mean,
            input_scale=args.input_scale, raw_scale=args.raw_scale,
            channel_swap=channel_swap)

    # Load numpy array (.npy), directory glob (*.jpg), or image file.
    args.input_dir = os.path.expanduser(args.input_dir)
    inputs = []
    imagenames = [] 
    if os.path.isdir(args.input_dir):
        print("Loading folder: %s" % args.input_dir)
        for im_f in glob.glob(args.input_dir + '/*.*'):
            inputs.append(caffe.io.load_image(im_f))
            imagenames.append(os.path.basename(im_f))
            
    print("Classifying %d inputs." % len(inputs))

    # Classify.
    start = time.time()
    predictions = classifier.predict(inputs, not args.center_only)
    print("Done in %.2f s." % (time.time() - start))
    if os.path.exists(args.label_file):
        CLASSES = [line.strip() for line in open(args.label_file) if line]
    else:
        CLASSES = None

    results = [] 
    for i in np.arange(len(imagenames)):
        sampleId = imagenames[i]
        proba = predictions[i][predictions[i].argmax()]
        top_k = predictions[i].flatten().argsort()[::-1]
        j = 0
        go = True
        while go:
            if (j < len(top_k) and predictions[i,top_k[j]] >= args.prob_thresh):
                label = CLASSES and CLASSES[top_k[j]] or str(int(top_k[j]))
                prob = float('%.3f'%predictions[i,top_k[j]])
                results.append({"sampleId":sampleId, "label":label, "prob":prob})
                j+=1
            else:
                go = False
    with open(os.path.join(args.output_dir, args.output_file), 'w') as f:
         json.dump({"type":"ImageClassfication", "result":results}, f, indent=4)

    spark.stop()

if __name__ == '__main__':
    main(sys.argv)
