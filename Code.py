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
        elt=(binaire[i-2]+(binaire[i-1]+(binaire[i])))
        elt.replace(" ", "")
        liste_binaire.append(elt) #liste_binaire est une liste qui contient des strings de trois bits chacun, pour pouvoir les incorporer a l'image
    restant=len(binaire)%3
    #la boucle if ici sert a rajouter les valeurs qui n'ont peut-etre pas ete prises par la boucle for parce qu'elle avance de 3 en 3. il faudra voir si on ajoute les bits au debut ou a la fin du dernier string
    if restant==1:
        liste_binaire.append('00'+binaire[-1])
    elif restant==2:
        liste_binaire.append('0'+binaire[-2]+binaire[-1])
    print(liste_binaire)
    for k in range(len(liste_binaire)):
        coordinate = x, y = k % w_img,k//w_img
        tpl=im.getpixel(coordinate)
        couleur=list(tpl)
        couleur_bin=[int((bin(couleur[0]))[2:10]),int((bin(couleur[1]))[2:10]),int((bin(couleur[2]))[2:10])] #couleur_bin est une liste. les valeurs prises sont 'couleur' en binaire, string, auquel on enleve le '0b' du debut, et qu'on reconvertit en string
        #print('liste binaire',liste_binaire[k],'couleur_bin 0',couleur_bin[0],'couleur_bin_%1000',couleur_bin[0]-couleur_bin[0]%1000)
        str_0= couleur_bin[0]-couleur_bin[0]%1000+liste_binaire[k]
        im.putpixel((k % w_img),(k//w_img))
    im.show

traitement_image('bonjour')