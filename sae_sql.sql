DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS jean;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS coupe_jean;
DROP TABLE IF EXISTS taille;


CREATE TABLE taille(
   id_taille INT AUTO_INCREMENT,
   nom_taille VARCHAR(50),
   PRIMARY KEY(id_taille)
);

CREATE TABLE coupe_jean(
   id_coupe_jean INT AUTO_INCREMENT,
   nom_coupe VARCHAR(50),
   PRIMARY KEY(id_coupe_jean)
);

CREATE TABLE utilisateur(
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(50),
   email VARCHAR(50),
   nom VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(50),
   est_actif VARCHAR(1),
   PRIMARY KEY(id_utilisateur)
);
CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(id_etat)
);

CREATE TABLE jean(
   id_jean INT AUTO_INCREMENT,
   nom_jean VARCHAR(50),
   prix_jean DECIMAL(5,2),
   matiere VARCHAR(50),
   couleur VARCHAR(50),
   description TEXT,
   marque VARCHAR(50),
   fournisseur VARCHAR(50),
    photo VARCHAR(255),
   taille_id INT NOT NULL,
   coupe_jean_id INT NOT NULL,
   PRIMARY KEY(id_jean),
   CONSTRAINT fk_jean_taille FOREIGN KEY(taille_id) REFERENCES taille(id_taille),
   CONSTRAINT fk_jean_coupe FOREIGN KEY(coupe_jean_id) REFERENCES coupe_jean(id_coupe_jean)
);

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   utilisateur_id INT NOT NULL,
   etat_id INT NOT NULL,
   PRIMARY KEY(id_commande),
   CONSTRAINT fk_commande_utilisateur FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   CONSTRAINT fk_commande_etat FOREIGN KEY(etat_id) REFERENCES etat(id_etat)
);

CREATE TABLE ligne_commande(
   jean_id INT,
   commande_id INT,
   prix DECIMAL(5,2),
   quantite_commande INT,
   PRIMARY KEY(jean_id, commande_id),
   CONSTRAINT fk_ligne_commande_jean FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
   CONSTRAINT fk_ligne_commande_commande FOREIGN KEY(commande_id) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
   jean_id INT,
   utilisateur_id INT,
   quantite_panier INT,
   date_ajout DATE,
   PRIMARY KEY(jean_id, utilisateur_id),
   CONSTRAINT fk_ligne_panier_jean FOREIGN KEY(jean_id) REFERENCES jean(id_jean),
   CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);


INSERT INTO etat VALUES(null, "en attente") ;
INSERT INTO etat VALUES(null, "expédié") ;
INSERT INTO etat VALUES(null, "validé") ;
INSERT INTO etat VALUES(null, "confirmé") ;

INSERT INTO taille(id_taille, nom_taille) VALUES
(NULL, 'W29'),
(NULL, 'W30'),
(NULL, 'W32'),
(NULL, 'W34'),
(NULL, 'W38');

INSERT INTO coupe_jean(id_coupe_jean, nom_coupe) VALUES
(NULL, 'slim'),
(NULL, 'droit'),
(NULL, 'large'),
(NULL, 'ajuste');

INSERT INTO jean(id_jean, nom_jean, prix_jean, matiere, couleur, description, marque, fournisseur, photo, taille_id, coupe_jean_id) VALUES
(NULL, 'jean Xantia ', '45', 'coton','blanc', 'Jean ajuste blanc', 'Levis', 'Herpi','jean_blanc_ajuste.jpg',NULL, NULL),
(NULL, 'jean Picasso ', '50', 'polyester','blanc', 'Jean droit blanc', 'Bershka', 'Herpi','jean_blanc_droit.jpg',NULL, NULL),
(NULL, 'jean Santiago ', '70', 'materiaux recyclés','blanc', 'Jean large blanc', 'Jack and Jones', 'BZB','jean_blanc_large.jpg',NULL, NULL),
(NULL, 'jean Mirabella ', '50', 'polyester','blanc', 'Jean large blanc', 'Bershka', 'Herpi','jean_blanc_large2.jpg',NULL, NULL),
(NULL, 'jean Starlight ', '60', 'coton','blanc', 'Jean slim blanc', 'Calvin Klein', 'Officine Générale','jean_blanc_slim.jpg',NULL, NULL),
(NULL, 'jean Summer ', '70', 'coton','blanc', 'Jean slim blanc', 'Levis', 'BZB','jean_blanc_slim2.jpg',NULL, NULL),
(NULL, 'jean Winter ', '45', 'coton','bleu', 'Jean ajuste bleu', 'Jack and Jones', 'Officine Générale','jean_bleu_ajuste.jpg',NULL, NULL),
(NULL, 'jean Flower ', '50', 'materiaux recyclés','bleu', 'Jean ajuste bleu', 'Calvin Klein', 'BZB','jean_bleu_ajuste2.jpg',NULL, NULL),
(NULL, 'jean OG ', '60', 'polyester','bleu', 'Jean droit bleu', 'Bershka', 'BZB','jean_bleu_droit.jpg',NULL, NULL),
(NULL, 'jean Simple ', '40', 'coton','bleu', 'Jean droit bleu', 'Levis', 'Officine Générale','jean_bleu_droit2.jpg',NULL, NULL),
(NULL, 'jean Crazy ', '45', 'polyester','bleu', 'Jean large bleu', 'Calvin Klein', 'Herpi','jean_bleu_large.jpg',NULL, NULL),
(NULL, 'jean Brazil ', '70', 'polyester','bleu', 'Jean large bleu', 'Jack and Jones', 'BZB','jean_bleu_large2.jpg',NULL, NULL),
(NULL, 'jean Tropical ', '50', 'coton','bleu', 'Jean large bleu', 'Bershka', 'Officine Générale','jean_bleu_large3.jpg',NULL, NULL),
(NULL, 'jean Ecolo ', '60', 'materiaux recyclés','bleu', 'Jean slim bleu', 'Levis', 'Herpi','jean_bleu_slim.jpg',NULL, NULL),
(NULL, 'jean Mer ', '40', 'coton','bleu', 'Jean slim bleu', 'Jack and Jones', 'Herpi','jean_bleu_slim2.jpg',NULL, NULL),
(NULL, 'jean Black ', '40', 'polyester','noir', 'Jean ajuste noir', 'Jack and Jones', 'Officine Générale','jean_noir_ajuste.jpg',NULL, NULL),
(NULL, 'jean Noche ', '70', 'coton','noir', 'Jean ajuste noir', 'Calvin Klein', 'BZB','jean_noir_ajuste2.jpg',NULL, NULL),
(NULL, 'jean Classico ', '50', 'coton','noir', 'Jean ajuste noir', 'Levis', 'Herpi','jean_noir_ajuste3.jpg',NULL, NULL),
(NULL, 'jean Recycle ', '40', 'materiaux recyclés','noir', 'Jean droit noir', 'Bershka', 'BZB','jean_noir_droit.jpg',NULL, NULL),
(NULL, 'jean Michou ', '70', 'polyester','noir', 'Jean droit noir', 'Calvin Klein', 'Officine Générale','jean_noir_droit2.jpg',NULL, NULL),
(NULL, 'jean Goat ', '45', 'coton','noir', 'Jean slim noir', 'Bershka', 'BZB','jean_noir_slim.jpg',NULL, NULL);

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');

