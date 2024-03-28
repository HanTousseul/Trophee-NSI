from tkinter import *
from tkinter import filedialog
from PIL import Image
from random import*


# fonction qui va verifier les coordonnees du pixel que l'on tente d'occuper. si celles-ci depassent le bord de l'image ou si cet emplacement est deja occupe, on en genere un nouveau
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
    # verifie que le message peut etre encrypter dans la photo
    if len(texte)>((w_img*h_img)//3):
        return False
    # la variable binaire est un string de binaire correspondant au texte donne en argument
    else:
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
        return im

# fontion qui transforme un string contenant un nombre binaire en un entier decimal
def bin_a_dec(binaire):
    Lbinaire=list(binaire)
    Lbinaire.reverse()
    decimal=0
    for i in range(len(Lbinaire)):
        decimal += int(Lbinaire[i])*2**i
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


# programmation de tkinter
window = Tk()
window.title('EnigmaPic')
window.geometry('1000x600+100+10')
window.resizable(False, False)
window.configure(bg='dark blue')


def button_encryptage_click():
    label_titre.place_forget()
    label_desc.place_forget()
    button_decryptage.place_forget()
    button_encryptage.place_forget()
    label_titre_encryptage.place(x=335, y=40)
    label_texte_encryptage.place(x=171, y=130)
    label_texte_image_encryptage.place(x=50, y=220)
    button_encryptage_encryptage.place(x=160, y=350)
    button_retour.place(x=50, y=500)
    button_retour.configure(text='Retour', width='10', command=button_retour_click1)


def button_decryptage_click():
    label_titre.place_forget()
    label_desc.place_forget()
    button_decryptage.place_forget()
    button_encryptage.place_forget()
    label_titre_decryptage.place(x=335, y=40)
    label_texte_decryptage.place(x=171, y=130)
    label_texte_image_decryptage.place(x=50, y=220)
    button_decryptage_decryptage.place(x=160, y=350)
    button_retour.place(x=50, y=500)
    button_retour.configure(text='Retour', width='10', command=retour_decryptage)


def imageUploader():
    from PIL import Image, ImageTk
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    global path
    global x
    global y
    path = filedialog.askopenfilename(filetypes=fileTypes)
    img = Image.open(path)
    size_img = img.size
    img_ratio = round(size_img[1] / size_img[0], 1)
    longueur = 350
    largeur = int(350 * img_ratio)
    x = 600
    y = 210
    if largeur > 390:
        largeur = 395
        longueur = int(round(395 / img_ratio))
        x = 650
        y = 190
    elif largeur < 250:
        y = 250
    img = img.resize((longueur, largeur))
    pic = ImageTk.PhotoImage(img)
    label_image.configure(image=pic)
    label_image.image = pic
    label_image.place(x=x, y=y)
    button_selectionner.place(x=350, y=500)


def imageUploader_decryptage():
    from PIL import Image, ImageTk
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    global path
    path = filedialog.askopenfilename(filetypes=fileTypes)
    img = Image.open(path)
    size_img = img.size
    img_ratio = round(size_img[1] / size_img[0], 1)
    longueur = 350
    largeur = int(350 * img_ratio)
    x = 600
    y = 210
    if largeur > 390:
        largeur = 395
        longueur = int(round(395 / img_ratio))
        x = 650
        y = 190
    elif largeur < 250:
        y = 250
    img = img.resize((longueur, largeur))
    pic = ImageTk.PhotoImage(img)
    label_image.configure(image=pic)
    label_image.image = pic
    label_image.place(x=x, y=y)
    button_selectionner_decryptage.place(x=350, y=500)


def button_retour_click2():
    global x
    global y
    label_texte_message_encryptage.place_forget()
    message_encryptage.place_forget()
    button_entrer.place_forget()
    label_titre_encryptage.place(x=335, y=40)
    label_texte_encryptage.place(x=171, y=130)
    label_texte_image_encryptage.place(x=50, y=220)
    button_encryptage_encryptage.place(x=160, y=350)
    label_image.place(x=x, y=y)
    button_selectionner.place(x=350, y=500)
    button_retour.configure(command=button_retour_click1)
    label_erreur2.place_forget()


def button_retour_click1():
    label_titre.place(x=50, y=40)
    label_desc.place(x=70, y=130)
    button_encryptage.place(x=120, y=350)
    button_decryptage.place(x=550, y=350)
    label_titre_encryptage.place_forget()
    label_texte_encryptage.place_forget()
    label_texte_image_encryptage.place_forget()
    button_encryptage_encryptage.place_forget()
    button_retour.place_forget()
    label_image.place_forget()
    button_selectionner.place_forget()
    label_image2.place_forget()
    label_resultat.place_forget()
    button_telecharger.place_forget()


def retour_decryptage():
    label_titre_decryptage.place_forget()
    label_texte_decryptage.place_forget()
    label_texte_image_decryptage.place_forget()
    button_decryptage_decryptage.place_forget()
    label_image.place_forget()
    button_selectionner_decryptage.place_forget()
    button_retour.place_forget()
    label_titre.place(x=50, y=40)
    label_desc.place(x=70, y=130)
    button_encryptage.place(x=120, y=350)
    button_decryptage.place(x=550, y=350)


def retour_menu_principal_decryptage():
    label_titre.place(x=50, y=40)
    label_desc.place(x=70, y=130)
    button_encryptage.place(x=120, y=350)
    button_decryptage.place(x=550, y=350)
    label_texte_message_decryptage.place_forget()
    label_titre_decryptage.place_forget()
    label_texte_decryptage.place_forget()
    label_resultat_final.place_forget()
    label_image.place_forget()
    button_retour.place_forget()
    label_erreur.place_forget()
    button_copier.place_forget()


def button_selectionner_click():
    label_texte_message_encryptage.place(x=50, y=220)
    message_encryptage.place(x=100, y=300)
    button_entrer.place(x=800, y=500)
    label_texte_image_encryptage.place_forget()
    button_encryptage_encryptage.place_forget()
    label_image.place_forget()
    button_selectionner.place_forget()
    button_retour.configure(command=button_retour_click2)
    message_encryptage.delete(0, END)


def button_selectionner_click_decryptage():
    global path
    global image
    button_retour.configure(text='Menu Principal', width='13', command=retour_menu_principal_decryptage)
    label_texte_image_decryptage.place_forget()
    button_decryptage_decryptage.place_forget()
    label_image.place_forget()
    button_selectionner_decryptage.place_forget()
    message_final_encryp = decodage(path)
    if message_final_encryp == False:
        label_erreur.place(x=50, y=280)
    else:
        global message_copier
        message_copier = message_final_encryp
        button_copier.place(x=700, y=500)
        label_texte_message_decryptage.place(x=50, y=200)
        if len(message_final_encryp) < 34:
            label_resultat_final.configure(text="'" + message_final_encryp + "'", font=('Century Schoolbook L', 40, 'bold'),
                                           bg='dark blue', fg='white')
        elif len(message_final_encryp)<100:
            message_liste = list(message_final_encryp)
            message2 = []
            while len(message_liste) > 0:
                message_liste_petit = message_liste[0:34]
                message = ''.join(message_liste_petit)
                message2.append(message)
                message2.append('\n')
                for i in range(min(34, len(message_liste))):
                    del message_liste[0]
            message3 = message2[0:-1]
            message4 = ''.join(message3)
            label_resultat_final.configure(text="'" + message4 + "'",
                                           font=('Century Schoolbook L', 40, 'bold'),
                                           bg='dark blue', fg='white')
        elif len(message_final_encryp)<434 :
            message_liste = list(message_final_encryp)
            message2 = []
            while len(message_liste) > 0:
                message_liste_petit = message_liste[0:62]
                message = ''.join(message_liste_petit)
                message2.append(message)
                message2.append('\n')
                for i in range(min(62, len(message_liste))):
                    del message_liste[0]
            message3 = message2[0:-1]
            message4 = ''.join(message3)
            label_resultat_final.configure(text="'" + message4 + "'",
                                           font=('Century Schoolbook L', 20, 'bold'),
                                           bg='dark blue', fg='white')
        elif len(message_final_encryp)<888:
            message_liste = list(message_final_encryp)
            message2 = []
            while len(message_liste) > 0:
                message_liste_petit = message_liste[0:90]
                message = ''.join(message_liste_petit)
                message2.append(message)
                message2.append('\n')
                for i in range(min(90, len(message_liste))):
                    del message_liste[0]
            message3 = message2[0:-1]
            message4 = ''.join(message3)
            label_resultat_final.configure(text="'" + message4 + "'",
                                           font=('Century Schoolbook L', 15, 'bold'),
                                           bg='dark blue', fg='white')
        else :
            message_liste = list(message_final_encryp)
            message2 = []
            while len(message_liste) > 0:
                message_liste_petit = message_liste[0:134]
                message = ''.join(message_liste_petit)
                message2.append(message)
                message2.append('\n')
                for i in range(min(134, len(message_liste))):
                    del message_liste[0]
            message3 = message2[0:-1]
            message4 = ''.join(message3)
            label_resultat_final.configure(text="'" + message4 + "'",
                                           font=('Century Schoolbook L', 10, 'bold'),
                                           bg='dark blue', fg='white')
        label_resultat_final.place(x=15, y=260)


def button_entrer_click():
    from PIL import ImageTk
    global message
    global path
    global image
    message = message_encryptage.get()
    try:
        image = encodage(path, message)
        size_img = image.size
    except:
        label_erreur2.place(x=30, y=370)
    else:
        img_ratio = round(size_img[1] / size_img[0], 1)
        longueur = 350
        largeur = int(350 * img_ratio)
        x = 600
        y = 210
        if largeur > 395:
            largeur = 395
            longueur = int(round(395 / img_ratio))
            x = 650
            y = 190
        elif largeur < 250:
            y = 250
        im = image.resize((longueur, largeur))
        pic2 = ImageTk.PhotoImage(im)
        label_image2.configure(image=pic2)
        label_image2.image = pic2
        label_image2.place(x=x, y=y)
        label_texte_message_encryptage.place_forget()
        message_encryptage.place_forget()
        button_entrer.place_forget()
        button_retour.configure(text='Menu Principal', width='13', command=button_retour_click1)
        label_resultat.place(x=50, y=220)
        button_telecharger.place(x=190, y=350)
        label_erreur2.place_forget()


def telecharger():
    global image
    global name
    fileTypes = [("Image files", "*.png")]
    path2 = filedialog.asksaveasfilename(filetypes=fileTypes, defaultextension=".png", initialfile='image encodee.png')
    image.save(path2)


def copier():
    global message_copier
    window.clipboard_clear()
    window.clipboard_append(message_copier)
    window.update()


# page 1
label_titre = Label(window, text='Bienvenue dans EnigmaPic !', font=('Century Schoolbook L', 50, 'bold'),
                    bg='dark blue', fg='white')
label_titre.place(x=50, y=40)

label_desc = Label(window,
                   text="Ici, vous pourrez encrypter des messages dans des images,\nafin d'envoyer ce que vous désirez à quelqu'un sans laisser aucune trace !",
                   font=('Century Schoolbook L', 20), bg='dark blue', fg='white')
label_desc.place(x=70, y=130)

button_encryptage = Button(window, text="Encryptage\nd'une image", font=('Century Schoolbook L', 25), width='18',
                           height='2', bg='grey', fg='white', command=button_encryptage_click)
button_encryptage.place(x=120, y=350)

button_decryptage = Button(window, text="Décryptage\nd'une image", font=('Century Schoolbook L', 25), width='18',
                           height='2', bg='grey', fg='white', command=button_decryptage_click)
button_decryptage.place(x=550, y=350)

# page 2
label_titre_encryptage = Label(window, text='Encryptage', font=('Century Schoolbook L', 50, 'bold'),
                               bg='dark blue', fg='white')

label_texte_encryptage = Label(window, text="Ici, vous pouvez dissimuler un message dans votre image.",
                               font=('Century Schoolbook L', 20), bg='dark blue', fg='white')

label_texte_image_encryptage = Label(window,
                                     text="Sélectionnez d'abord l'image dans\nlaquelle sera encodé le message :",
                                     font=('Century Schoolbook L', 25, 'underline'), bg='dark blue', fg='white',
                                     justify='left')

button_encryptage_encryptage = Button(window, text="Choisir un fichier", font=('Century Schoolbook L', 20), width='15',
                                      height='1', bg='grey', fg='white', command=imageUploader)

label_image = Label(window)

button_retour = Button(window, text='Retour', font=('Century Schoolbook L', 20), width='10',
                       height='1', bg='grey', fg='white', command=button_retour_click1)

button_selectionner = Button(window, text='Sélectionner', font=('Century Schoolbook L', 20), width='13',
                             height='1', bg='green', fg='white', command=button_selectionner_click)

# page 3
label_texte_message_encryptage = Label(window, text="Entrez le message à encoder dans l'image :",
                                       font=('Century Schoolbook L', 25, 'underline'), bg='dark blue', fg='white')

message_encryptage = Entry(window, font=('Century Schoolbook L', 20), justify='left', fg='black',
                           borderwidth='2', width=50)

button_entrer = Button(window, text='Entrer', font=('Century Schoolbook L', 20), width='10',
                       height='1', bg='green', fg='white', command=button_entrer_click)

label_erreur2 = Label(window, text="Le message est trop long pour être encodé dans l'image, veuillez raccourcir votre\nmessage ou bien fournir une image ayant une résolution plus élevée.",
                     font=('Century Schoolbook L', 18, 'bold'), bg='dark blue', fg='red')

# page 4
label_resultat = Label(window, text="Voici votre image encodée !",
                       font=('Century Schoolbook L', 25, 'underline'), bg='dark blue', fg='white')

button_telecharger = Button(window, text="Télécharger l'image", font=('Century Schoolbook L', 20), width='18',
                            height='1', bg='grey', fg='white', command=telecharger)

label_image2 = Label(window)

# page 5
label_titre_decryptage = Label(window, text='Décryptage', font=('Century Schoolbook L', 50, 'bold'),
                               bg='dark blue', fg='white')

label_texte_decryptage = Label(window, text="Ici, vous pouvez lire le message caché de votre image.",
                               font=('Century Schoolbook L', 20), bg='dark blue', fg='white')

label_texte_image_decryptage = Label(window, text="Sélectionnez l'image que\nvous voulez décrytper :",
                                     font=('Century Schoolbook L', 25, 'underline'), bg='dark blue', fg='white',
                                     justify='left')

button_decryptage_decryptage = Button(window, text="Choisir un fichier", font=('Century Schoolbook L', 20), width='15',
                                      height='1', bg='grey', fg='white', command=imageUploader_decryptage)


button_selectionner_decryptage = Button(window, text='Sélectionner', font=('Century Schoolbook L', 20), width='13',
                                        height='1', bg='green', fg='white',
                                        command=button_selectionner_click_decryptage)

label_image = Label(window)

# page 6
label_texte_message_decryptage = Label(window, text="Le message encodé est :",
                                       font=('Century Schoolbook L', 25, 'underline'), bg='dark blue', fg='white')

label_resultat_final = Label(window)

label_erreur = Label(window, text="Il n'y a pas de message encodé dans cette photo.\nVeuillez en sélectionner une autre.",
                     font=('Century Schoolbook L', 30, 'bold'), bg='dark blue', fg='red')

button_copier = Button(window, text='Copier le message', font=('Century Schoolbook L', 20), width='15',
                        height='1', bg='grey', fg='white', command=copier)

window.mainloop()
