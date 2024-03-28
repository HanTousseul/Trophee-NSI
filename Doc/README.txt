EnigmaPic est le nom de notre projet en vue du concours 'Trophée NSI'. 
Il est recommandé d'utiliser le système d'exploitation Windows si vous désirez utiliser l'interface graphique.
Le code marchera sur macOS uniquement si vous passez par le fichier 'EnigmaPic (Fonctions).py'. 
Pour le protocole d'utilisation, il y'a deux options;
-   Soit vous passez par le fichier 'EnigmaPic (Interface graphique).py', auquel cas, il suffit d'éxecuter le code, et de suivre les instructions de l'interface graphique de Tkinter
-   Soit vous passez par le fichier 'EnigmaPic (Fonctions).py', auquel cas il faut appeler les fonctions: 
        La 1ère: 'encodage' prend en argument le chemin absolu de l'image, et le message à encoder, et enregistre la nouvelle image encodée dans le même dossier que l'image passée en argument
        La 2ème: 'decodage' prend en argument le chemin absolu de l'image à décoder et renvoie le message caché dedans.

P.S: Nous avons constaté que lorsqu'on copie un chemin sur Windows, il sépare les dossiers de l'arborescence avec des '\'. Or, les nouvelles version de Python interprètent ce signe comme étant un 'linebreak', ou un retour à la ligne. La solution la plus simple que l'on a trouvé est de remplacer les '\' par des '/'. Par ailleurs, il faut également penser à retirer le nom du disque au début du chemin par exemple: le chemin 
'C:\Users\utilisateur\Desktop\VS Code\Trophee NSI\Trophee-NSI\Images\image.jpg' devient 
'/Users/marca/Desktop/VS Code/Trophee NSI/Trophee-NSI/Images/image.jpg'