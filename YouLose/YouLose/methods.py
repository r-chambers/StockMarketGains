import requests
import re
import bs4 as bs
from bs4 import BeautifulSoup

def get_present_price(ticker):
    
    ticker = ticker.lower()
   
    #gets beautiful soup of marketwatch page for the ticker
    url = "https://www.marketwatch.com/investing/stock/"+ticker.lower()+"?mod=search_symbol"
    
    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
   
    my_regex = re.compile(ticker)
    matched_strings = soup.find_all(text=my_regex)
    
    #price string holds the line which contains the price
    price_string = ""
    
    for matched_string in matched_strings:
        line = str(matched_string)
        
        #attepmts to locate the price using the keyword price
        if(line.find("price") != -1):
            loc = line.find("price")
            price_string += line[loc:loc+20]
        elif(line.find(",priceCur") != -1):
            loc = line.find(",priceCur")
            price_string += line[loc-20:loc]
            
            
            
    #price holds just the numbers of the price
    price = ""
    
    for letter in price_string:
        if(letter.isdigit() or letter == "."):
            price += letter
      
    #updates instance variables, returns price
    #watchlist.append(ticker.upper() + ", $" + str(price))
    return price

