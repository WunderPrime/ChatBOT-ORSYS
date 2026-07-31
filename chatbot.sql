create database chatbot;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE commandes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    montant NUMERIC,
    date_commande DATE
);

CREATE TABLE produits (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    prix NUMERIC,
    stock INTEGER
);

CREATE TABLE factures (
    id SERIAL PRIMARY KEY,
    commande_id INTEGER REFERENCES commandes(id),
    montant_ttc NUMERIC,
    date_facture DATE
);

CREATE TABLE reclamations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    sujet TEXT,
    statut TEXT
);

INSERT INTO users (name, email) VALUES
('Amine', 'amine@example.com'),
('Sara', 'sara@example.com'),
('Youssef', 'youssef@example.com');

INSERT INTO commandes (user_id, montant, date_commande) VALUES
(1, 250.50, '2026-07-01'),
(2, 100.00, '2026-07-15');

INSERT INTO reclamations (user_id, sujet, statut) VALUES
(1, 'Livraison en retard', 'en cours'),
(3, 'Produit défectueux', 'résolu');


select * from users;


