-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : mer. 02 avr. 2025 à 19:35
-- Version du serveur : 10.3.39-MariaDB-0+deb10u2
-- Version de PHP : 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `Midnightcraft`
--

-- --------------------------------------------------------

--
-- Structure de la table `messages`
--

CREATE TABLE `messages` (
  `message_id` int(11) NOT NULL,
  `player_uuid` varchar(36) NOT NULL,
  `username` text NOT NULL,
  `message` text NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `messages`
--

INSERT INTO `messages` (`message_id`, `player_uuid`, `username`, `message`, `date`) VALUES
(1, 'f4b2f7ff-cd60-3631-b8ca-fe63c2604d0b', 'Datavore', 'Owner I just bought for $50 dollar on shop', '2025-04-01 20:09:39'),
(2, 'f4b2f7ff-cd60-3631-b8ca-fe63c2604d0b', 'Datavore', 'Where is my rank ????', '2025-04-01 20:10:15'),
(3, '773f36b0-3da2-3df1-8de2-2891a18871b9', 'MechaShade', 'Bro leave this server. The owner is a scammer', '2025-04-01 20:10:20'),
(4, '773f36b0-3da2-3df1-8de2-2891a18871b9', 'MechaShade', 'He left with all the money and he deleted all it\'s messages...', '2025-04-01 20:10:30');

-- --------------------------------------------------------

--
-- Structure de la table `players`
--

CREATE TABLE `players` (
  `uuid` varchar(36) NOT NULL,
  `first_join` datetime NOT NULL DEFAULT current_timestamp(),
  `last_join` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `players`
--

INSERT INTO `players` (`uuid`, `first_join`, `last_join`) VALUES
('5fc9fa58-db9b-356e-910a-1bdbcc5d6f4e', '2025-02-03 10:17:28', '2025-03-20 18:17:28'),
('773f36b0-3da2-3df1-8de2-2891a18871b9', '2025-03-31 20:05:11', '2025-04-01 20:24:14'),
('f4b2f7ff-cd60-3631-b8ca-fe63c2604d0b', '2025-04-01 20:09:10', '2025-04-01 20:09:10');

-- --------------------------------------------------------

--
-- Structure de la table `website_users`
--

CREATE TABLE `website_users` (
  `id` int(11) NOT NULL,
  `username` varchar(40) NOT NULL,
  `password` text NOT NULL,
  `is_admin` int(11) NOT NULL,
  `date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `website_users`
--

INSERT INTO `website_users` (`id`, `username`, `password`, `is_admin`, `date`) VALUES
(1, 'admin', 'debfa77d7b298887d604956e1228caf0', 1, '2025-03-16 20:24:52');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `player_uuid` (`player_uuid`);

--
-- Index pour la table `players`
--
ALTER TABLE `players`
  ADD PRIMARY KEY (`uuid`);

--
-- Index pour la table `website_users`
--
ALTER TABLE `website_users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `messages`
--
ALTER TABLE `messages`
  MODIFY `message_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT pour la table `website_users`
--
ALTER TABLE `website_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`player_uuid`) REFERENCES `players` (`uuid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
