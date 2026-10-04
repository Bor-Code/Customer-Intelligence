import polars as pl

def build_anomaly_features(sales_df: pl.DataFrame, returns_df: pl.DataFrame) -> pl.DataFrame:
    if not sales_df.is_empty():
        sales_agg = sales_df.group_by("Customer_ID").agg(
            pl.col("Invoice").n_unique().alias("Total_Purchases"),
            (pl.col("Quantity") * pl.col("Price")).sum().alias("Total_Spent"),
        )
    else:
        sales_agg = pl.DataFrame(
            {"Customer_ID": pl.Int64, "Total_Purchases": pl.UInt32, "Total_Spent": pl.Float64}
        )

    if not returns_df.is_empty():
        returns_agg = returns_df.group_by("Customer_ID").agg(
            pl.col("Invoice").n_unique().alias("Total_Returns"),
            (pl.col("Quantity").abs() * pl.col("Price")).sum().alias("Total_Refunded"),
        )
    else:
        returns_agg = pl.DataFrame(
            {"Customer_ID": pl.Int64, "Total_Returns": pl.UInt32, "Total_Refunded": pl.Float64}
        )

    if sales_agg.is_empty() and returns_agg.is_empty():
        return pl.DataFrame(
            schema={
                "Customer_ID": pl.Int64,
                "Return_Ratio": pl.Float64,
                "Refund_Ratio": pl.Float64,
            }
        )

    features = sales_agg.join(returns_agg, on="Customer_ID", how="outer_coalesce")
    features = features.fill_null(0)

    features = features.with_columns(
        (pl.col("Total_Returns") / (pl.col("Total_Purchases") + pl.col("Total_Returns")))
        .fill_nan(0)
        .alias("Return_Ratio"),
        (pl.col("Total_Refunded") / (pl.col("Total_Spent") + pl.col("Total_Refunded")))
        .fill_nan(0)
        .alias("Refund_Ratio"),
    )

    return features.select(["Customer_ID", "Return_Ratio", "Refund_Ratio"])
