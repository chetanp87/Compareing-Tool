from flask import Flask, render_template, request, redirect, url_for
import get_products
from get_products import ProductScraper,AmazonScraper,FlipkartScraper
import csv

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/search", methods=['GET', 'POST'])
def search_page():
    if request.method == "POST":
        search_query = request.form["nm"]
        search_query = search_query.replace(" ", "+")

        selected_rating_min = int(request.form['min_rating'])
        selected_rating_max = int(request.form['max_rating'])

        print(f"Selected rating range: {selected_rating_min} - {selected_rating_max}")

        selected_rating = 4
        if 'rating' in request.form:
            selected_rating = int(request.form['rating'])
            print(f"Selected rating: {selected_rating}")

        return redirect(url_for('results_page', str=search_query, min_rating=selected_rating))

    else:
        return render_template('search.html')
 
@app.route("/<str>")
def results_page(str):
    min_rating = request.args.get('min_rating', type=int, default=0)

    print("Received min rating in results page:", min_rating)  

    plist = []
    amazon_scraper = get_products.AmazonScraper(str)
    amazon_scraper.scrape()
    plist.extend(amazon_scraper.products)

    flipkart_scraper = get_products.FlipkartScraper(str)
    flipkart_scraper.scrape()
    plist.extend(flipkart_scraper.products)

    filtered_and_sorted_list = []

    min_price = 0
    max_price = 100000000

    for entry in plist:
        entry['price'] = (entry['price'].replace('₹', '').replace(',', ''))
        if ' ' in entry['price']:
            rate, garbage = entry['rating'].split(' ')
            entry['price'] = rate
        if (float(entry['price']) >= min_rating) and (float(entry['price']) <= max_price) and (
                float(entry['price']) >= min_price):
            filtered_and_sorted_list.append(entry)

    sorted_list = sorted(filtered_and_sorted_list, key=lambda x: x['price'])
    return render_template('results.html', result = str, products=sorted_list, min_rating=min_rating)


@app.route("/contact+us")
def contact_page():
    return render_template("contact_us.html")

def register(email, password):
    try:
        with open("users.csv", mode="a", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([email, password])
            return True  # Registration successful
    except Exception as e:
        print(f"Error occurred while registering user: {e}")
        return False  # Registration failed


def register(email, password):
    try:
        with open("users.csv", mode="w", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow([email, password])
            return True  # Registration successful
    except Exception as e:
        print(f"Error occurred while registering user: {e}")
        return False  # Registration failed

def login(email, password):
    with open("users.csv", mode="r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if row == [email, password]:
                return True
    return False



@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if login(email, password):
            return render_template('home.html')
        else:
            error_message = "Please check username and password again!"
            return render_template('index.html', error_message=error_message)

            # return "Please try again!"
    return render_template('index.html')



@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        cntu = cntl = cnts = num = 0
        error_message = None
        if password != password2:
            error_message = "Passwords do not match"
        elif len(password) < 8 or not any(c.isupper() for c in password) or not any(c.islower() for c in password) or not any(c.isdigit() for c in password):
            error_message = "Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter and one digit"
        else:
            # return render_template('index.html')
            register(email , password)
            return redirect(url_for('login_page'))
        
        return render_template('register.html', error_message=error_message)

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)


