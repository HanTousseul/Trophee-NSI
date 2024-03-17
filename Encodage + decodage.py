from PIL import Image

# fonction qui transforme une image en une liste de pixels rgba
def convert_image_pixel(file):
    image = Image.open(file)
    image = image.convert('RGBA')
    liste_pixels = list(image.getdata())
    return liste_pixels

# fonction qui encode un message dans une image
def traitement_image(file, texte):
    liste_binaire=[]
    im = Image.open(file)
    im = im.convert('RGBA')
    w_img = (im.size)[0]
    if len(texte)>((w_img-8)/2):
        return("Le message est trop long pour être encodé dans l'image, veuillez raccourcir votre message ou bien fournir une image ayant une résolution plus élevée")
    # la variable binaire est un string de binaire correspondant au texte donne en argument
    binaire=''.join(format(ord(i), '08b') for i in texte)
    for i in range(len(binaire)):
        # liste_binaire est une liste contenant des strings. chaque string est un nombre en binaire
        liste_binaire.append(int(binaire[i]))
    nb_pixels = len(liste_binaire)//4
    for k in range(nb_pixels):
        # on place les bits en partant du pixel en haut a droite. on incremente de un a un vers la gauche jusqua toucher
        # la limite droite, on revient ensuite a gauche en descendant d'une ligne. donc l'abscisse est de k modulo la
        # largeur de l'image, et l'ordonnee est la division entiere de k par la largeur de l'image.
        coordinate = k % w_img, k//w_img
        tpl = im.getpixel(coordinate)
        couleur = list(tpl)
        couleur_bin = [int((bin(couleur[0]))[2:10]), int((bin(couleur[1]))[2:10]), int((bin(couleur[2]))[2:10]),int((bin(couleur[3]))[2:10])] #couleur_bin est une liste. les valeurs prises sont 'couleur' en binaire, string, auquel on enleve le '0b' du debut(avec un slice), et qu'on reconvertit en string
        for i in range(4):
            if liste_binaire[4*k+i] != couleur_bin[i] % 2:
                couleur_bin[i] = str((couleur_bin[i]//10)*10+liste_binaire[4*k+i])
                couleur_bin[i] = int(couleur_bin[i], 2)
            else:
                couleur_bin[i] = int(str(couleur_bin[i]), 2)
        couleur_bin = tuple(couleur_bin)
        im.putpixel(((k % w_img), (k//w_img)), couleur_bin)
    # la varibale liste_nb_pixels contient la valeur en binaire sur 32 bits du nombre de pixels a decoder
    liste_nb_pixels = list(bin(nb_pixels))
    liste_nb_pixels.pop(0)
    liste_nb_pixels.pop(0)
    liste_nb_pixels.reverse()
    for i in range(len(liste_nb_pixels)):
        liste_nb_pixels[i]=int(liste_nb_pixels[i])
    while len(liste_nb_pixels)<32:
        liste_nb_pixels.append(0)
    # je laisse la liste a l'envers car je vais prendre les pixels en partant du bit de poids faible
    for i in range(8):
        # j'utilise ces operations sur x et y pour que le nombre de pixel stocke soit ecrit meme si l'image fait moins de 8 pixels de large
        x = -1 - i % w_img
        y = -1-i//w_img
        couleur_pixel=list(im.getpixel((x, y)))
        for k in range(1, 5):
            if couleur_pixel[-k]%2==1 and liste_nb_pixels[0]%2==0:
                couleur_pixel[-k]-=1
            elif couleur_pixel[-k]%2==0 and liste_nb_pixels[0]%2==1:
                couleur_pixel[-k]+=1
            del(liste_nb_pixels[0])
        im.putpixel([x, y], tuple(couleur_pixel))
    im.show()
    n_file=str(file)
    name=''
    i=0
    while n_file[i]!='.':
        name+=n_file[i]
        i+=1
    name+=' (encodé).png'
    im.save(name)
# fonction qui decode le nombre de pixels utilises dans l'encodage


def nb_pixels_encodes(image):
    # recuperer la liste des pixels rgba decimal d'une image
    liste_pixels = convert_image_pixel(image)
    # initialiser une liste qui va contenir les bits necessaires pour avoir
    # le nombre de pixels utilises dans l'encodage (a l'envers)
    liste_bit = []
    for i in range(1, 9):
        for k in range(1, 5):
            bit = liste_pixels[-i][-k] % 2
            liste_bit.append(bit)
    # remettre la liste des bits a l'endroit
    liste_bit.reverse()
    # transformer la liste en une chaine de caractere
    nombre_bin = ''
    for bit in liste_bit:
        nombre_bin += str(bit)
    # transformer le nombre de pixel en decimal
    nombre_pixels_utilises = int(nombre_bin, 2)
    return nombre_pixels_utilises


# fonction qui decode le message cache dans l'image
def decodage(image):
    # liste des pixels (en rgba) qui constituent l'image
    liste_pixels_rgba = convert_image_pixel(image)
    # nombre de pixels utilises pour encoder le messsage
    nb_pixels = nb_pixels_encodes(image)
    # initialiser une liste qui contient les bits necessaires pour le decodage
    message_bin = []
    # recuperer les bits necessaires pour le decodage
    for i in range(nb_pixels):
        for k in range(4):
            bit = liste_pixels_rgba[i][k] % 2
            message_bin.append(bit)
    # initialiser une nouvelle liste qui va contenir les bits regroupes en 8
    message_bin_8 = []
    while len(message_bin) > 0:
        lettre_bin = ''
        for i in range(8):
            lettre_bin += str(message_bin[i])
        message_bin_8.append(lettre_bin)
        del message_bin[0:8]
    # initialiser une nouvelle liste qui va contenir les nombres decimaux correspondant a chaque caractere
    message_ascii = []
    for bits8 in message_bin_8:
        message_ascii.append(int(bits8, 2))
    # initialiser une nouvelle liste qui va contenir les caracteres du message encodes
    message_unicode = []
    for nbr in message_ascii:
        message_unicode.append(chr(nbr))
    # transformer la liste en une chaine de caractere
    message = ''
    for caractere in message_unicode:
        message += caractere
    return message


# programme principal
traitement_image('image groupe.jpg', 'On est les gagnants')
print(decodage('image groupe (encodé).png'))
