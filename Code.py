from PIL import Image
def traitement_image(texte):
    liste_binaire=[]
    #on doit trouver une facon de stocker la photo de maniere "universelle" i.e que ca marche partout
    im=Image.open(r'C:\Users\marca\Desktop\VS Code\Trophee NSI\IMG_4939.png')
    #join() sert a concatener des strings, format converit du ASCII en binaire et ord convertit le Unicode en ASCII
    w_img=(im.size)[0]
    h_img=(im.size)[1]
    binaire=''.join(format(ord(i), '08b') for i in texte)#la variable binaire est un string de binaire correspondant au texte donne en argument
    for i in range(2,len(binaire),3):
        liste_binaire.append((binaire[i-2].join(binaire[i-1].join(binaire[i])))) #liste_binaire est une liste qui contient des strings de trois bits chacun, pour pouvoir les incorporer a l'image
    restant=len(binaire)%3
    for k in range(len(liste_binaire)):
        coordinate = x, y = k % w_img,k//w_img
        tpl=im.getpixel(coordinate)
        couleur=list(tpl)
        couleur_bin=[bin(couleur[0]),bin(couleur[1]),bin(couleur[2])]
        str_0= couleur_bin[0]-couleur_bin[0]%1000+liste_binaire[k]
        im.putpixel((k % w_img),(k//w_img))
    im.show

traitement_image('bonjour')