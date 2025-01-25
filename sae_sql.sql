DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS jean;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS coupe_jean;
DROP TABLE IF EXISTS taille;

CREATE TABLE IF NOT EXISTS taille (
   id_taille INT AUTO_INCREMENT,
   nom_taille VARCHAR(50),
   PRIMARY KEY (id_taille)
);

CREATE TABLE IF NOT EXISTS coupe_jean (
   id_coupe_jean INT AUTO_INCREMENT,
   nom_coupe VARCHAR(50),
   PRIMARY KEY (id_coupe_jean)
);

CREATE TABLE IF NOT EXISTS utilisateur (
   id_utilisateur INT AUTO_INCREMENT,
   login VARCHAR(50),
   email VARCHAR(50),
   nom VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(50),
   est_actif CHAR(1),
   PRIMARY KEY (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS etat (
   id_etat INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY (id_etat)
);

CREATE TABLE IF NOT EXISTS jean (
   id_jean INT AUTO_INCREMENT,
   nom_jean VARCHAR(50),
   prix_jean DECIMAL(5, 2),
   matiere VARCHAR(50),
   couleur VARCHAR(50),
   description TEXT,
   marque VARCHAR(50),
   fournisseur VARCHAR(50),
   photo VARCHAR(255),
   taille_id INT NOT NULL,
   coupe_jean_id INT NOT NULL,
   PRIMARY KEY (id_jean),
   CONSTRAINT fk_jean_taille FOREIGN KEY (taille_id) REFERENCES taille (id_taille),
   CONSTRAINT fk_jean_coupe FOREIGN KEY (coupe_jean_id) REFERENCES coupe_jean (id_coupe_jean)
);

CREATE TABLE IF NOT EXISTS commande (
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   utilisateur_id INT NOT NULL,
   etat_id INT NOT NULL,
   PRIMARY KEY (id_commande),
   CONSTRAINT fk_commande_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur),
   CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat (id_etat)
);

CREATE TABLE IF NOT EXISTS ligne_commande (
   jean_id INT,
   commande_id INT,
   prix DECIMAL(5, 2),
   quantite_commande INT,
   PRIMARY KEY (jean_id, commande_id),
   CONSTRAINT fk_ligne_commande_jean FOREIGN KEY (jean_id) REFERENCES jean (id_jean) ,
   CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande (id_commande)
);

CREATE TABLE IF NOT EXISTS ligne_panier (
   jean_id INT,
   utilisateur_id INT,
   quantite_panier INT,
   date_ajout DATE,
   PRIMARY KEY (jean_id, utilisateur_id),
   CONSTRAINT fk_ligne_panier_jean FOREIGN KEY (jean_id) REFERENCES jean (id_jean),
   CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

-- Populate the `etat` table
INSERT INTO etat (libelle) VALUES
('en attente'),
('expédié'),
('validé'),
('confirmé');

-- Populate the `taille` table
INSERT INTO taille (nom_taille) VALUES
('W29'),
('W30'),
('W32'),
('W34'),
('W38');

-- Populate the `coupe_jean` table
INSERT INTO coupe_jean (nom_coupe) VALUES
('slim'),
('droit'),
('large'),
('ajuste');

-- Populate the `utilisateur` table
INSERT INTO utilisateur (login, email, nom, password, role, est_actif) VALUES
('admin', 'admin@admin.fr', 'admin', 'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988', 'ROLE_admin', '1'),
('client', 'client@client.fr', 'client', 'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349', 'ROLE_client', '1'),
('client2', 'client2@client2.fr', 'client2', 'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080', 'ROLE_client', '1');

-- Populate the `jean` table with valid foreign keys
INSERT INTO jean (nom_jean, prix_jean, matiere, couleur, description, marque, fournisseur, photo, taille_id, coupe_jean_id) VALUES
('jean Xantia', '45', 'coton', 'blanc', 'Jean ajuste blanc', 'Levis', 'Herpi', 'jean_blanc_ajuste.jpg', 1, 4),
('jean Picasso', '50', 'polyester', 'blanc', 'Jean droit blanc', 'Bershka', 'Herpi', 'jean_blanc_droit.jpg', 2, 2);
-- Continue with remaining data entries, ensuring proper `taille_id` and `coupe_jean_id`.
