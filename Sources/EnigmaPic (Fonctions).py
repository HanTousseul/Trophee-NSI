from PIL import Image
from random import*

#fonction qui va verifier les coordonnees du pixel que l'on tente d'occuper. si celles-ci depassent le bord de l'image ou si cet emplacement est deja occupe, on en genere un nouveau
def verification_coords(coordx, coordy, w_img, h_img, coord_occ):
    while coordx>=w_img:
        coordx-=w_img
        coordy+=1
    if coordy>=h_img:
        coordy=0
    while (coordx,coordy) in coord_occ:
        coordx=coordx+1
        if coordx>=w_img:
            coordx=0
            coordy+=1
            if coordy>=h_img:
                coordy=0
    return coordx, coordy

# fonction qui encode un message dans une image
def encodage(file, texte):
    '''
    la fonction encodage prend en argument un string nommé file et un string nommé texte, elle va ensuite encoder le texte dans l'image de type png ou jpg dont le chemin est donné dans file. Si l'image est dans le même dossier que le code, le nom de l'image suffira
    ______________________________________
    file: str
    texte: str
    '''
    im = Image.open(file)
    im = im.convert('RGBA')
    w_img = (im.size)[0]
    h_img = (im.size)[1]
    if len(texte)>((w_img*h_img)//3):
        return("Le message est trop long pour être encodé dans l'image, veuillez raccourcir votre message ou bien fournir une image ayant une résolution plus élevée")
    # la variable binaire est un string de binaire correspondant au texte donne en argument
    binaire=''.join(format(ord(i), '08b') for i in texte)
    liste_binaire=[int(i) for i in binaire]
        # liste_binaire est une liste contenant des entier. chaque entier est un bit en binaire
    nb_lettres = len(liste_binaire)//8
    coord_occ=[] #cette liste va contenir les coordonnées de tout les pixels qui sont deja occupés (c'est a dire que le code ne doit pas modifier)
    nb_pixels_morts=(w_img*h_img)%3 #calculer le nombre de pixels qui ne font pas partie d'un trio pour les exclure
    if nb_pixels_morts>0:
        coord_occ.append((w_img-1,h_img-1))
        if nb_pixels_morts>1:
            coord_occ.append((w_img-2,h_img-1))
    coordx= 0 #initialisation des coordonnées
    coordy= 0
    for k in range(nb_lettres):
        for z in range(3): #forme les groupe de trios: 2 pixels encodent la lettre et le 3eme le saut
            if z!=0: #increment les coordonnées
                coordx+=1
            if coordx>=w_img: #verification que les coordonnées sont dans l'image
                coordx=0
                coordy+=1
                if coordy>=h_img:
                    coordy=0
            tpl = im.getpixel((coordx,coordy))
            couleur = list(tpl)
            couleur_bin = [int(dec_a_bin(couleur[0])), int(dec_a_bin(couleur[1])), int(dec_a_bin(couleur[2])),int(dec_a_bin(couleur[3]))] #couleur_bin est une liste. les valeurs prises sont 'couleur' en binaire, string, et qu'on reconvertit en entier            
            if z==2: #encode le saut
                saut=randint(1,15)
                sautbin='{:04b}'.format(saut)
                listesautbin=[int(m) for m in sautbin]
                if k==nb_lettres-1: #on est arrivés a la derniere lettre, on encode alors un saut de 0 pour que le programme de decodage sache quand s'arreter
                    saut=0
                    listesautbin=[0 for _ in range(4)]
                for i in range(4):
                    if listesautbin[i] != couleur_bin[i] % 2:
                        couleur_bin[i] = str((couleur_bin[i]//10)*10+listesautbin[i])
                        couleur_bin[i] = int(couleur_bin[i], 2)
                    else:
                        couleur_bin[i]=int(str(couleur_bin[i]), 2)
            else: #encode la lettre
                for i in range(4):
                    if liste_binaire[4*(2*k+z)+i] != couleur_bin[i] % 2:
                        couleur_bin[i] = str((couleur_bin[i]//10)*10+liste_binaire[4*(2*k+z)+i])
                        couleur_bin[i] = int(couleur_bin[i], 2)
                    else:
                        couleur_bin[i] = int(str(couleur_bin[i]), 2)
            coord_occ.append((coordx,coordy)) #indique qu'une coordonnées est désormais occupée
            couleur_bin = tuple(couleur_bin)
            im.putpixel((coordx, coordy), couleur_bin) #modifie le pixel
            if z==2 and saut!=0: #prend en compte le saut pour placer le prochain trio
                coordx+=(saut-1)*3+1
                old_coordy=coordy
                coordx,coordy= verification_coords(coordx, coordy, w_img, h_img, coord_occ)
                if coordy<old_coordy:
                    coordx,coordy=0,0
                    coordx,coordy=verification_coords(coordx, coordy, w_img, h_img, coord_occ)
    n_file=str(file)
    name='' #initialise le nom du ficher
    i=0
    while n_file[i]!='.':
        name+=n_file[i]
        i+=1
    name+=' (encodé).png' 
    im.save(name)
    return im

#fontion qui transforme un string contenant un nombre binaire en un entier décimal
def bin_a_dec(binaire):
    Lbinaire=list(binaire)
    Lbinaire.reverse()
    decimal=0
    for i in range(len(Lbinaire)):
        decimal+=int(Lbinaire[i])*2**i
    return decimal

#fonction qui transforme un entier décimal entre 0 et 255 en nombre binaire composé de 8 bits
def dec_a_bin(decimal):
    binaire=''
    while decimal>0:
        binaire=str(decimal%2)+binaire
        decimal=decimal//2
    while len(binaire)<8:
        binaire='0'+binaire
    return binaire

# fonction qui decode le message cache dans l'image
def decodage(image):
    '''
    La fonction décodage prend en argument un le chemin d'une image (encodée en utilisant la fonction 'encodage', elle est donc de format .png) et renvoie le message encodé dedans. De même, si l'image est dans le même dossier que le code, son nom suffira, dans le cas contraire, merci de fournir son chemin absolu entre guillemets
    __________________________________
    image: str
    '''
    im = Image.open(image)
    im = im.convert('RGBA')
    w_img = (im.size)[0]
    h_img = (im.size)[1]
    saut=15
    coordx=0
    coordy=0
    coord_occ=[]
    nb_pixels_morts=(w_img*h_img)%3
    if nb_pixels_morts>0:
        coord_occ.append((w_img-1,h_img-1))
        if nb_pixels_morts>1:
            coord_occ.append((w_img-2,h_img-1))
    message_bin=[]
    while saut!=0:
        for z in range(3):
            if z!=0:
                coordx+=1
            if coordx>=w_img:
                coordx=0
                coordy+=1
                if coordy>=h_img:
                    coordy=0
            tpl = im.getpixel((coordx,coordy))
            couleur = list(tpl)
            bits = [str(couleur[0]%2), str(couleur[1]%2), str(couleur[2]%2), str(couleur[3]%2)]
            if z==2:
                bits_str=''.join(bits)
                saut=bin_a_dec(bits_str)
            else:
                for m in bits:
                    message_bin.append(m)
            coord_occ.append((coordx,coordy))
            if z==2 and saut!=0:
                coordx+=(saut-1)*3+1
                old_coordy=coordy
                coordx,coordy= verification_coords(coordx, coordy, w_img, h_img, coord_occ)
                if coordy<old_coordy:
                    coordx,coordy=0,0
                    coordx,coordy=verification_coords(coordx, coordy, w_img, h_img, coord_occ)
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