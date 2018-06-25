import argparse
import os
import sys

import cv2
import dlib
import numpy as np
import tensorflow as tf

import inception_resnet_v1

os.environ['CUDA_VISIBLE_DEVICES'] = ''

MODEL_PATH = "./model"

SESSION = None
AGE = None
GENDER = None
IMAGES_PL = None
TRAIN_MODE = None

# Tensorflow configuration to use CPU instead of GPU
tf_config = tf.ConfigProto(
	device_count = {'GPU': 0}
	)

def load_session(model_path=MODEL_PATH):
	global SESSION
	global AGE
	global GENDER
	global IMAGES_PL
	global TRAIN_MODE
	global tf_config

	graph = tf.Graph().as_default()
	sess = tf.Session(config=tf_config)
	images_pl = tf.placeholder(tf.float32, shape=[None, 160, 160, 3], name='input_image')
	images = tf.map_fn(lambda frame: tf.reverse_v2(frame, [-1]), images_pl) #BGR TO RGB
	images_norm = tf.map_fn(lambda frame: tf.image.per_image_standardization(frame), images)
	train_mode = tf.placeholder(tf.bool)
	age_logits, gender_logits, _ = inception_resnet_v1.inference(images_norm, keep_probability=1.0, #0.8
																	phase_train=train_mode,
																	weight_decay=1e-5)
	gender = tf.argmax(tf.nn.softmax(gender_logits), 1)
	age_ = tf.cast(tf.constant([i for i in range(0, 101)]), tf.float32)
	age = tf.reduce_sum(tf.multiply(tf.nn.softmax(age_logits), age_), axis=1)

	GENDER = gender
	AGE = age
	IMAGES_PL = images_pl
	TRAIN_MODE = train_mode

	init_op = tf.group(tf.global_variables_initializer(),
						tf.local_variables_initializer())
	sess.run(init_op)
	saver = tf.train.Saver()
	ckpt = tf.train.get_checkpoint_state(model_path)
	if ckpt and ckpt.model_checkpoint_path:
		saver.restore(sess, ckpt.model_checkpoint_path)
		print("restore and continue training!")
	else:
		sys.exit("Age-Gender Model not found")
	
	SESSION = sess

def eval_image(aligned_images):
	global SESSION
	global AGE
	global GENDER
	global IMAGES_PL
	global TRAIN_MODE

	assert(len(aligned_images)>0)
	assert(not SESSION == None)
	
	age = AGE
	gender = GENDER
	images_pl = IMAGES_PL
	train_mode = TRAIN_MODE
	return SESSION.run([age, gender], feed_dict={images_pl: aligned_images, train_mode: False})