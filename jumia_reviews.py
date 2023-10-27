from bs4 import BeautifulSoup
import requests
import pandas as pd

html_text = requests.get('https://www.jumia.com.ng/catalog/productratingsreviews/sku/OR537EA12BLZ8NAFAMZ/',
                         timeout=10).text
response = BeautifulSoup(html_text, 'lxml')
soup = BeautifulSoup(response.prettify(), 'lxml')
review_container = soup.find_all('article', class_='-pvs -hr _bet')
review_list = []

for reviews in review_container:
    review_topic = reviews.find('h3', class_='-m -fs16 -pvs').text.strip()
    review_body = reviews.find('p', class_='-pvs').text.strip()
    review_rating = reviews.find(
        'div', class_='stars _m _al -mvs').text.split()[0]
    review_date = reviews.find('span', class_='-prs').text.strip()
    name = reviews.find('span', class_='').text.strip().split()
    if len(name) <= 2:
        name.append('')
    customer_name = " " .join(name[-2:])
    review_dictionary = {
        "Customer Name": customer_name,
        "Review Topic": review_topic,
        "Review Body": review_body,
        "Rating (of 5)": review_rating,
        "Review Date": review_date
    }
    review_list.append(review_dictionary)

df = pd.DataFrame(review_list)
df.to_csv("Jumia_Reviews.csv", index=False)
print("fin.")
