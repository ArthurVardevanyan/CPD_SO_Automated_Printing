-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 18, 2020 at 01:48 PM
-- Server version: 10.5.2-MariaDB-1:10.5.2+maria~focal
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `school_orders`
--

-- --------------------------------------------------------

--
-- Table structure for table `deliver`
--

CREATE TABLE `deliver` (
  `order_number` varchar(11) NOT NULL,
  `name` varchar(25) NOT NULL,
  `address` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `files`
--

CREATE TABLE `files` (
  `file_number` varchar(14) NOT NULL,
  `order_number` varchar(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `pages` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `order_data`
--

CREATE TABLE `order_data` (
  `email_id` varchar(28) NOT NULL,
  `order_number` varchar(10) NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `sheets` int(11) NOT NULL,
  `cost` varchar(11) NOT NULL,
  `duplex` varchar(50) DEFAULT NULL,
  `date_ordered` date DEFAULT NULL,
  `order_subject` varchar(50) DEFAULT NULL,
  `copies` varchar(50) DEFAULT NULL,
  `paper` varchar(50) DEFAULT NULL,
  `drilling` varchar(50) DEFAULT NULL,
  `collation` varchar(50) DEFAULT NULL,
  `email` varchar(25) NOT NULL,
  `stapling` varchar(25) NOT NULL,
  `front_cover` varchar(25) NOT NULL,
  `folding` varchar(25) NOT NULL,
  `cutting` varchar(25) NOT NULL,
  `booklets` varchar(25) NOT NULL,
  `slip_shrink` varchar(500) NOT NULL,
  `special_instructions` varchar(500) NOT NULL,
  `back_cover` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `email` varchar(25) NOT NULL,
  `first_name` varchar(25) NOT NULL,
  `last_name` varchar(25) NOT NULL,
  `phone` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `deliver`
--
ALTER TABLE `deliver`
  ADD PRIMARY KEY (`order_number`);

--
-- Indexes for table `files`
--
ALTER TABLE `files`
  ADD PRIMARY KEY (`file_number`),
  ADD KEY `order_number` (`order_number`);

--
-- Indexes for table `order_data`
--
ALTER TABLE `order_data`
  ADD PRIMARY KEY (`email_id`),
  ADD UNIQUE KEY `Order Number` (`order_number`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`email`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `deliver`
--
ALTER TABLE `deliver`
  ADD CONSTRAINT `deliver_ibfk_1` FOREIGN KEY (`order_number`) REFERENCES `order_data` (`order_number`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `files`
--
ALTER TABLE `files`
  ADD CONSTRAINT `files_ibfk_1` FOREIGN KEY (`order_number`) REFERENCES `order_data` (`order_number`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `teachers`
--
ALTER TABLE `teachers`
  ADD CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`email`) REFERENCES `order_data` (`email_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;