import requests
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText

import os
from dotenv import load_dotenv

load_dotenv()

def check_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = 'Item name not found'
    price = 'Price not found'
    in_stock = False

    # title
    title_element = soup.find('h1', class_='product-template__body--title')
    if title_element:
        title = title_element.text.strip()

    # price
    price_element = soup.find('div', class_='costco-price')
    if price_element:
        price_span = price_element.find('span')
        price = price_span.text.strip()
    
    # stock
    stock_element = soup.select_one('.quantity-add-to-cart input[type="submit"]')
    if stock_element:
        stock_status = stock_element['value']
        in_stock = 'add to cart' in stock_status.lower()

    return {
        'title': title,
        'price': price,
        'stock': in_stock
    }

def send_email(subject, body, to_email):
    from_email = os.getenv('FROM_EMAIL_ADDRESS')
    if not from_email:
        raise ValueError('FROM_EMAIL_ADDRESS environment variable not set.')
    
    password = os.getenv('FROM_EMAIL_PASSWORD')
    if not password:
        raise ValueError('FROM_EMAIL_PASSWORD environment variable not set.')

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    smtp_server = os.getenv('SMTP_SERVER')
    if not smtp_server:
        raise ValueError('SMTP_SERVER environment variable not set.')
    smtp_port = os.getenv('SMTP_PORT')
    if not smtp_port:
        raise ValueError('SMTP_PORT environment variable not set.')

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print('Email sent successfully!')
    except smtplib.SMTPAuthenticationError as e:
        print(f'SMTPAuthenticationError: {e}')
    except Exception as e:
        print(f'Error: {e}')

def main():
    update = False 

    # add product URLs here
    urls = [
        'https://costco.bysophieofficial.com/products/dr-althea-345-relief-cream-50ml', 
    ]

    to_email = os.getenv('TO_EMAIL_ADDRESS')
    if not to_email:
        raise ValueError('TO_EMAIL_ADDRESS environment variable not set.')

    body = ''
    for url in urls:
        info = check_info(url)
        if info['stock']:
            body += f'<ul><a href="{url}">{info["title"]}</a> is now in stock for {info["price"]}</ul>'
            update = True
        else:
            body += f'<ul><a href="{url}">{info["title"]}</a> is still not in stock</ul>'
    
    if update:
        subject = f'Sophie Alert'
        body += f'<ul>Please remember to remove items from the tracking list to stop receiving emails about in-stock items</ul>'
        send_email(subject, body, to_email)
    else:
        print('No new updates.')

if __name__ == '__main__':
    main()
