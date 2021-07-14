CREATE TABLE [dbo].[ds_commodity_wholesale_price] (
  [id] bigint  IDENTITY(1,1) NOT NULL,
  [price_date] datetime  NULL,
  [price] float(53)  NULL,
  [product_name] varchar(64) COLLATE Chinese_PRC_CI_AS  NULL,
  [marketing_name] varchar(64) COLLATE Chinese_PRC_CI_AS  NULL,
  [product_id] bigint  NULL,
  [price_unit] varchar(16) COLLATE Chinese_PRC_CI_AS  NULL,
  [create_time] datetime  NULL
)