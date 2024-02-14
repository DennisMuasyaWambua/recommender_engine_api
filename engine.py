from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import logging


app = FastAPI()
logging.basicConfig(level=logging.INFO)
products_data = pd.read_csv("/home/dennis/Desktop/regulusProducts.csv")
data = pd.DataFrame(products_data)
products_bought = data.pivot_table(values="Order number",index="Customer name", columns="Product")

class Product(BaseModel):
    name:str

@app.get('/')
def initial():
    return{"Data":data["Product"].to_json(),}

@app.post('/recommend')
def recommend(product: Product):
    print(Product.name)
    dictionary = products_bought[Product.name]
    similarBooks = products_bought.corrwith(dictionary)
    similarBooks = similarBooks.dropna()
    similarBooksdf = pd.DataFrame(similarBooks)
    return {"products":similarBooksdf.to_json()}
    