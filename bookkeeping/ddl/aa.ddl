CREATE TABLE `transaction_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `batch_id` varchar(40) NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0' COMMENT '0待确认, 1确认, 2删除',
  `createDT` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updateDT` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `creator` varchar(50) DEFAULT NULL,
  `updator` varchar(50) DEFAULT NULL,

  `transaction_date` datetime DEFAULT NULL,
  `item` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `price` decimal(10,2) DEFAULT '0.00',
  `quantity` decimal(10,2) DEFAULT '1.00',
  `quantity_unit` varchar(20) DEFAULT '个',
  `amount` decimal(10,2) DEFAULT '0.00',
  `ttype` varchar(255) DEFAULT NULL COMMENT '支出=31,收入=42',
  `payment` varchar(200) DEFAULT NULL COMMENT '收付款方式 支出时默认现金，收入时默认银行转帐',
  `remark` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=500 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
