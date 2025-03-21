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
    stock INT,
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
('jean Xantia ', '45', 'coton','blanc', 'Jean ajuste blanc', 'Levis', 'Herpi','jean_blanc_ajuste.jpg',2, 4),
('jean Picasso ', '50', 'polyester','blanc', 'Jean droit blanc', 'Bershka', 'Herpi','jean_blanc_droit.jpg',2, 2),
('jean Santiago ', '70', 'materiaux recyclés','blanc', 'Jean large blanc', 'Jack and Jones', 'BZB','jean_blanc_large.jpg',2, 3),
('jean Mirabella ', '50', 'polyester','blanc', 'Jean large blanc', 'Bershka', 'Herpi','jean_blanc_large2.jpg',2, 3),
('jean Starlight ', '60', 'coton','blanc', 'Jean slim blanc', 'Calvin Klein', 'Officine Générale','jean_blanc_slim.jpg',2, 1),
('jean Summer ', '70', 'coton','blanc', 'Jean slim blanc', 'Levis', 'BZB','jean_blanc_slim2.jpg',2, 1),
('jean Winter ', '45', 'coton','bleu', 'Jean ajuste bleu', 'Jack and Jones', 'Officine Générale','jean_bleu_ajuste.jpg',2, 4),
('jean Flower ', '50', 'materiaux recyclés','bleu', 'Jean ajuste bleu', 'Calvin Klein', 'BZB','jean_bleu_ajuste2.jpg',2, 4),
('jean OG ', '60', 'polyester','bleu', 'Jean droit bleu', 'Bershka', 'BZB','jean_bleu_droit.jpg',2, 2),
('jean Simple ', '40', 'coton','bleu', 'Jean droit bleu', 'Levis', 'Officine Générale','jean_bleu_droit2.jpg',2, 2),
('jean Crazy ', '45', 'polyester','bleu', 'Jean large bleu', 'Calvin Klein', 'Herpi','jean_bleu_large.jpg',2, 3),
('jean Brazil ', '70', 'polyester','bleu', 'Jean large bleu', 'Jack and Jones', 'BZB','jean_bleu_large2.jpg',2, 3),
('jean Tropical ', '50', 'coton','bleu', 'Jean large bleu', 'Bershka', 'Officine Générale','jean_bleu_large3.jpg',2, 3),
('jean Ecolo ', '60', 'materiaux recyclés','bleu', 'Jean slim bleu', 'Levis', 'Herpi','jean_bleu_slim.jpg',2, 1),
('jean Mer ', '40', 'coton','bleu', 'Jean slim bleu', 'Jack and Jones', 'Herpi','jean_bleu_slim2.jpg',2, 1),
('jean Black ', '40', 'polyester','noir', 'Jean ajuste noir', 'Jack and Jones', 'Officine Générale','jean_noir_ajuste.jpg',2, 4),
('jean Noche ', '70', 'coton','noir', 'Jean ajuste noir', 'Calvin Klein', 'BZB','jean_noir_ajuste2.jpg',2, 4),
('jean Classico ', '50', 'coton','noir', 'Jean ajuste noir', 'Levis', 'Herpi','jean_noir_ajuste3.jpg',2, 4),
('jean Recycle ', '40', 'materiaux recyclés','noir', 'Jean droit noir', 'Bershka', 'BZB','jean_noir_droit.jpg',2, 2),
('jean Michou ', '70', 'polyester','noir', 'Jean droit noir', 'Calvin Klein', 'Officine Générale','jean_noir_droit2.jpg',2, 2),
('jean Goat ', '45', 'coton','noir', 'Jean slim noir', 'Bershka', 'BZB','jean_noir_slim.jpg',2, 1);

UPDATE jean SET stock = 1 ;

INSERT INTO utilisateur(login,email,password,role,nom,est_actif) VALUES
('admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
('client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
('client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');

INSERT INTO commande (date_achat, utilisateur_id, etat_id) VALUES
('2024-02-01', 1, 1),  -- En attente
('2024-02-05', 2, 2),  -- Expédié
('2024-02-10', 3, 3),  -- Validé
('2024-02-15', 1, 4);  -- Confirmé
INSERT INTO ligne_commande (jean_id, commande_id, prix, quantite_commande) VALUES
(1, 1, 45.00, 2),
(2, 1, 50.00, 1),
(3, 2, 70.00, 3),
(4, 2, 50.00, 2),
(5, 3, 60.00, 1),
(6, 3, 70.00, 1),
(7, 4, 45.00, 2),
(8, 4, 50.00, 1);