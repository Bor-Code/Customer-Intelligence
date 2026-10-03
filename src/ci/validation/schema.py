import pandera as pa
from pandera.typing import Series

class RetailSchema(pa.DataFrameModel):
    Invoice: Series[str] = pa.Field(coerce=True)
    StockCode: Series[str] = pa.Field(coerce=True)
    Description: Series[str] = pa.Field(nullable=True, coerce=True)
    Quantity: Series[int] = pa.Field(coerce=True)
    InvoiceDate: Series[pa.DateTime] = pa.Field(coerce=True)
    Price: Series[float] = pa.Field(ge=0.0, coerce=True)
    Customer_ID: Series[float] = pa.Field(nullable=True, coerce=True)
    Country: Series[str] = pa.Field(coerce=True)

    class Config:
        strict = False
