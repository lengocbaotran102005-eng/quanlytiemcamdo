-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 11, 2026 at 03:46 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pawnshop_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('bcd58ab365e3');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `id_card` varchar(20) DEFAULT NULL,
  `address` text,
  `note` text,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `full_name`, `phone`, `id_card`, `address`, `note`, `created_at`) VALUES
(1, 'Nguyễn Văn A', '0901234567', '012345678901', 'Quận 1, TP.HCM', 'Khách quen', '2026-03-11 02:56:42'),
(2, 'Trần Thị B', '0902345678', '012345678902', 'Quận Bình Thạnh, TP.HCM', NULL, '2026-03-11 02:56:42');

-- --------------------------------------------------------

--
-- Table structure for table `item_images`
--

CREATE TABLE `item_images` (
  `id` int NOT NULL,
  `item_id` int NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_path` varchar(500) NOT NULL,
  `file_size` int DEFAULT NULL,
  `is_primary` tinyint(1) DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pawn_items`
--

CREATE TABLE `pawn_items` (
  `id` int NOT NULL,
  `name` varchar(200) NOT NULL,
  `category` enum('electronics','jewelry','vehicle','documents','other') NOT NULL,
  `brand` varchar(100) DEFAULT NULL,
  `serial_number` varchar(100) DEFAULT NULL,
  `condition` enum('good','fair','poor') NOT NULL,
  `description` text,
  `estimated_value` decimal(15,2) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pawn_items`
--

INSERT INTO `pawn_items` (`id`, `name`, `category`, `brand`, `serial_number`, `condition`, `description`, `estimated_value`, `created_at`) VALUES
(1, 'iPhone 14 Pro 256GB', 'electronics', 'Apple', 'IPH14PRO256', 'good', NULL, '25000000.00', '2026-03-11 02:56:42'),
(2, 'Nhẫn vàng 18K 2 chỉ', 'jewelry', 'PNJ', NULL, 'good', NULL, '14000000.00', '2026-03-11 02:56:42'),
(4, 'VF8', 'other', NULL, NULL, 'good', NULL, '100000000.00', '2026-03-11 03:51:54'),
(5, 'VF9', 'other', NULL, NULL, 'good', NULL, '100000000.00', '2026-03-11 07:21:03');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int NOT NULL,
  `transaction_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `payment_type` enum('interest','partial','redeem','extension') NOT NULL,
  `payment_date` date NOT NULL,
  `note` text,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`id`, `transaction_id`, `staff_id`, `amount`, `payment_type`, `payment_date`, `note`, `created_at`) VALUES
(1, 4, 1, '0.00', 'extension', '2026-03-11', 'Gia hạn thêm 30 ngày, thu lãi kỳ trước', '2026-03-11 04:04:37'),
(2, 4, 1, '100000000.00', 'redeem', '2026-03-11', 'Chuộc đồ - tất toán phiếu, gồm gốc và lãi còn lại', '2026-03-11 04:05:27'),
(3, 2, 1, '320000.00', 'interest', '2026-03-11', 'Thu lãi từ 30/01/2026 đến 11/03/2026', '2026-03-11 04:11:32'),
(4, 1, 1, '450000.00', 'extension', '2026-03-11', 'Gia hạn thêm 30 ngày, thu lãi kỳ trước', '2026-03-11 04:13:17'),
(5, 1, 1, '450000.00', 'extension', '2026-03-11', 'Gia hạn thêm 30 ngày, thu lãi kỳ trước', '2026-03-11 04:13:23'),
(6, 1, 1, '15000000.00', 'redeem', '2026-03-11', 'Chuộc đồ - tất toán phiếu, gồm gốc và lãi còn lại', '2026-03-11 04:39:15'),
(7, 2, 1, '8000000.00', 'redeem', '2026-03-11', 'Chuộc đồ - tất toán phiếu, gồm gốc và lãi còn lại', '2026-03-11 07:00:05');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int NOT NULL,
  `ticket_no` varchar(20) NOT NULL,
  `customer_id` int NOT NULL,
  `item_id` int NOT NULL,
  `staff_id` int NOT NULL,
  `pawn_value` decimal(15,2) NOT NULL,
  `interest_rate` decimal(5,2) NOT NULL,
  `interest_type` enum('daily','monthly') DEFAULT NULL,
  `pawn_date` date NOT NULL,
  `due_date` date NOT NULL,
  `duration_days` int NOT NULL,
  `status` enum('active','redeemed','overdue','extended','liquidated') NOT NULL,
  `redeem_amount` decimal(15,2) DEFAULT NULL,
  `redeem_date` date DEFAULT NULL,
  `redeem_by` int DEFAULT NULL,
  `notes` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `extension_count` int NOT NULL,
  `brought_name` varchar(100) DEFAULT NULL,
  `brought_id_card` varchar(20) DEFAULT NULL,
  `brought_phone` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `ticket_no`, `customer_id`, `item_id`, `staff_id`, `pawn_value`, `interest_rate`, `interest_type`, `pawn_date`, `due_date`, `duration_days`, `status`, `redeem_amount`, `redeem_date`, `redeem_by`, `notes`, `created_at`, `updated_at`, `extension_count`, `brought_name`, `brought_id_card`, `brought_phone`) VALUES
(1, 'TCD-20260311-001', 1, 1, 2, '15000000.00', '3.00', 'monthly', '2026-03-11', '2026-06-09', 90, 'redeemed', '15000000.00', '2026-03-11', 1, NULL, '2026-03-11 02:56:42', '2026-03-11 04:39:15', 2, NULL, NULL, NULL),
(2, 'TCD-20260311-002', 2, 2, 2, '8000000.00', '3.00', 'monthly', '2026-01-30', '2026-03-01', 30, 'redeemed', '8000000.00', '2026-03-11', 1, NULL, '2026-03-11 02:56:42', '2026-03-11 07:00:05', 0, NULL, NULL, NULL),
(4, 'TCD-20260311-003', 1, 4, 1, '100000000.00', '3.00', 'monthly', '2026-03-11', '2026-05-10', 60, 'redeemed', '100000000.00', '2026-03-11', 1, NULL, '2026-03-11 03:51:54', '2026-03-11 04:05:27', 1, NULL, NULL, NULL),
(5, 'TCD-20260311-004', 1, 5, 1, '100000000.00', '5.00', 'monthly', '2026-03-11', '2026-06-19', 100, 'active', NULL, NULL, NULL, NULL, '2026-03-11 07:21:03', NULL, 0, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `role` enum('admin','staff') NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `avatar_url` varchar(255) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `bio` text,
  `last_login` datetime DEFAULT NULL,
  `must_change_password` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `full_name`, `phone`, `role`, `is_active`, `avatar_url`, `email`, `bio`, `last_login`, `must_change_password`, `created_at`, `updated_at`, `is_deleted`) VALUES
(1, 'admin', '$2b$12$tOPbnuE3tgSVnxIDUlnPd.EDM3H7dEar7Lo7hnmONllp9FxNC6/Lu', 'Quản lý hệ thống', '0900000000', 'admin', 1, '/static/uploads/avatars/1.webp', NULL, NULL, '2026-03-11 08:50:40', 1, '2026-03-11 02:56:37', '2026-03-11 08:50:40', 0),
(2, 'staff1', '$2b$12$HtX7vhB1DF2VWr4Whq4pEOy7DQpCcwlslH7z2S8RKS1wQywiLYk9.', 'Nhân viên giao dịch', '0901111111', 'staff', 1, NULL, NULL, NULL, '2026-03-11 03:05:05', 1, '2026-03-11 02:56:42', '2026-03-11 04:40:16', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_card` (`id_card`);

--
-- Indexes for table `item_images`
--
ALTER TABLE `item_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `pawn_items`
--
ALTER TABLE `pawn_items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `staff_id` (`staff_id`),
  ADD KEY `transaction_id` (`transaction_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ticket_no` (`ticket_no`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `item_id` (`item_id`),
  ADD KEY `redeem_by` (`redeem_by`),
  ADD KEY `staff_id` (`staff_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `item_images`
--
ALTER TABLE `item_images`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pawn_items`
--
ALTER TABLE `pawn_items`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `item_images`
--
ALTER TABLE `item_images`
  ADD CONSTRAINT `item_images_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `pawn_items` (`id`);

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`staff_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`);

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `pawn_items` (`id`),
  ADD CONSTRAINT `transactions_ibfk_3` FOREIGN KEY (`redeem_by`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `transactions_ibfk_4` FOREIGN KEY (`staff_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
