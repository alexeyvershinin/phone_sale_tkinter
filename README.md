# phone_sale_tkinter
Intermediate certification work on creating a Python desktop application using the tkinter library and a Postgresql relational database.

### Assignment for intermediate certification

It is necessary to develop a (console/desktop) application for the sale of phones. 

* The system must have the following roles: administrator and store visitor. To interact with the tables of users and phones, you can create separate modules. 

* Users have a footprint. attributes: full name, login, password, role, logical deletion (exist, with data type bool).

* Phones have a footprint. attributes: name, number of memory, number of RAM, processor.

* When the application starts, a menu with a choice of actions should be displayed: 1 – log in, 2 – register

* The user can log in with a username and password. The entered data is checked from the User table in the database. If the user does not logically exist (exist == false), then the user cannot log in.

* If the user has logged in as a visitor, the functionality of viewing available phones for purchase is available to him.

* If the user has logged in as an administrator, the functionality of adding products, deleting products, viewing user information, changing the role of the user is available to him.

* By default, all users are registered as visitors. The role of the visitor can only be changed by the administrator.

* Registration data: Last name, first name, patronymic, login, password.

* You should also add exception handlers and data validation.

### Screenshots of the application

main screen

![main_screen](screenshots/login_scr.png)

register page

![register](screenshots/register.png)

user page

![user page](screenshots/user_page.png)

phone page

![phone page](screenshots/phone_page.png)
