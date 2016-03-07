# copyright 2014-2016
# make an array of icons to act as a decision aid
 
import Image, ImageChops, ImageDraw, ImageFont, ImageOps

def addlegend(icon_image, n, N, outcome_label, h_offset, v_offset):
	draw = ImageDraw.Draw(icon_image)
	font = ImageFont.truetype('Helvetica', 25)
	# better to get size from image provided
	dim_vert = icon_image.size[1]
	draw.text((h_offset, dim_vert - v_offset), str(n) + ' out of '\
	 + str(N) + ' people ' + 'experience ' + outcome_label,\
	  font=font, fill="black")
	del draw
	return icon_image
	
def addtitle(icon_image, title, h_offset, v_offset, v_pad):
	titled_icon_image = Image.new("RGB", (icon_image.size[0], icon_image.size[1]+v_pad), "white")
	titled_icon_image.paste(icon_image, (0, v_pad))
	
	# better to centre the text
	
	draw = ImageDraw.Draw(titled_icon_image)
	font = ImageFont.truetype('Helvetica', 64)
	draw.text((h_offset, v_offset), str(title) ,\
	  font=font, fill="black")
	del draw
	
	return titled_icon_image
	
def appendright(left_image, right_image, h_pad, bg='white'):
	
	width = left_image.size[0]
	total_width = width + h_pad + right_image.size[0]
	height = left_image.size[1]
	appended_image = Image.new("RGB", (total_width, height), "white")
	appended_image.paste(left_image, (0, 0))
	appended_image.paste(right_image, (width+h_pad, 0))

	return appended_image

def makeiconarray(n_switch=12, n_switch2 = 6, outcomes=['this outcome', 'other outcome'], dimension=64, dimension_vert=92, n_horiz=10, n_vert=10, iconimage = 'green_icon.png', icon_colours = ['green', 'red']):
	"""this makes an iconarray in PIL format"""
	
	img = Image.open(iconimage)
	img = ImageOps.grayscale(img)
	img = img.resize((dimension,dimension_vert), Image.BILINEAR)
	#img_alt = ImageChops.invert(img)
	img_basic = ImageOps.colorize(ImageOps.autocontrast(img), 'grey', 'white')
	img_alt = ImageOps.colorize(ImageOps.autocontrast(img), icon_colours[0], 'white')
	img_alt2 = ImageOps.colorize(ImageOps.autocontrast(img), icon_colours[1], 'white')

	blank_image = Image.new("RGB", (dimension*n_horiz, dimension_vert*(n_vert+1)), "white")
	counter=n_horiz*n_vert
 
	for vert in range(n_vert):
		for hor in range(n_horiz):
			if counter > n_switch:
				blank_image.paste(img_basic,(hor*dimension, vert*dimension_vert))
			elif counter > n_switch2:
				blank_image.paste(img_alt2,(hor*dimension, vert*dimension_vert))
			else: 	
				blank_image.paste(img_alt,(hor*dimension, vert*dimension_vert))
			counter -= 1
 
	blank_image = addlegend(blank_image, n_switch, n_horiz*n_vert, outcomes[0], dimension, v_offset = 30)
	if n_switch2 > 0:
		blank_image = addlegend(blank_image, n_switch2, n_horiz*n_vert, outcomes[1], dimension, v_offset = 60)
	return blank_image
	
def makepairoficonarrays(n_out1, n_out2, treatments, icon_colours, outcomes):
	icon_image0 = makeiconarray(n_out1[0], n_out2[0], icon_colours = ['green', 'lightgreen'], outcomes = ['response', 'remission'])
	icon_image0 = addtitle(icon_image0, 'active', 268, 20, 92)
	icon_image1 = makeiconarray(n_out1[1], n_out2[1], icon_colours = ['green', 'lightgreen'], outcomes = ['response', 'remission'])
	icon_image1 = addtitle(icon_image1, 'control', 268, 20, 92)
	
	# need to separate with some white space
	
	pair_image = appendright(icon_image0, icon_image1, 40)
	
	return pair_image

def main():
    icon_image = makeiconarray(12, 8, icon_colours = ['green', 'lightgreen'], outcomes = ['response', 'remission'])
    icon_image.show()
    
    pair_image = makepairoficonarrays([12, 7], [8, 3], ['active', 'placebo'], ['green', 'lightgreen'], outcomes = ['response', 'remission'])
    pair_image.show()

if __name__ == "__main__":
    main()
    