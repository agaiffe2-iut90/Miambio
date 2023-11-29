DROP TABLE IF EXISTS est_présent,produit, période_de_vente, Vente, Récolte ,Produits , Semaine, Saison ,Catégorie_produit , Maraichers , Marchés;
CREATE TABLE Marchés(
   Id_Marché INT AUTO_INCREMENT,
   Date_marché DATE NOT NULL,
   Lieu_du_marché TEXT NOT NULL,
   PRIMARY KEY(Id_Marché)
);

CREATE TABLE Maraichers(
   Id_Maraicher INT AUTO_INCREMENT,
   Nom_maraicher VARCHAR(50) NOT NULL,
   Prénom_maraicher VARCHAR(50) NOT NULL,
   Adresse TEXT,
   Numéro_de_téléphone VARCHAR(50),
   PRIMARY KEY(Id_Maraicher)
);

CREATE TABLE Catégorie_produit(
   Id_catégorie_produit INT AUTO_INCREMENT,
   Libellé_catégorie VARCHAR(50),
   PRIMARY KEY(Id_catégorie_produit)
);
CREATE TABLE Saison(
   Id_saison INT AUTO_INCREMENT,
   Libellé_saison VARCHAR(50),
   PRIMARY KEY(Id_saison)
);

CREATE TABLE Semaine(
   Id_Semaine INT AUTO_INCREMENT,
   PRIMARY KEY(Id_Semaine)
);

CREATE TABLE Produits(
   Id_produit INT AUTO_INCREMENT,
   Libellé_produit VARCHAR(50) NOT NULL,
   Id_catégorie_produit INT NOT NULL,
   PRIMARY KEY(Id_produit),
   FOREIGN KEY(Id_catégorie_produit) REFERENCES Catégorie_produit(Id_catégorie_produit)
);

CREATE TABLE Récolte(
   Id_Récolte INT AUTO_INCREMENT,
   Quantitée_récoltée INT,
   Id_Semaine INT NOT NULL,
   Id_produit INT NOT NULL,
   Id_Maraicher INT NOT NULL,
   PRIMARY KEY(Id_Récolte),
   FOREIGN KEY(Id_Semaine) REFERENCES Semaine(Id_Semaine),
   FOREIGN KEY(Id_produit) REFERENCES Produits(Id_produit),
   FOREIGN KEY(Id_Maraicher) REFERENCES Maraichers(Id_Maraicher)
);

CREATE TABLE Vente(
   Id_Vente INT AUTO_INCREMENT,
   Prix_de_vente INT,
   Quantitée_vendue INT,
   Prix_total_de_vente INT,
   Id_Semaine INT NOT NULL,
   Id_produit INT NOT NULL,
   Id_Marché INT NOT NULL,
   Id_Maraicher INT NOT NULL,
   PRIMARY KEY(Id_Vente),
   FOREIGN KEY(Id_Semaine) REFERENCES Semaine(Id_Semaine),
   FOREIGN KEY(Id_produit) REFERENCES Produits(Id_produit),
   FOREIGN KEY(Id_Marché) REFERENCES Marchés(Id_Marché),
   FOREIGN KEY(Id_Maraicher) REFERENCES Maraichers(Id_Maraicher)
);

CREATE TABLE est_présent(
   Id_Marché INT,
   Id_Maraicher INT,
   PRIMARY KEY(Id_Marché, Id_Maraicher),
   FOREIGN KEY(Id_Marché) REFERENCES Marchés(Id_Marché),
   FOREIGN KEY(Id_Maraicher) REFERENCES Maraichers(Id_Maraicher)
);

CREATE TABLE produit(
   Id_Maraicher INT,
   Id_produit INT,
   Surface_cultivée INT,
   PRIMARY KEY(Id_Maraicher, Id_produit),
   FOREIGN KEY(Id_Maraicher) REFERENCES Maraichers(Id_Maraicher),
   FOREIGN KEY(Id_produit) REFERENCES Produits(Id_produit)

);

CREATE TABLE période_de_vente(
   Id_produit INT,
   Id_saison INT,
   PRIMARY KEY(Id_produit, Id_saison),
   FOREIGN KEY(Id_produit) REFERENCES Produits(Id_produit),
   FOREIGN KEY(Id_saison) REFERENCES Saison(Id_saison)
);



-- INSERT


INSERT INTO Marchés (Date_marché, Lieu_du_marché) VALUES
('2023-11-15', 'Belfort'),
('2023-11-16', 'Libreville'),
('2023-11-17', 'Chèvremont');

INSERT INTO Maraichers (Id_Maraicher, Nom_maraicher, Prénom_maraicher, Adresse, Numéro_de_téléphone) VALUES
('1', 'Hollande', 'François', '5 rue des Mirabelles', '0754646478'),
('2', 'Girado', 'Jérôme', '9 rue Lafayette', '0624897548'),
('3', 'Poulain', 'Amélie', '1 rue de plancher-bas', '0748952154'),
('4', 'Vuyon', 'Hugo', '8 avenue Denfert-Rochereau', '0678123651');

INSERT INTO Catégorie_produit (Id_catégorie_produit, Libellé_catégorie) VALUES
('1','Légumes'),
('2','Fruits'),
('3','Herbes aromatiques');

INSERT INTO Saison (Id_saison, Libellé_saison) VALUES
('1','Été'),
('2','Automne'),
('3','Hiver'),
('4','Printemps');

INSERT INTO Semaine (Id_Semaine) VALUE
('1'),
('2'),
('3');

INSERT INTO Produits (Libellé_produit, Id_catégorie_produit) VALUES
('Tomates', 1),
('Pommes', 2),
('Persil', 3);


INSERT INTO Récolte (Quantitée_récoltée, Id_Semaine, Id_produit, Id_Maraicher) VALUES
(100, 1, 1, 1),
(150, 1, 2, 2),
(75, 2, 3, 3);

INSERT INTO Vente (Prix_de_vente, Quantitée_vendue, Prix_total_de_vente, Id_Semaine, Id_produit, Id_Marché, Id_Maraicher) VALUES
(2, 50, 100, 1, 1, 1, 1),
(3, 100, 300, 1, 2, 2, 2),
(1, 30, 30, 2, 3, 3, 3);

INSERT INTO est_présent (Id_Marché, Id_Maraicher) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO production (Id_Maraicher, Id_produit) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO période_de_vente (Id_produit, Id_saison) VALUES
(1, 1),
(2, 2),
(3, 3);


-- REQUETES


-- total des ventes par marchés
SELECT Marchés.Lieu_du_marché, SUM(Vente.Prix_total_de_vente) AS Total_ventes
FROM Marchés
INNER JOIN Vente ON Marchés.Id_Marché = Vente.Id_Marché
GROUP BY Marchés.Lieu_du_marché;

-- récolte moyenne par produit
SELECT Produits.Libellé_produit, AVG(Récolte.Quantitée_récoltée) AS Moyenne_récolte
FROM Produits
INNER JOIN Récolte ON Produits.Id_produit = Récolte.Id_produit
GROUP BY Produits.Libellé_produit;

-- nombre de produits vendus par saison
SELECT Saison.Libellé_saison, COUNT(DISTINCT Vente.Id_produit) AS Nombre_produits_vendus
FROM Saison
INNER JOIN période_de_vente ON Saison.Id_saison = période_de_vente.Id_saison
INNER JOIN Vente ON période_de_vente.Id_produit = Vente.Id_produit
GROUP BY Saison.Libellé_saison;

-- récoltes par maraîchers
SELECT
    M.Nom_maraicher,
    R.Id_produit,
    SUM(R.Quantitée_récoltée) AS Total_récolté,
    V.Id_produit AS Produit_plus_vendu,
    COUNT(V.Id_produit) AS Nb_ventes_produit_plus_vendu
FROM
    Maraichers M
LEFT JOIN
    Récolte R ON M.Id_Maraicher = R.Id_Maraicher
LEFT JOIN
    Vente V ON M.Id_Maraicher = V.Id_Maraicher
GROUP BY
    M.Nom_maraicher, R.Id_produit, V.Id_produit
ORDER BY
    M.Nom_maraicher, SUM(R.Quantitée_récoltée) DESC;


