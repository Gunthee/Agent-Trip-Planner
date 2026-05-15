import pandas as pd 
import re 

def clean_price(price_text):
    """
    Return only the first price string

    Example:
    '23,888บาท' -> '23,888บาท'
    '15,388บาท10,388บาท' -> '15,388บาท'
    """

    if not isinstance(price_text, str):
        return None

    match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*บาท', price_text)

    if match:
        return f"{match.group(1)}บาท"

    return None


df = pd.read_csv("tours_merged_cleaned.csv")

df2 = pd.read_csv("tours_merged_fixed.csv")

column = df2['price'].apply(clean_price)
print(column)

prefix = "ราคา"


df['description'] = df['description'] +' '+prefix + column
print(df['description'][20])

df.to_csv("tours_merged_cleaned2.csv", index=False, encoding="utf-8-sig")