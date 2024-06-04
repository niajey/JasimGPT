from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel , Field
import os  
from langchain_core.tools import Tool , tool
from langchain_core.messages import AIMessage , SystemMessage , HumanMessage
from langchain_core.output_parsers import   StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


import requests 
import json


os.environ['OPENAI_API_KEY'] =  st.secrets["OPENAI_API_KEY"]
os.environ['SUPERMARKETS_API_KEY'] =  st.secrets["SUPERMARKETS_API_KEY"]
os.environ['TAVILY_API_KEY']  =  st.secrets["TAVILY_API_KEY"]
chatHistory=[]


def getProductPriceByBarcodeFromMarket(productBarCode ,  marketName='ALL' , pricingSummerizationMethod='AVG') : 
    """ this method retuns price of an item based on its barcode. The price is fetched from Kuwaiti Supermarkets"""
    result = []
    try : 
        url = "http://daiyacoop.com/appadmin/api/get_product/{barcode}".format(barcode=productBarCode)
        payload = {}
        headers = {
          'api-key': os.environ['SUPERMARKETS_API_KEY'],
          'Cookie': 'ci_session=gc9isema4iojitf8ef05rh69b6iu4ft1'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if 200==response.status_code : 
            jdata = json.loads(response.text )
            pstatus = jdata['status']
            if bool(pstatus) : 
                pdata = jdata['data'][0]
                pprice = pdata['price']
                pdescrition = pdata['product_description']
                result.append({'market_name':marketName , 'item_name':pdescrition, 'price':pprice,  'barcode':productBarCode })
    except : 
        result=[]
    return result
    
#print(getProductPriceByBarcodeFromMarket(None))



def getProductsListFromSuperMarketsBasedOnWord( productName) : 
    """ this tool returns """
    result = ''
    try : 
        url = "http://daiyacoop.com/appadmin/api/search_product"
        payload = {'query':productName}
        headers = {
          'api-key': os.environ['SUPERMARKETS_API_KEY'],
          'Cookie': 'ci_session=gc9isema4iojitf8ef05rh69b6iu4ft1'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if 200==response.status_code : 
            jdata = json.loads(response.text )
            pstatus = jdata['status']
            if bool(pstatus) : 
                for x in jdata['data'] : 
                    pdata = x
                    pprice = pdata['price']
                    pdescrition = pdata['product_description']
                    barcode = pdata['barcode_number']
                    msg="""product name is  : {item_name} , and it's price is : {price}"""
                    result = result + msg.format( item_name=pdescrition, price=pprice ) + '\n'

    except :
        result = ''
    return result    

class SuperMarketByName(BaseModel) : 
    productname : str =Field(description = ' this is the product name to search and get the price from market')                        

@tool("get product info from supermarket by product name", args_schema = SuperMarketByName   )
def getProductsListFromSuperMarkets(productname: str ) ->str : 
    """ This tool is usfull to  search an Item name in supermarkets and return its price. This returns many possible matches and you must select what matches the customer input. its important to pass to the tool the argument as product name like such as Cheese"""
    lis = productname.split() 
    result = ''
    for x in lis : 
       re= getProductsListFromSuperMarketsBasedOnWord(x)
       result = result + re + '\n'
    return result

def getProductPriceBybarcodeWrapperFormLLM(productBarcode:str) ->str: 
    #print("checking : " , productBarcode)
    response = getProductPriceByBarcodeFromMarket(productBarcode ,  marketName='ALL' , pricingSummerizationMethod='AVG') 
    price = '0' 
    try : 
        data = response[0] 
        price = data['price'] ##"product name is {name} and its price is {price}".format(price=data['price'],name=data['item_name'])
        price = "Price returned is : {prc}".format(prc=price)
    except :
        price = '0'
    return price 

#price = getProductPriceBybarcodeWrapperFormLLM('8000815004776')


def getInternetSearch(searchQuery) : 

    search = TavilySearchResults()
    res = search.run(searchQuery) 
    return res

#getInternetSearch("what is happening in Kuwait")


def getTivSearchResult(strdict) : 
    dic = json.loads(strdict)
    name = dic['name']
    hits = int(dic['hits'])
    search = TavilySearchResults()
    res = search.run(f"{name} linked full profile page") 
    results = ''
    for x in range(hits) : 
       try : 
        results = results+res[x]['url'] + "\n"
       except : 
           break
    return results 

getTivSearchResult("""{"name":"Mousa Alsulaimi" , "hits":1}""")
