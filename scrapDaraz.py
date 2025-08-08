from selenium import webdriver
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import time
import pandas as pd     

# Step 1: Scrape data from Daraz
driver = webdriver.Chrome()
search_url = "https://www.daraz.com.bd/catalog/?spm=a2a0e.tm80335411.search.2.735212f7lP8Lz4&q=laptop&_keyori=ss&from=search_history&sugg=laptop_0_1"
driver.get(search_url)
time.sleep(5)

products = driver.find_elements(By.CLASS_NAME, "Bm3ON")

data = []

for i, product in enumerate(products):
    try:
        title = product.find_element(By.CLASS_NAME, "RfADt").text
        price = product.find_element(By.CLASS_NAME, "aBrP0").text
        link = product.find_element(By.TAG_NAME, "a").get_attribute("href")
        data.append({
            "title": title, 
            "price": price,
            "link": link 
        })
    except Exception as e:
        print(f"{i}. error: {e}")

driver.quit()

# Step 2: Connect to Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("projectdaraz").sheet1

# Step 3: Update data in Google Sheet
sheet.clear()

df = pd.DataFrame(data)
sheet.insert_row(df.columns.tolist(), 1)

for index, row in df.iterrows():
    sheet.insert_row(row.tolist(), index + 2)

print("✅ Daraz data saved to Google Sheets!")
