# Import the libraries
import requests
import json
from bs4 import BeautifulSoup, Comment

# The URL to scrape
url = "https://www.ebay.ca/sch/i.html?_fsrp=1&_from=R40&_nkw=graphics+card&_sacat=0&LH_ItemCondition=3000%7C2500%7C2030%7C2020%7C2010%7C2000%7C1500&_stpos=M5A2N3&_fcid=2&LH_PrefLoc=3&imm=1&rt=nc&Chipset%2520Manufacturer=NVIDIA&_oaa=1&_dcat=27386"

# Make the HTTP request and get the HTML response
response = requests.get(url)

# Check the status code
if response.status_code == 200:
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Create an empty list to store the scraped data
    data = []

    # Find all the product items on the page
    items = soup.find_all("div", class_="s-item__info clearfix")

    # Loop through each item
    for item in items:
        # Initialize an empty dictionary to store the item data
        item_data = {}

        # Extract the title using the class name "s-item__title"
        title = item.find("div", class_="s-item__title")
        if title:
            # Find all the elements with the class name "LIGHT_HIGHLIGHT"
            labels = title.find_all("span", class_="LIGHT_HIGHLIGHT")
            # Remove the elements from the title element
            [label.extract() for label in labels]
            # Get the remaining text from the title element
            item_data["title"] = title.text

        # Extract the item title using the class name "s-item__subtitle"
        subtitle = item.find("div", class_="s-item__subtitle")
        if subtitle:
            item_data["condition"] = subtitle.text

        # Extract the price using the class name "s-item__price"
        price = item.find("span", class_="s-item__price")
        if price:
            item_data["price"] = price.text

        # Extract the seller info using the class name "s-item__seller-info"
        seller = item.find("span", class_="s-item__seller-info")
        if seller:
            item_data["seller-info"] = seller.text

        # Extract the offer using the class name "s-item__price"
        offer = item.find("span", class_="s-item__purchase-options s-item__purchaseOptions")
        if offer:
            item_data["purchase-optpions"] = offer.text

        # Extract the link using the class name "s-item__link"
        link = item.find("a", class_="s-item__link")
        if link:
            item_data["link"] = link["href"]

        # Extract the condition using the class name "SECONDARY_INFO"
        #condition = item.find("span", class_="SECONDARY_INFO")
        #if condition:
        #    item_data["condition"] = condition.text

        # Extract the shipping cost using the class name "s-item__shipping s-item__logisticsCost"
        shipping = item.find("span", class_="s-item__shipping s-item__logisticsCost")
        if shipping:
            item_data["shipping"] = shipping.text

        # Extract the location using the class name "s-item__location"
        location = item.find("span", class_="s-item__location s-item__itemLocation")
        if location:
            item_data["location"] = location.text
        
        # Extract the item title using the class name "s-item__title"
        reviews = item.find("span", class_="s-item__reviews")
        if title:
            item_data["title"] = title.text

        # Append the item data to the data list
        data.append(item_data)

    # Save the data to a JSON file
    with open("ebay_data.json", "w") as f:
        json.dump(data, f, indent=4)

    # Print a success message
    print("Data scraped and saved to ebay_data.json")
else:
    # Print an error message
    print("Request failed with status code:", response.status_code)
