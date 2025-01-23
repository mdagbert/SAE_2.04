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
   password VARCHAR(50),
   role VARCHAR(50),
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