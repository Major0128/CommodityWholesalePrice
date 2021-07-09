/*
 Navicat Premium Data Transfer

 Source Server         : Local_Docker_MSDB_tempdb
 Source Server Type    : SQL Server
 Source Server Version : 14003048
 Source Host           : localhost:1433
 Source Catalog        : mall
 Source Schema         : dbo

 Target Server Type    : SQL Server
 Target Server Version : 14003048
 File Encoding         : 65001

 Date: 09/07/2021 17:30:20
*/


-- ----------------------------
-- Table structure for commodity_wholesale_price
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[commodity_wholesale_price]') AND type IN ('U'))
	DROP TABLE [dbo].[commodity_wholesale_price]
GO

CREATE TABLE [dbo].[commodity_wholesale_price] (
  [id] bigint  IDENTITY(1,1) NOT NULL,
  [price_date] datetime  NULL,
  [price] float(53)  NULL,
  [product_name] varchar(64) COLLATE Chinese_PRC_CI_AS  NULL,
  [marketing_name] varchar(64) COLLATE Chinese_PRC_CI_AS  NULL,
  [product_id] bigint  NULL,
  [price_unit] varchar(16) COLLATE Chinese_PRC_CI_AS  NULL,
  [create_time] datetime  NULL
)
GO

ALTER TABLE [dbo].[commodity_wholesale_price] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'价格日期',
'SCHEMA', N'dbo',
'TABLE', N'commodity_wholesale_price',
'COLUMN', N'price_date'
GO

EXEC sp_addextendedproperty
'MS_Description', N'价格',
'SCHEMA', N'dbo',
'TABLE', N'commodity_wholesale_price',
'COLUMN', N'price'
GO

EXEC sp_addextendedproperty
'MS_Description', N'商品名',
'SCHEMA', N'dbo',
'TABLE', N'commodity_wholesale_price',
'COLUMN', N'product_name'
GO

EXEC sp_addextendedproperty
'MS_Description', N'市场名',
'SCHEMA', N'dbo',
'TABLE', N'commodity_wholesale_price',
'COLUMN', N'marketing_name'
GO

EXEC sp_addextendedproperty
'MS_Description', N'商品id',
'SCHEMA', N'dbo',
'TABLE', N'commodity_wholesale_price',
'COLUMN', N'product_id'
GO

EXEC sp_addextendedproperty
'MS_Description', N'价格单位',
'SCHEMA', N'dbo',
'TABLE', N'commodity_wholesale_price',
'COLUMN', N'price_unit'
GO

EXEC sp_addextendedproperty
'MS_Description', N'创建时间',
'SCHEMA', N'dbo',
'TABLE', N'commodity_wholesale_price',
'COLUMN', N'create_time'
GO


-- ----------------------------
-- Indexes structure for table commodity_wholesale_price
-- ----------------------------
CREATE NONCLUSTERED INDEX [idx_price_date]
ON [dbo].[commodity_wholesale_price] (
  [price_date] ASC
)
GO

CREATE NONCLUSTERED INDEX [idx_product]
ON [dbo].[commodity_wholesale_price] (
  [product_name] ASC
)
GO

CREATE NONCLUSTERED INDEX [idx_marketing]
ON [dbo].[commodity_wholesale_price] (
  [marketing_name] ASC
)
GO


-- ----------------------------
-- Primary Key structure for table commodity_wholesale_price
-- ----------------------------
ALTER TABLE [dbo].[commodity_wholesale_price] ADD CONSTRAINT [PK__commodit__D50E2AB92D6E404C] PRIMARY KEY CLUSTERED ([id])
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)  
ON [PRIMARY]
GO

