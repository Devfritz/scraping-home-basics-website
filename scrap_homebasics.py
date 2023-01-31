import requests
from bs4 import BeautifulSoup
import json
import csv


class HomeBasicsProduct:
    def __init__(self, Sku, VendorItemNo):
        self.Sku = Sku
        self.VendorItemNo = VendorItemNo


csv_file_name = 'homeBas-1.csv'
data_home_basic = []
allData = []
with open(csv_file_name) as file:
    reader = csv.DictReader(file)
    for row in reader:
        item_homeB = HomeBasicsProduct(row['No.'], row['Vendor Item No.'])
        data_home_basic.append(
            {'sku': item_homeB.Sku, 'VendorItemNo': item_homeB.VendorItemNo})


for item_homeB in data_home_basic:

    try:
        vendor_itemNO = item_homeB['VendorItemNo']
        url = "https://shophomebasics.com/products/"+vendor_itemNO
        # # get data from home basics
        response = requests.get(url)
        if response.status_code:
            print(response.status_code)
            # get response to format to text
            html = response.text

            bSobj = BeautifulSoup(html, "html.parser")
            product = bSobj.find(
                "div", {"class", "clearfix product_form init"})

            product_data = product.attrs['data-product']

            data = json.loads(product_data)

            #  get description
            des = bSobj.find("div", {"class", "description"})
            des_P = '<p>' + des.find("p").get_text() + '</p>'

            # description with ul
            des_lst = des.findAll("li")
            last = len(des_lst) - 1
            short_des = des_lst[0:last]
            shortFull = ""

            for item in short_des:
                shortFull = shortFull + '<li>' + item.get_text() + '</li>'
                print(item)
                product = {
                    'sku': item_homeB['Sku'],
                    'title': data['title'],
                    'description': des_P + "</br> <ul>" + shortFull + "</ul>",
                    'images': data['images']

                }
                allData.append(product)
            alt_img = 0
            for img in product['images']:
                format_url = 'https:' + img
                response2 = requests.get(format_url, stream=True)
                if response2.status_code:
                    name = str(item_homeB['Sku']) + ".jpg" if not alt_img else str(item_homeB['Sku']) + \
                        "_" + str(alt_img) + ".jpg"
                    with open(name, 'wb') as fileImg:
                        fileImg.write(response2.content)
                        alt_img = alt_img + 1

    except:
        continue


print(allData)

