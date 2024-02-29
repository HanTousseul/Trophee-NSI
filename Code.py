from PIL import Image
def traitement_image(texte):
    liste_binaire=[]
    liste_valeurs=[] #liste_valeurs sert a verifier que les valeurs ont ete modifiees correctement
    #on doit trouver une facon de stocker la photo de maniere "universelle" i.e que ca marche partout
    im=Image.open(r'C:\Users\marca\Desktop\VS Code\Trophee NSI\IMG_4939.png')
    im=im.convert('RGBA')
    #join() sert a concatener des strings, .format() convertit du ASCII en binaire et ord convertit le Unicode en ASCII
    w_img=(im.size)[0]
    h_img=(im.size)[1]
    binaire=''.join(format(ord(i), '08b') for i in texte)#la variable binaire est un string de binaire correspondant au texte donne en argument
    for i in range(len(binaire)):
        liste_binaire.append(int(binaire[i])) #liste_binaire est une liste contenant des strings. chaque string est un nombre en binaire 
    nb_pixels=len(liste_binaire)//4
    leftovers=len(liste_binaire)%4
    for k in range(nb_pixels):
        coordinate = x, y = k % w_img,k//w_img # on place les bits en partant du pixel en haut a droite. on incremente de un a un vers la gauche jusqua toucher la limite droite, on revient ensuite a gauche en descendant d'une ligne. donc l'abscisse est de k modulo la largeur de l'image, et l'ordonnee est la division entiere de k par la largeur de l'image.
        tpl=im.getpixel(coordinate)
        couleur=list(tpl)
        couleur_bin=[int((bin(couleur[0]))[2:10]),int((bin(couleur[1]))[2:10]),int((bin(couleur[2]))[2:10]),int((bin(couleur[3]))[2:10])] #couleur_bin est une liste. les valeurs prises sont 'couleur' en binaire, string, auquel on enleve le '0b' du debut(avec un slice), et qu'on reconvertit en string
        for i in range(4):
            if liste_binaire[4*k+i] != couleur_bin[i]%2:
                couleur_bin[i]=(couleur_bin[i]//10)*10+liste_binaire[4*k+i]
        couleur_bin=tuple(couleur_bin)
        im.putpixel(((k % w_img),(k//w_img)),couleur_bin)
        liste_valeurs.append(couleur_bin)
    im.show()
traitement_image('bonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjourbonjour')