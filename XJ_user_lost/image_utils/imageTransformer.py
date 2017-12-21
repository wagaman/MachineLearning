# --------------------------------------------------------
# Image Main dataset transformer
# Copyright (c) 2017 IBM
# Written by Dong Lin
# --------------------------------------------------------
import os
import sys
import xml.etree.ElementTree as ET
import numpy as np
import cv2
import argparse
import shutil
import time

class imageTransformor(object):
    def __init__(self, sourceDir, image_set, targetDir, xScale, yScale, isDraw):
        self.sDir = sourceDir
        self.tDir = targetDir
        self._image_set = image_set
        self._xScale = xScale
        self._yScale = yScale
        self._isDraw = isDraw
        self.start_time = time.time()

    def transoformImage(self):
        imageDir = os.path.join(self.sDir, "JPEGImages")
        annoationDir = os.path.join(self.sDir, "Annotations")
        dataDir = os.path.join(self.sDir, "ImageSets")

        if not os.path.isdir(self.tDir):
            os.mkdir(self.tDir)		
        t_imageDir = os.path.join(self.tDir, "JPEGImages")
        if not os.path.isdir(t_imageDir):
            os.mkdir(t_imageDir)
        t_annoationDir = os.path.join(self.tDir, "Annotations")
        if not os.path.isdir(t_annoationDir):
            os.mkdir(t_annoationDir)
        t_dataDir = os.path.join(self.tDir, "ImageSets")
        if not os.path.isdir(t_dataDir):
            os.mkdir(t_dataDir)
        t_dataDir_Main = os.path.join(t_dataDir, 'Main')
        if not os.path.isdir(t_dataDir_Main):
            os.mkdir(t_dataDir_Main)

        image_set_file = os.path.join(dataDir, 'Main', self._image_set + '.txt')
        t_image_set_file = os.path.join(t_dataDir_Main, self._image_set + '.txt')
        assert os.path.exists(image_set_file), \
                'Path does not exist: {}'.format(image_set_file)
        with open(image_set_file) as f:
            image_index = [x.strip() for x in f.readlines()]
        im_num = len(image_index)
        com_num = 0
        for index in image_index:
            com_num = com_num + 1
            boxes = self._update_image_annotation(index, os.path.join(annoationDir, index+".xml"), self._xScale, self._yScale)
            self._resize_image(index, os.path.join(imageDir, index+".jpg"), self._xScale, self._yScale, boxes)
            print("--> Resize status: image %s done, %s/%s(total)" %(index, com_num, im_num))

        shutil.copyfile(image_set_file, t_image_set_file)
        print "Congratulation, Image transform done!"
        print "Total Time cost: {:.3f}s".format(time.time() - self.start_time)

    def _resize_image(self, index, image_file, xScale, yScale, boxes):
        res_img = os.path.join(self.tDir, "JPEGImages", index+".jpg")
        im = cv2.imread(image_file)
        im = cv2.resize(im, None, None, fx=xScale, fy=yScale, interpolation=cv2.INTER_LINEAR)
        if self._isDraw:
            for i in xrange(boxes.shape[0]):
                box = boxes[i, :]
                cv2.rectangle(im,(box[0], box[1]),(box[2], box[3]),(0,255,0),3)
        cv2.imwrite(res_img,im)

    def _update_image_annotation(self, index, xml_file, xScale, yScale):
        filename = xml_file
        tree = ET.parse(filename)
        objs = tree.findall('object')
        sizes = tree.findall('size')
        num_objs = len(objs)
        boxes = np.zeros((num_objs, 4), dtype=np.uint16)

        #update size
        for i, size in enumerate(sizes):
            width = float(size.find('width').text)
            height = float(size.find('height').text)
            size.find('width').text = str(int(width*xScale))
            size.find('height').text = str(int(height*yScale))

        #update bbox
        for ix, obj in enumerate(objs):
            bbox = obj.find('bndbox')
            sx1 = float(bbox.find('xmin').text)
            sy1 = float(bbox.find('ymin').text)
            sx2 = float(bbox.find('xmax').text)
            sy2 = float(bbox.find('ymax').text)
            txmin = sx1 * xScale
            tymin = sy1 * yScale
            txmax = sx2 * xScale
            tymax = sy2 * yScale
            boxes[ix, :] = [int(txmin), int(tymin), int(txmax), int(tymax)]
            bbox.find('xmin').text = str(txmin)
            bbox.find('ymin').text = str(tymin)
            bbox.find('xmax').text = str(txmax)
            bbox.find('ymax').text = str(tymax)
        res_xml = os.path.join(self.tDir, "Annotations", index+".xml")
        tree.write(res_xml, encoding="utf-8",xml_declaration=True)
        return boxes

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Transform image main datasets')
    parser.add_argument('--input', dest='input_dir',
                        help='Input dataset path',
                        required=True, type=str)
    parser.add_argument('--dataset', dest='dataset',
                        help='dataset name (e.g., "trainval")',
                        required=True, type=str)
    parser.add_argument('--output', dest='output_dir',
                        help='output dataset path',
                        required=True, type=str)
    parser.add_argument('--xScale', dest='xScale',
                        help='scale ratio in horizontal',
                        required=True, type=float)
    parser.add_argument('--yScale', dest='yScale',
                        help='scale ratio in vertical',
                        required=True, type=float)
    parser.add_argument('--draw', dest='isDraw',
                        help='draw bbox or not (e.g., "True" or "False"(default))',
                        default=False, type=bool)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    #im = imageTransformor("/gpfs/user_homes/donglbj/pyt/data", "trainval", "/gpfs/user_homes/donglbj/pyt/output", 0.5, 0.5);
    im = imageTransformor(args.input_dir, args.dataset, args.output_dir, args.xScale, args.yScale, args.isDraw);
    im.transoformImage()

