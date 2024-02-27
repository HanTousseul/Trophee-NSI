from PIL import Image
im=Image.open('/workspaces/Trophee-NSI/IMG_4939.png')
px=im.load()
coordinate = (1,1) 
#print (im.getpixel(coordinate))
for i in range(30):
    for k in range(30):
        im.putpixel((i,k),(0,0,0))
im.show