# 1. Distinctiveness and Complexity
Defence: Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.
1. This project is an e-commerce website. The uniqueness of this website is that it includes all lesson contents combined such as: commerce, social network and email system.
2. Furthermore, it's added some new features such as: integration with a third-party Stripe payment; usage of prescriptive data analysis to display its trend of the popular products based on the dataset from the users's input
3. Complexity: Regarding its complexity, the website has included the automatic email sent to user when their transaction is a success. At this point, the Stripe payment transaction and the built email system must collaborate together to ship the end outcome.
   
# 2. What’s contained in each file you created.

1. `admin_product.html` 
  - displayed all current products encompassing the CRUD operations. 
  - added Pagination functionality at the end of the page
2. `admin_user.html` showed registered users excluding the admin person
3. `home_products.html` 
  - displayed all products currently in the system
  - added a checkbox functionality to filter out the products
4. 
# 3. How to run your application.
1. Create a virtual environment: `$pip -m venv final_env`
2. Activate the virtual environemnt: `source ./final_env/bin/activate`
3. Direct to your current working directory and run the command: `$python3 manage.py runserver`
# 4. Supplementary information about your project. 
1.  The email address the user used to register for this website is considered the main vehicle used for communication with this user by the admin or a sales person
2.  The app does use other Bootstrap libraries for collapsible task as shown
  ```js
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
  
  ```   
# 5. Python Libraries used:

 ```python
   pip install plotly
   pandas
   numPy
   pip install stripe
   pip freeze > requirements.txt

```
# 6. Agile User Stories:
1. As a visitor, I can surf the website and look for products that I want
2. As a registered user, I can
    -  save items in my profile for later purchase
    -  delete items that I no longer want
    -  add items into my cart
    -  view all items before and after making a transaction
    -  make an online transaction
    -  contact the sale persons via email in case I want to make a complain
    -  can talk to the chatbot regarding my current order status
    -  view my history purchase
    -  write a review
    -  have an option to like or not to like a particular product
3. As an admin person or a general manager/boss, I can
    - view all current registered users encompassing their history purchases and account info (except password)
    - view all available products
    - perform all CRUD operations on products
