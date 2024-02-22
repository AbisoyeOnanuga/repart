# Import the requests and json modules
import requests
import json
# Import BeautifulSoup for HTML parsing
from bs4 import BeautifulSoup

# Define the base URL and the query parameters
base_url = "https://www.ebay.ca/sch/i.html"
query_params = {
    "_dcat": "27386",
    "_fsrp": "1",
    "rt": "nc",
    "_from": "R40",
    "_nkw": "graphics card",
    "_sacat": "0",
    "Chipset%20Manufacturer": "NVIDIA|AMD",
    "LH_ItemCondition": "3000|2500|2030|2020|2010|2000|1500"
}

# Initialize the page number and the data list
page = 1
data = []

# Loop through the pages until the status code is not 200 or the page number is greater than 10
while True:
    # Add the page parameter to the query parameters
    query_params["_pgn"] = str(page)
    # Make the request and get the response
    response = requests.get(base_url, params=query_params)
    # Check the status code
    if response.status_code == 200:
        # Convert the response to HTML using BeautifulSoup
        html = BeautifulSoup(response.text, "html.parser")
        # Find all the list elements with the class name "s-item"
        items = html.find_all("li", class_="s-item")
        # Loop through each list element
        for item in items:
            # Initialize an empty dictionary to store the data
            item_data = {}
            # Extract the title using the class name "s-item__title"
            title = item.find("h3", class_="s-item__title")
            if title:
                item_data["title"] = title.text
            # Extract the subtitle using the class name "s-item__subtitle"
            subtitle = item.find("div", class_="s-item__subtitle")
            if subtitle:
                item_data["subtitle"] = subtitle.text
            # Extract the reviews using the class name "s-item__reviews"
            reviews = item.find("span", class_="s-item__reviews")
            if reviews:
                item_data["reviews"] = reviews.text
            # Extract the price using the class name "s-item__price"
            price = item.find("span", class_="s-item__price")
            if price:
                item_data["price"] = price.text
            # Extract the seller info using the class name "s-item__seller-info"
            seller_info = item.find("span", class_="s-item__seller-info")
            if seller_info:
                item_data["seller_info"] = seller_info.text
            # Extract the purchase options using the class name "s-item__purchaseOptions"
            purchase_options = item.find("div", class_="s-item__purchaseOptions")
            if purchase_options:
                item_data["purchase_options"] = purchase_options.text
            # Extract the shipping cost using the class name "s-item__logisticsCost"
            shipping_cost = item.find("span", class_="s-item__logisticsCost")
            if shipping_cost:
                item_data["shipping_cost"] = shipping_cost.text
            # Extract the location using the class name "s-item__Location"
            location = item.find("span", class_="s-item__Location")
            if location:
                item_data["location"] = location.text
            # Extract the quantity sold using the class name "s-item__quantitySold"
            quantity_sold = item.find("span", class_="s-item__quantitySold")
            if quantity_sold:
                item_data["quantity_sold"] = quantity_sold.text
            # Append the data to the data list
            data.append(item_data)
        # Increment the page number
        page += 1
    else:
        # Break the loop if the status code is not 200
        break

# Save the data list to a JSON file
with open("ebay_data.json", "w") as f:
    json.dump(data, f)
