import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

def scrape_dineout_data(Url):
    
    data = []
    
    url = f"{Url}"
    try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            print(f"Successful Scraping ")
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for the specific HTML tags that contain the restaurant info
            restaurants = soup.find_all('div', class_='restnt-main-wrap clearfix')

            for restaurant in restaurants:
                # Extract the restaurant's name
                name = restaurant.find('div', class_='restnt-detail-wrap').text 

                for rating_class in range(6):
                    rating_div = restaurant.find('div', class_=f'restnt-rating rating-{rating_class}')
                    if rating_div:
                        rating =rating_div.text.strip()
                        break  
                    else:
                        # If the rating div is not found, set rating to 'Not available'
                        rating = '0'
                name = name[12:]
                data.append([name, rating])

    except requests.exceptions.HTTPError as errh:
            # The code inside the 'except' block is executed if an HTTPError occurs
            print(f"HTTP Error:")
    return data

# Base URL for Dineout 
url = "https://www.dineout.co.in/chennai-restaurants/welcome-back?p=1"


scraped_data = scrape_dineout_data(url)


hotels = []
ratings = []


for item in scraped_data:
    hotels.append(item[0])    
    ratings.append(float(item[1]))
   

# Create DataFrame
df = pd.DataFrame({
    'Hotel Name': hotels,
    'Rating': ratings  
}, index=range(1, len(hotels) + 1))

df.to_csv('All_Restaurant_Details.csv', index=True)
high_rated_hotels = df[df['Rating'] >= 4]
high_rated_hotels.reset_index(drop=True, inplace=True)

# Save the filtered DataFrame to a new CSV file
high_rated_hotels.to_csv('Best_Restaurants_of_Chennai.csv', index=True)

# Open (or create) a CSV file with write permissions
with open('restaurants.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)  # Create a csv writer object
    writer.writerow(["Name", "Rating"])  # Write the header row

    # Loop through the list of restaurants
    for restaurant in scraped_data:
        # Extract the name
        name = restaurant[0][12:]
        # Extract the rating
        rating = restaurant[1]
        # Write a row with the name and rating
        writer.writerow([name, rating])