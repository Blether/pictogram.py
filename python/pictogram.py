# copyright 2014-2016
# make an array of icons to act as a decision aid
 
import Image, ImageChops, ImageDraw, ImageFont, ImageOps

def makeiconarray(n_switch=7, the_outcome='this outcome', dimension=64, dimension_vert=92, n_horiz=10, n_vert=10):
	"""this makes an iconarray in PIL format"""
	img = Image.open('green_icon.png')
	img=ImageOps.grayscale(img)
	img = img.resize((dimension,dimension_vert), Image.BILINEAR)
	#img_alt = ImageChops.invert(img)
	img_alt = Image.open('red_icon.png')
	img_alt = img_alt.resize((dimension,dimension_vert), Image.BILINEAR)
 
	blank_image = Image.new("RGB", (dimension*n_horiz, dimension_vert*(n_vert+1)), "white")
	counter=n_horiz*n_vert
 
	for vert in range(n_vert):
		for hor in range(n_horiz):
			if counter > n_switch:
				blank_image.paste(img,(hor*dimension, vert*dimension_vert))
			else: 	
				blank_image.paste(img_alt,(hor*dimension, vert*dimension_vert))
			counter -= 1
 
	draw = ImageDraw.Draw(blank_image)
	font = ImageFont.truetype('Helvetica', 25)
	draw.text((dimension, 20 + dimension_vert*n_vert), str(n_switch) + ' out of '\
	 + str(n_horiz*n_vert) + ' people ' + 'experience ' + the_outcome,\
	  font=font, fill="black")
	del draw
	return blank_image

icon_image = makeiconarray()
icon_image.show()
