import threading
import time
from django.db import connection
from .extended_views.add_product import scrape_data
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = 'pricetracker2024@gmail.com'
my_thread = None
timestamp_file = 'last_checked.txt'
CHECKING_TIME = float(5*60*60)

def read_last_checked():
    try:
        with open(timestamp_file, 'r') as file:
            last_checked = float(file.read().strip())
        return last_checked
    except (FileNotFoundError, ValueError):
        return None  # If file doesn't exist or is empty
    
def write_last_checked():
    with open(timestamp_file, 'w') as file:
        file.write(str(time.time()))  # Store current timestamp in seconds

def periodic_check():
    print("Thread started!")
    last_checked = read_last_checked()
    if last_checked is not None:
        time_difference = time.time() - last_checked
        print(f"Last timestamp: {last_checked} Time difference: {time_difference}")
        if time_difference < CHECKING_TIME:
            time.sleep(CHECKING_TIME-time_difference)
    while True:
        all_fail = check_prices()
        if all_fail:
            time.sleep(60)
        else:
            time.sleep(CHECKING_TIME)
        
def check_prices():
    
    #models are not ready when the thread is started so only import them when they are necessary
    from .models import Product, ProductPrice, UserInterest

    data = Product.objects.all()
    print(f"Fetched {data.count()} records")
    all_fail = True

    for product in data:
        try:
            price, name, image = scrape_data(product.url)

            #Sleep for a bit so emag doesn't  detect us as a bot
            if price is None:
                print(f'Failed to get price for {product.name}')
                time.sleep(10)
                continue
            all_fail = False
        
            print(f"Got price for {product.name}: {price} RON.")
            #Last price from the database scraped at last run of the check function
            last_price= None

            try:
                #From product price database we select the entries for the current product that we are processing, 
                #sort them descending by timestamp and get the first entry
                last_price = ProductPrice.objects.filter(product=product).order_by('-timestamp').first()
            except Exception as error:
                print(f"Could not get last price for product: {product.name}, Exception: {error}")

            #New logic, create price entry anyway so there's more data in database
            ProductPrice.objects.create(product=product, price=price)

            if last_price is None:
                time.sleep(15)
                continue
            print("Last price: " + str(last_price.price) + " RON.")

            #Old logic, only insert price entry if it's different from the last one
            #if last_price is None #or not math.isclose(last_price.price, price, rel_tol=1e-9):
               # print(f"Inserted price in database: {price}")
                
            if last_price.price > price:
                users = UserInterest.objects.filter(product=product, notify = True)
                for interest in users:
                    receiver_email = interest.user.email
                    username = f"{interest.user.first_name} {interest.user.last_name}".strip() or interest.user.username
                    send_email(receiver_email, username, product.name, price, product.image_url)

            time.sleep(10)

        except Exception as e:
            print(f"Error in thread: {e}")
    if not all_fail:
        write_last_checked()
    return all_fail

#pricetracker2024@gmail.com
    

def start_thread():
    global my_thread
    # Check if the thread is already started and running
    if my_thread is not None and my_thread.is_alive():
        print("Thread is already running!")
        return

    # If not, start a new thread
    my_thread = threading.Thread(target=periodic_check, daemon=True)
    my_thread.start()
    #send_email('alexa.nedelcu8@gmail.com', 'alexa', 'Cana model pisica Edream, Sticla termorezistenta borosilicata, 250 ml', 35.00, 'https://s13emagst.akamaized.net/products/38782/38781562/images/res_514242a60683e0b5098656bbf0e7de50.jpg' )
    
def send_email(receiver_email, username, product_name, price, image):
    subject = "The price of a product you're interested in has dropped!"
    body =  f"<html> <body> <p> Hello, {username}! </p>"  
    body += f"<p> The price of {product_name} has dropped to {price} RON! </p>"
    body += f'<img src="{image}" alt="Image" style="width:300px;">'
    body += f"<p> If you'd like, you can log into your account to see how the price has been fluctuating lately. </p> <br>"
    body += f"<p> Your sincerely, <br> The Price Tracker Team </p></body></html>"

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    print(f"Sender Email: '{sender_email}'")
    print(f"Receiver Email: '{receiver_email}'")

    # Add body to email
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    # Set up the SMTP server (using Gmail's SMTP server)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use 465 for SSL

    # Login to the server using your email and password
    smtp_username = 'pricetracker2024@gmail.com'
    smtp_password =  'loyi qlvy kmrl toiz'                              
    #loyi qlvy kmrl toiz

    # Establish a connection to the server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()
