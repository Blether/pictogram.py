# copyright 2014-2016
# make an array of icons to act as a decision aid

import Image, ImageChops, ImageDraw, ImageFont, ImageOps
import math
import numpy as np

def addlegend(icon_image, n, N, outcome_label, v_pad = 20, bg='white'):
  dim_hor, dim_vert = icon_image.size
  font = ImageFont.truetype('Helvetica', 25)
  # get size from info provided
  message = " ".join([str(n), 'out of', str(N), 'people' , 'experience', outcome_label])
  w,height = font.getsize(message)
  legend_icon_image = Image.new("RGB", (dim_hor, dim_vert+height+v_pad), bg)
  legend_icon_image.paste(icon_image, (0, 0))

  draw = ImageDraw.Draw(legend_icon_image)
  h_offset = (dim_hor/2)-(w/2)
  draw.text((h_offset, dim_vert + v_pad), message, font=font, fill="black")
  del draw
  return legend_icon_image

def addlegends(icon_image, n_s, N, outcome_labels, v_pad = 20, bg='white'):
  for outcome in range(len(outcome_labels)):
    if outcome_labels[outcome] is not '':
      icon_image = addlegend(icon_image, n_s[outcome], N, outcome_labels[outcome], v_pad, bg)
  return icon_image

def addtitle(icon_image, title, v_pad=20, bg='white'):
  dim_hor, dim_vert = icon_image.size
  font = ImageFont.truetype('Helvetica', 64)
  message = str(title)
  w,height = font.getsize(message)
  h_offset = (icon_image.size[0]/2)-(w/2)
  title_height = height+(v_pad*2) # round this?

  titled_icon_image = Image.new("RGB", (dim_hor, (dim_vert+ title_height)), bg)
  titled_icon_image.paste(icon_image, (0, title_height))

  draw = ImageDraw.Draw(titled_icon_image)
  draw.text((h_offset, v_pad), message, font=font, fill="black")
  del draw

  return titled_icon_image

def appendright(left_image, right_image, h_pad=0, bg='white'):
  w_l,h_l = left_image.size
  w_r,h_r = right_image.size
  total_width = w_l + h_pad + w_r
  height = max(h_l,h_r)

  appended_image = Image.new("RGB", (total_width, height), bg)
  appended_image.paste(left_image, (0, height-h_l))
  appended_image.paste(right_image, (w_l+h_pad, height-h_r))

  return appended_image

def geticonshape(shape, dim_horiz, dim_vert):
  iconimage = ''.join([shape, '_icon.png'])
  img = Image.open(iconimage)
  img = ImageOps.grayscale(img)
  img = ImageOps.autocontrast(img)
  img = img.resize((dim_horiz, dim_vert), Image.BILINEAR)
  return img

def drawarrayoficons(numbersofeach, coloured_images, tile_horiz = 10):
  total_N = sum(numbersofeach)
  firstimage = coloured_images[0]
  width = firstimage.size[0]
  height = firstimage.size[1]
  tile_vert = int(math.ceil(total_N/float(tile_horiz))) # round up
  arrayed_image = Image.new("RGB", (width*tile_horiz, height*(tile_vert)), "white")

  numbersofeach = numbersofeach + [tile_horiz] # extra padding if needed

  colindex = []
  for i in range(len(numbersofeach)):
    to_add = [i for number in range(numbersofeach[i])]
    colindex = colindex + to_add
  vertindex = []
  vertrange = range(tile_vert)
  for i in vertrange:
    vertindex.extend([i]*tile_horiz) # need to make long enough
  horindex = range(tile_horiz)*tile_vert

  for counter in range(tile_vert*tile_horiz):
    arrayed_image.paste(coloured_images[colindex[counter]],(horindex[counter]*width, vertindex[counter]*height))

  return arrayed_image

def makecolourediconset(shape, icon_colours, bg):
  coloured_images = []
  for col in icon_colours:
    coloured_images.append(ImageOps.colorize(shape, col, bg))
  coloured_images.append(ImageOps.colorize(shape, bg, bg))
  return coloured_images

def makearray(numbersofeach, icon_colours, outcomes, title = '', dimension=64, dimension_vert=92, n_horiz=10, bg='white', iconshape = 'person' ):
  """this makes an iconarray in PIL format; general case """
  img = geticonshape(iconshape, dimension, dimension_vert)
  coloured_images = makecolourediconset(img, icon_colours, bg)
  out_image = drawarrayoficons(numbersofeach, coloured_images)
  total_N = sum(numbersofeach)
  out_image = addlegends(out_image, numbersofeach, total_N, outcomes)
  if title is not '':
    out_image = addtitle(out_image, title)
  return out_image

def pictogram(numbersofoutcome, icon_colours, outcomes, titles, dimension=64, dimension_vert=92, n_horiz=10, h_pad=20, bg='white', iconshape = 'person' ):
  """make image of one or more pictograms"""

  arrayofnumbers = np.array(numbersofoutcome)
  separate_images = []
  if arrayofnumbers.ndim > 1:
    for each in range(arrayofnumbers.shape[0]):
      separate_images.append(makearray(arrayofnumbers[each,].tolist(), icon_colours, outcomes, titles[each], dimension, dimension_vert, n_horiz, bg, iconshape))
  else:
    separate_images.append(makearray(arrayofnumbers.tolist(), icon_colours, outcomes, titles, dimension, dimension_vert, n_horiz, bg, iconshape))
  # append these
  output_image = separate_images[0]
  if arrayofnumbers.ndim > 1:
    for each in range(arrayofnumbers.shape[0]-1):
      output_image = appendright(output_image, separate_images[each+1], h_pad)
  return output_image

def pictogramNRR(numbersofoutcome, icon_colours, outcomes, titles, dimension=64, dimension_vert=92, n_horiz=10, h_pad=20, bg='white', iconshape = 'person' ):
  """make pictograms for special case where each group presupposes previous group also, for example response and remission rates"""

  arrayofNRR = np.array(numbersofoutcome)
  differences = np.diff(arrayofNRR)*-1
  separate_images = []
  if arrayofNRR.ndim > 1:
    for each in range(arrayofNRR.shape[0]): # this was broken before
      numberstouse = np.append(differences[each,:], arrayofNRR[each,-1]).tolist()
      separate_images.append(makearray(numberstouse, icon_colours, outcomes, titles[each], dimension, dimension_vert, n_horiz, bg, iconshape))
  else:
    numberstouse = np.append(differences, arrayofNRR[-1]).tolist()
    separate_images.append(makearray(numberstouse, icon_colours, outcomes, titles, dimension, dimension_vert, n_horiz, bg, iconshape))
  # append these
  output_image = separate_images[0]
  if arrayofNRR.ndim > 1:
    for each in range(arrayofNRR.shape[0]-1):
      output_image = appendright(output_image, separate_images[each+1], h_pad)

  return output_image

def main():
  complex = pictogram([[2, 58,13,7],[4,6,7,8]], ['red', 'grey', 'green', 'blue'], ['harm', '', 'improvement', 'cure'], ['magic', 'jordan'])
  complex.show()
  morecomplex = pictogramNRR([[100,58,13,7],[100,42,14,2]] , ['grey', 'cyan', 'lightgreen', 'green'], ['', 'slight', 'improvement', 'cure'], ['magic', 'nowt'])
  morecomplex.show()

if __name__ == "__main__":
  main()