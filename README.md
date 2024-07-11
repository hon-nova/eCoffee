# 0. Introduction

1. As a coffee enthusiast, the project theme was born: the eCoffee website offers an online shopping experience. Utilizing Django classes and models, the platform integrates robust features such as user authentication, a customizable shopping cart, and secure payment processing via Stripe. Users can track their favorite coffee products. To simulate a realistic scenario, the project also includes comprehensive admin capabilities for managing inventory and users' purchase history, making it viable in the digital marketplace.
  
2. I took on this project to tackle the complexities of e-commerce websites. It is crucial to create a smooth experience for users, making it easy to browse products and complete transactions. The website can generate detailed receipts and lets users check their purchase history. I'm passionate about full-stack development. Solving e-commerce challenges is like solving real business problems. This project highlights the importance of continually improving skills to build successful e-commerce solutions, which is my main focus in web development.

# 1. Distinctiveness and Complexity
## **Distinctiveness:**

   The distinctiveness of this website is demonstrated through the integration of various comprehensive features that go beyond basic e-commerce functionalities:

   1. Full-Stack Development: The project showcases a complete full-stack development approach, integrating frontend and backend components and the third party service seamlessly.
   2. Diverse Features: It incorporates multiple lessons and components learned throughout the course, such as commerce concepts, user authentication, database structures and dynamic content rendering. Specific features include:
      - Product Like/Unlike Option: Users can like or unlike products, adding an interactive element to the user experience
      - Stripe Payment Integration: Secure and reliable payment processing through Stripe, enhancing user trust and transaction safety
      - **User Purchase History**: Registered users can view their purchase history, providing a personalized shopping experience
      - **Admin Dashboard**: A visual admin interface that allows administrators to manage products, view sales data, and reports
  
## **Complexity:**


   The project’s complexity is evident through the following advanced features and implementations:
   1. **Sales Reporting**: The website includes functionality to generate detailed sales reports, accessible through the admin dashboard. This feature leverages data aggregation and visualization techniques to provide insights into sales performance.
   2. User Profiles and Orders Management: The site allows users to view all past orders, integrating complex querying and data retrieval processes.
   3. Custom User Authentication: Implementation of a custom user authentication system using AbstractUser, enhancing security and allowing for extended user functionalities.
   4. Cart and Order Management: The project includes comprehensive cart and order management systems, enabling users to add items to their cart, adjust quantities, and proceed to checkout seamlessly.
   5. Responsive Design: The frontend is designed to be fully responsive with Bootstrap support features, ensuring a smooth user experience across different screen sizes.
   
# 2. File Contents: .html, .py, .js Extensions

### html:

A) User Route:

0. `layout.html`:
   
     - Template Inheritance: It sets up blocks that other templates can inherit using {% extends "eCoffee/layout.html" %}. This allows consistent structure and styling across multiple pages
     - Navigation Bar: Includes a navigation bar that provides links to various routes:
         - eCoffee: Likely the homepage or main section of the website
         - Login: Link to the login page for user authentication
         - Register: Link to the registration page for new users
         - Profile: Link to the user's profile page for managing personal information
         - Cart Icon: Displays an icon associated with the user's cart, showing the total number of items currently in the cart. This allows quick access and visibility of cart contents
  
1. `index.html`   
     - displays the intro. page of the eCoffee website

2. `home_products.html` 
     - Displays all products currently in the system
     - Adds a checkbox functionality to filter products as desired
     - Includes the pagination functionality at the end of the page
3. `cart.html`
     - Displays Selected Items: It lists all selected items from the user's cart, allowing them to increase, decrease quantities, or remove items entirely
     - Dynamic Updates: Based on user interactions (increasing, decreasing quantities, or removing items), the page dynamically updates the sub-total, taxes, and total amounts to reflect these changes
     - Checkout Button: It provides a prominent "Continue to Checkout" button, enabling users to proceed to payment services, indicating readiness to complete their purchase
4. `create_checkout_session.html`
     - The file includes a script tag that initiates the process for a user to checkout and make a payment for their selected items. This tag triggers the Stripe template sheet for payment, sets up a click handler for a checkout button, sends a POST request to create a Stripe checkout session, and then redirects the user to the Stripe Checkout page. It also handles errors by logging them and redirecting the user to a failure page
     - Session parameters contain
         - Line items: Products being purchased
         - Payment details: Amount to be charged, currency, total items in cart
         - Success and failure URLs directions 
     - Return Session ID: Sends back the session ID or URL to the client-side, typically as a JSON response   
   
5. `success_transaction.html`
     - Displays a success transaction message and allows user to go back to HomePage
6. `failure_transaction.html`
     - Displays a reason for a failure transaction and leads user back to the HomePage
   
7. `product_details.html`
     - Shows the product information in greater details
     - Allows user to add the item; increase, decrease the number of the particular item; or remove all of them at once
8.  `profile.html`
     -  Mainly displays the info all of the items which were purchased based on `order_id` including amount paid for the order
    
B) Admin Route: 

1. `main_dashboard.html`
      - contains all sections of the admin route, encompassing admin dashboard, admin products and admin user pages for convenient navigation
      - adds a script tag that utilizes `chart.js` for generating a sales report chart
  
2.  `admin_products.html` 
      - displays all current products encompassing the CRUD operations 
      - adds Pagination functionality at the end of the page
3.  `admin_user.html` 
      - shows all registered users excluding the admin user

### py:
1. `admin.py`:
      - This file registers the `User, Product, Cart, CartItem, Like, Order,OrderItem, and OrderAdmin` models with the Django admin site. As a result, these models can be managed via the Django admin interface, allowing administrators to view, add, modify, and delete instances of these models through a web-based interface
      - The `OrderAdmin` class is created in this file that is used to manage how the model `Order` is diplayed and importantly will be customised in the Django admin interface. The fields selected are `'cart', 'payment_status', 'placed_order_at', 'payment_intent_id', 'amount'`
  
2. `context_processors.py`
      - Defines a context processor function `send_cart_length` that provides cart-related information to all **templates**. Specifically, it adds the total number of items in the cart (cart_length) and the total price of the items in the cart (total) to the context. This function is registered in the settings.py as follows
  
      ```python
            ...
            'context_processors': [
                ...
                'eCoffee.context_processors.send_cart_length'
            ],
      ```
3. `forms.py`
      - The forms.py file defines a:
         -  `ProductForm`class that inherits from forms.ModelForm. This form is used to create or update instances of the Product model

         - The Meta class within ProductForm specifies that the form is based on the Product model. The form includes the fields `description, category, price, quantity, and photo_url` from the `Product` model. The Django form itself serves as a `Constructor` of the `Product` class

         - `OrderForm` class is used to create a custom form for the Django admin interface specifically to allow for a customizable placed_order_at field for testing sales report purposes
         - The Meta class includes all fields `(fields = '__all__')` from the Order model
  
4. `models.py`

      - `User`: Extends AbstractUser with no additional fields
      - `Product`: Represents a product with a description, category (choices provided), price, quantity, photo URL, and creation timestamp
      - `Like`: Tracks which users like which products, with a unique constraint on the user-product pair
      - `Cart`: One-to-one relationship with User, includes methods to get total items and total price
      - `CartItem`: Represents items in a cart, linked to Cart and Product, with a quantity field
      - `Order`: Is linked to Cart, includes fields for payment status, order placement timestamp, payment intent ID, amount, and a method to get the total payment
      - `OrderItem`: Is linked to CartItem, includes all info about the purchased items. The model is used to saved all purchased items for each order and to retrieve for later review
5. `urls.py`
      This urlpatterns list defines the routing paths for URLs in a Django application:

  
   |       url                 | description                                                         | 
   |     --------              | ----------                                                          | 
   |         ''                | Points to `views.index` for the root URL, typically the homepage       | 
   | "accounts/login/"         | Links to `views.login_view` for user login functionality        |
   | "logout"                  | Connects to `views.logout_view` for user logout        | 
   | "register"                |  Routes to `views.register` for user registration |
   | "coffee_admin"            |Directs to `views.main_dashboard` for the main administrative dashboard|
   | "coffee_admin/products"   |Maps to `views.admin_products` for managing products in the admin dashboard|
   | "get_product/<int:product_id>"|Fetches a specific product using `views.get_product` based on its ID|
   | "coffee_admin/users"      |Points to `views.admin_users` for viewing user accounts in the admin dashboard|
   | "home_products"           |Points to the products page                   |
   | "delete_product"          |Routes to `views.delete_product` for deleting a product|
   | "product_details/<int:product_id>" | Shows details of a specific product using `views.product_details`|
   | "save_product"            | Connects to `views.save_product` for saving product details|
   | "cart_items"              | Links to `views.cart_items` for managing items in the shopping cart|
   | "cart/<int:product_id>"   | Adds a product to the cart using `views.add_to_cart` based on its ID|
   | "cart_items/<int:item_id>"|Deletes an item from the cart using `views.cart_delete_item` based on its ID |
   |"update_cart_item/<int:product_id>" |Updates the quantity of an item in the cart using `views.update_cart_item` based on its ID|
   | "create_checkout_session/"| Initiates a checkout session using `views.create_checkout_session`|
   |"success_transaction/" |Displays a success message for a completed transaction using `views.success_transaction` |
   | "failure_transaction/"| Displays a failure message for a failed transaction using `views.failure_transaction`|
   | "profile/<int:user_id>"| Shows the profile of a user using `views.profile` based on their ID|
   | "likes/<int:product_id>"| Handles toggling of product likes using `views.toggle_like` based on the product's ID|
   |"webhook/"                | Handles webhook events from Stripe using `views.stripe_webhook`|
   |"api/sales-data/"|Handles sending data from Django backend to the frontend event using `views.sales_data`|

6. `views.py`
      - The views.py file in a Django application serves as the backbone, defining various view functions that handle different aspects of the application's functionality. Each view function is responsible for processing requests, interacting with the database through models, and rendering appropriate responses or templates to users. All functions are defined as follows: 
  

      |Name|Function|Description|
      |----|--------|------------|
      |Index View|`index`|Renders the homepage of the application| 
      |**Authentication Views**||
      |Login View|`login_view`|Handles user authentication and renders the login page|
      |Logout View|`logout_view`|Logs out the user and redirects to the homepage|
      |Register View|`register`|Manages user registration and renders the registration form|
      |**Admin Dashboard Views**||
      |Main Dashboard|`main_dashboard`|Renders the main administrative dashboard|
      |Admin Products|`admin_products`|Manages products within the administrative interface|
      |Admin Users|`admin_users`|Manages user-related tasks within the administrative interface|
      |**Product Views**||
      |Get Product|`get_product`|Retrieves and displays details of a specific product|
      |Delete Product|`delete_product`|Deletes a product from the database|
      |Product Details|`product_details`|Shows detailed information about a product|
      |Save Product|`save_product`|Handles the creation or update of product information|
      |**Cart Views**||
      |Cart Items|`cart_items`|Manages items in the user's shopping cart|
      |Add to Cart|`add_to_cart`|Adds a product to the user's cart|
      |Cart Delete Item|`cart_delete_item`|Removes an item from the user's cart|
      |Update Cart Item|`update_cart_item`|Updates the quantity of an item in the user's cart|
      |**Checkout Views**||
      |Create Checkout Session|`create_checkout_session`|Initiates a checkout session for payment processing|
      |Success Transaction|`success_transaction`|Displays a success message after a successful transaction|
      |Failure Transaction|`failure_transaction`|Displays a failure message after an unsuccessful transaction|
      |**Profile View**|`profile`|Renders and manages user history purchases information|
      |**Like View**|`toggle_like`|Handles toggling of product likes by users|
      |**Webhook Terminal**|`stripe_webhook`|Handles webhook events from Stripe for payment notifications and updates|
      |**Sales Report**||
      |Get Monthly Sales|`get_monthly_sales`|Returns a list of dict representing the sales data grouped by month|
      |Sales Data|`sales_data`|Sends a `JsonResponse` data object to the frontend|
### js:
1. `index.js`
      - There are a few functionalities:
         - First, one script is responsible for handling the `like` functionality on an e-commerce website. When a user clicks a like button for a product, it sends a request to the server Django to update the `like` status. Depending on the response, it updates the UI to reflect whether the product is liked or not by toggling a liked class on the corresponding `heart` icon. The script includes error handling to log any issues that occur during the process.
         - Second, a function call `getSalesData()` that is used for:
            - fetching monthly sales data from `/api/sales-data` backend Django
            - rendering a Chart.js bar chart (myChart) on main_dashboard.html using fetched data
            - using JavaScript to dynamically update the chart with monthly sales data
# 3. How to run the application
1. Create a virtual environment named as final_env: 
   ```python
   $ pip -m venv final_env
   ```
2. Activate the virtual environment: 
   ```python
   $ source ./final_env/bin/activate
   ```
3. Direct to your current working directory, then clone this app: 
   ```python
   $ git clone https://github.com/hon-nova/eCoffee
   ```
4. Start the Django development server by executing the command:
   ```python
   $ python3 manage.py runserver 8000
   ```
5. After making changes with database in models.py, update the database by running:
   ```python
   $ python3 manage.py makemigrations eCoffee
   $ python3 manage.py migrate
   ```
6. Create a Django admin user
   ```python
   $ python3 manage.py createsuperuser
   ```
7. Use `pip` to create a requirements.txt file: 
   ```python
   $ pip freeze > requirements.txt
   ```
# 4. Additional information about the project

0. The package for security & deployment purposes
   
   ```python   
   $ pip install python-dotenv
   ```
1. To validate the admin person, the library support is as follows
   ```python
   from django.contrib.auth.decorators import user_passes_test
   ```
2.  For the security reasons, all tokens and secret keys are stored in the `.env` file and the function `load_dotenv()` in `settings.py` is used to apply them
3.  For deployment purpose into Neon Cloud Service Provider, install
    ```python
    $ pip install dj-database-url
    $ brew install neonctl
    
    ```
  
# 5. Python Libraries used:
   0. Bootstrap libraries for collapsible task, `chart.js` and `Stripe` libraries
   ```js
      <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>

      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

      <script src="https://js.stripe.com/v3/"></script>
   ```   
   1. Install Stripe
      ```python
      $ pip install stripe
      ```
   2. Install Stripe CLI globally
      ```python
      $ brew install stripe/stripe-cli/stripe  
      ```
   3. Run your terminal shell to get the Stripe webhook secret(s)
      ```python
      $ stripe login
      $ stripe listen --forward-to localhost:8000/webhook/
      $ stripe listen --forward-to localhost:8000/success_transaction/
      $ stripe listen --forward-to localhost:8000/failure_transaction/
      ```
   4. Stripe Event Packages
      ```
      payment_intent.succeeded
      payment_intent.payment_failed
      ```
      **__Use Cases__**
      **success**

      ![success](./eCoffee/static/eCoffee/demo/success_transaction.png)

      **failure**
      ![failure](./eCoffee/static/eCoffee/demo/failure_transaction.png)
   5. Install `celery`, `redis`
      ```python
      $ pip install celery redis

      ```
# 6. Agile User Stories:
1. As a visitor, I can surf the website and look for products that I want
2. As a registered user, I can
   - Save items in my cart for future purchase
   - Remove unwanted items from my cart
   - Add items to my cart
   - Make online transactions
   - View all items in my cart before making a transaction   
   - Review my purchase history
   - Indicate preferences by liking or disliking a product
3. As an admin user or a general manager, I can
   - View the visual sales report Dashboard
   - Access and view all current registered users' purchase history and their account information (excluding passwords)
   - Perform all CRUD (Create, Read, Update, Delete) operations on products

# 7. Tech Stack:
   0. JavaScript
   1. The DOM
   2. CSS
   3. ChartJS
   4. Django's ORM
   5. Django Rest Framework (DRF) for APIs
   6. Sqlite3

# 8. Constraints:   
1. The project does not contain nor implement a 'forgot password' feature. In case users encounter this situation, they are advised to contact the Django admin person for further instructions
<hr/>

# Thank you
