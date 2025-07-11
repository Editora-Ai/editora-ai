# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:02:16 2020

@author: ASUS
"""

# -*- coding: utf-8 -*-

import time
import tensorflow as tf
import numpy as np
import os
import time
import cv2

checkpoint_dir = 'editora_api/train_data_crop'
checkpoint_dir2 = 'editora_api/train_data_seg'
#checkpoint_dir2 = 'E:/pix2pix saved models/sV'
const=7
BUFFER_SIZE = 200
BATCH_SIZE = 1
IMG_WIDTH = 256*const
IMG_HEIGHT = 256*const

def load(image_file):
  image = tf.io.read_file(image_file)
  image = tf.image.decode_jpeg(image)

  w = tf.shape(image)[1]

  real_image = image[:, :w, :]
  input_image = image[:, :w, :]

  input_image = tf.cast(input_image, tf.float32)
  real_image = tf.cast(real_image, tf.float32)

  return input_image, real_image


def resize(input_image, real_image, height, width):
  IMH = len(input_image)
  IMW = len(input_image[0])
  input_image = tf.image.resize(input_image, [height, width],
                                method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
  real_image = tf.image.resize(real_image, [height, width],
                               method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)

  return input_image, real_image ,IMW,IMH
def random_crop(input_image, real_image):
  stacked_image = tf.stack([input_image, real_image], axis=0)
  cropped_image = tf.image.random_crop(
      stacked_image, size=[2, IMG_HEIGHT, IMG_WIDTH, 3])

  return cropped_image[0], cropped_image[1]


def normalize(input_image, real_image):
  input_image = (input_image / 127.5) - 1
  real_image = (real_image / 127.5) - 1

  return input_image, real_image



#@tf.function()
def random_jitter(input_image, real_image):
  input_image, real_image , IMW , IMH= resize(input_image, real_image, 286*const, 286*const)

  input_image, real_image = random_crop(input_image, real_image)

  if tf.random.uniform(()) > 0.5:
    input_image = tf.image.flip_left_right(input_image)
    real_image = tf.image.flip_left_right(real_image)

  return input_image, real_image , IMW,IMH

def load_image_train(image_file):
  input_image, real_image = load(image_file)
  input_image, real_image,IMW,IMH = random_jitter(input_image, real_image)
  input_image, real_image = normalize(input_image, real_image)

  return input_image, real_image
def load_image_test(image_file):
  input_image, real_image = load(image_file)
  input_image, real_image , IMW,IMH= resize(input_image, real_image,
                                   IMG_HEIGHT, IMG_WIDTH)
  input_image, real_image = normalize(input_image, real_image)

  return input_image, real_image , IMW, IMH,image_file


OUTPUT_CHANNELS = 3
def downsample(filters, size, apply_batchnorm=True):
  initializer = tf.random_normal_initializer(0., 0.02)

  result = tf.keras.Sequential()
  result.add(
      tf.keras.layers.Conv2D(filters, size, strides=2, padding='same',
                             kernel_initializer=initializer, use_bias=False))

  if apply_batchnorm:
    result.add(tf.keras.layers.BatchNormalization())

  result.add(tf.keras.layers.LeakyReLU())

  return result
def upsample(filters, size, apply_dropout=False):
  initializer = tf.random_normal_initializer(0., 0.02)

  result = tf.keras.Sequential()
  result.add(
    tf.keras.layers.Conv2DTranspose(filters, size, strides=2,
                                    padding='same',
                                    kernel_initializer=initializer,
                                    use_bias=False))

  result.add(tf.keras.layers.BatchNormalization())

  if apply_dropout:
      result.add(tf.keras.layers.Dropout(0.5))

  result.add(tf.keras.layers.ReLU())

  return result
def Generator():
  inputs = tf.keras.layers.Input(shape=[256*const,256*const,3])

  down_stack = [
    downsample(64, 4, apply_batchnorm=False), # (bs, 512, 128, 64)
    downsample(128, 4), # (bs, 256, 64, 128)
    downsample(256, 4), # (bs, 128, 32, 256)
    downsample(512, 4), # (bs, 64, 16, 512)
    downsample(512, 4), # (bs, 32, 8, 512)
    downsample(512, 4), # (bs, 16, 4, 512)
    downsample(512, 4), # (bs, 8, 2, 512)
    downsample(512, 4), # (bs, 4, 1, 512)
#    downsample(1024, 4), # (bs, 2, 2, 512)
#    downsample(1024, 4), # (bs, 2, 1, 512)
  ]

  up_stack = [
#    upsample(1024, 4, apply_dropout=True), # (bs, 2, 2, 1024)
#    upsample(1024, 4, apply_dropout=True), # (bs, 4, 4, 1024)
    upsample(512, 4, apply_dropout=True), # (bs, 2, 2, 1024)
    upsample(512, 4, apply_dropout=True), # (bs, 4, 4, 1024)
    upsample(512, 4, apply_dropout=True), # (bs, 8, 8, 1024)
    upsample(512, 4), # (bs, 16, 16, 1024)
    upsample(256, 4), # (bs, 32, 32, 512)
    upsample(128, 4), # (bs, 64, 64, 256)
    upsample(64, 4), # (bs, 128, 128, 128)
  ]


  initializer = tf.random_normal_initializer(0., 0.02)
  last = tf.keras.layers.Conv2DTranspose(OUTPUT_CHANNELS, 4,
                                         strides=2,
                                         padding='same',
                                         kernel_initializer=initializer,
                                         activation='tanh') # (bs, 256, 256, 3)

  x = inputs

  # Downsampling through the model
  skips = []
  for down in down_stack:
    x = down(x)
    skips.append(x)

  skips = reversed(skips[:-1])

  # Upsampling and establishing the skip connections
  for up, skip in zip(up_stack, skips):
    x = up(x)
    x = tf.keras.layers.Concatenate()([x, skip])

  x = last(x)

  return tf.keras.Model(inputs=inputs, outputs=x)
generator = Generator()
LAMBDA = 100
def generator_loss(disc_generated_output, gen_output, target):
  gan_loss = loss_object(tf.ones_like(disc_generated_output), disc_generated_output)

  # mean absolute error
  l1_loss = tf.reduce_mean(tf.abs(target - gen_output))

  total_gen_loss = gan_loss + (LAMBDA * l1_loss)

  return total_gen_loss, gan_loss, l1_loss

def Discriminator():
  initializer = tf.random_normal_initializer(0., 0.02)

  inp = tf.keras.layers.Input(shape=[256*const, 256*const, 3], name='input_image')
  tar = tf.keras.layers.Input(shape=[256*const, 256*const, 3], name='target_image')

  x = tf.keras.layers.concatenate([inp, tar]) # (bs, 256, 256, channels*2)

  down1 = downsample(64, 4, False)(x) # (bs, 128, 128, 64)
  down2 = downsample(128, 4)(down1) # (bs, 64, 64, 128)
  down3 = downsample(256, 4)(down2) # (bs, 32, 32, 256)
#  down4 = downsample(512, 4)(down3) # (bs, 32, 32, 256)

  zero_pad1 = tf.keras.layers.ZeroPadding2D()(down3) # (bs, 34, 34, 256)
  conv = tf.keras.layers.Conv2D(512, 4, strides=1,
                                kernel_initializer=initializer,
                                use_bias=False)(zero_pad1) # (bs, 31, 31, 512)

  batchnorm1 = tf.keras.layers.BatchNormalization()(conv)

  leaky_relu = tf.keras.layers.LeakyReLU()(batchnorm1)

  zero_pad2 = tf.keras.layers.ZeroPadding2D()(leaky_relu) # (bs, 33, 33, 512)

  last = tf.keras.layers.Conv2D(1, 4, strides=1,
                                kernel_initializer=initializer)(zero_pad2) # (bs, 30, 30, 1)

  return tf.keras.Model(inputs=[inp, tar], outputs=last)
discriminator = Discriminator()
loss_object = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def discriminator_loss(disc_real_output, disc_generated_output):
  real_loss = loss_object(tf.ones_like(disc_real_output), disc_real_output)

  generated_loss = loss_object(tf.zeros_like(disc_generated_output), disc_generated_output)

  total_disc_loss = real_loss + generated_loss

  return total_disc_loss

generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
discriminator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
#
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                 discriminator_optimizer=discriminator_optimizer,
                                 generator=generator,
                                 discriminator=discriminator)






def generate_images3(model,input_image):
	imwidth = input_image.shape[1]
	imheight = input_image.shape[0]
	input_image = np.array(input_image , np.float32)

	input_image = cv2.resize(input_image , dsize = (256*const , 256*const))
	input_image = np.reshape(input_image , (1,256*const,256*const,3))
	input_image = (input_image / 127.5) - 1
	prediction = model(input_image , training = False)
#    out = cv2.resize(prediction[0],dsize = (imwidth,imheight))
	out = prediction[0]
	out = np.array(out,np.float32)
#	out = out*0.5 + 0.5
	out = out*255
	out = np.array(out , np.uint8)
	out = cv2.resize(out,dsize = (imwidth,imheight))

	return out

def fixchannels(img):
	imw = img.shape[0]
	imh = img.shape[1]
	imd = img.shape[2]
	bed = np.zeros(shape = (imw, imh , imd))
	b = img[:,:,0]
	g = img[:,:,1]
	r = img[:,:,2]
	bed[:,:,0] = r
	bed[:,:,1] = g
	bed[:,:,2] = b
	return bed



def Final(image, alpha = 1.20 , beta = 10):
	checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))
	x,X,y,Y = 0,0,0,0
#	x2,X2,y2,Y2 = 0,0,0,0

	IMAGE = np.array(image , np.uint8)


	img = fixchannels(IMAGE)

	otpt = generate_images3(generator , img)
	cropmap = otpt[:,:,0]

	for i in range(cropmap.shape[0]):
		if 2 in cropmap[i]:
			x = i
			break
	for i in range(cropmap.shape[0]):
		if 2 in cropmap[i]:
			X = i
	for i in range(cropmap.shape[1]):
		if 2 in cropmap[:,i]:
			y = i
			break
	for i in range(cropmap.shape[1]):
		if 2 in cropmap[:,i]:
			Y = i
	delta = 50
	if x-delta > 0 :
		x = x-delta
	else :
		x = 0

	if y-delta > 0 :
		y = y-delta
	else :
		y = 0

	if X+delta < cropmap.shape[0] :
		X += delta
	else :
		X = cropmap.shape[0]
	if Y+delta < cropmap.shape[1] :
		Y += delta
	else :
		Y = cropmap.shape[1]


	croped_image = img[x:X,y:Y]
	croped_raw = IMAGE[x:X , y:Y]
	checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir2))
	otpt = generate_images3(generator , croped_image)
	BGrem_map = otpt[:,:,0]
	BGrem_map = np.array(BGrem_map , np.uint8)
	croped_raw = np.array(croped_raw , np.uint8)
	BGrem_map = BGrem_map.reshape(BGrem_map.shape[0]*BGrem_map.shape[1])
	PPP = croped_raw.shape[0]
	QQQ = croped_raw.shape[1]
	croped_raw = croped_raw.reshape(croped_raw.shape[0]*croped_raw.shape[1] , 3)
	croped_raw[BGrem_map>252] = [255,255,255]
	croped_raw = croped_raw.reshape(PPP,QQQ , 3)
	croped_raw = np.array(croped_raw, np.float32)
	croped_raw = croped_raw*alpha + beta
	croped_raw = np.clip(croped_raw,0,255)
	croped_raw = np.array(croped_raw, np.uint8)
	return croped_raw
