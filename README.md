# theLineMedia
#### Video Demo:  <https://youtu.be/Cpi_4vbnRqoE>
## Objectives and work in general:
The idea for this project originated from lecture 8 while David discussed web applications and such,
where the main objective with this was to unify websites that provided some kind of list to keep track
of content that you consumed, be it movies, books or anime. Considering the amount of applications doing the same thing,
I thought how useful would it be to have some kind of main list, that encompasses all kinds of media, while keeping
the order untouched. My personal way of consuming media is that I always have to finish the first thing added to my list,
similar to a FIFO algorithm, and that's the origin for the name of my application and itsmain purpose overall, since in my experience,
I have yet to find a list website that easily keeps track of the first thing you added to your list that hasn't yet been consumed.
Though this website would require some knowledge of media in general, what is implemented here is only the core functionality, while things like title pages and third party databases could be added in the future.

## Files:
In this section Im going to go over each file in my project folder, detailing its use, but the main course for the functionality
of it is going to be in the next section.

### Static Folder:
Here I added two files, styles.css, which I used to keep some css code, an admittedly low amount of it, since this wasn't the main focus
of my program neither the CS50 course went into much detail about how to make a website pretty. Navbar function -> https://www.w3schools.com/css/css_navbar.asp

The other file here is a png that I made myself, to use as a logo for my website. Honestly, if I wasn't so bad at drawing, maybe it would look
decent, but I dare say its a good idea.

### Templates Folder:
This is where the html part of the web application goes, and my application contains 6 pages overall and 7 files, one being the layout.
The first one is my error.html page, a very simple one based on the apology page used in the finance problem of PSET9, where everything that goes wrong for the part of the user ends up.
Messages displayed on it are sent by the main application, but that's it for functionality.
The next file is my main page, index.html, which displays the logo along the main use for the site, which would the line of media to be consumed, displaying the next thing you should consume,
and a skip button, if you really don't want to consume it.

My layout.html is the file used for storing the base used in the website. On it there is a basic navigation bar based on the one used in Finance, which contains 4 tabs while logged in, they are "Line", my homepage, "List", containing the list and an add function, "Remove", which is used for removing an item from the list, and a log out page, which just logs you out and redirects you to the log in page. While logged out, there are register and log in options in the navbar, and it also highlights the current page you are on.

List.html is a dynamic html file that changes based on the user. It shows the list of the user and an add function, used to add items to your list, based on the title and genre.
Register.html and Login.html are pretty similar to the implementations used in the Finance problem, where they serve to manage your sessions while using the site. The main difference
here is that my register page uses a filter in the password field that requires the user to provide a password containing symbols, uppercase and lowercase characters and numbers while keeping it 8 or more characters long.

Lastly, remove.html is the page used for removing an item from the list, simple use but actually really complex implementation. I thought it to be silly if you needed to type exactly what was in your list, but also didn't have the knowledge to do some kind of smart system, so I did 2 select fields, where the first one dictates what is on the second one. You select the genre of the media
you want to remove in the first select, and the second select will show you all the media from that genre in your list. Took a lot of work to get it working, but it's now complete.

### App.py:
This is where the code is store, comprising 137 lines of code, using Flask and a bunch of libraries introduce in the CS50 course, a lot of it is very based on what was shown during
the classes, but it was also all written by myself. The only thing I needed to use from other sources is the hash function, from "werkzeug.security" and the login required function
also used in Finance which belongs to "https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/".

### project.db:
This is the SQL database used for storing users names and passwords and their respective lists. They are really basic, with only two tables, since I'm not using third-party databases or anything,
theses two tables are for storing users and their lists.

## In-depth Code:
In this section I'm going to go over the website step-by-step on how a user would use the site while explaining the code behind it.

First of all, the user needs to register, and this is done through the register page, which the user can select via the navbar on top. In this page, like in Finance, the user needs to type
their username, password and confirmation password. The password field requires them to use 8 or more characters, containing uppercase and lowercase letters, numbers and special symbols. This is done through a named parameter called pattern, which is coded to require these atributes from the text in the input box. Next, the fields are done in a form html field, that will be submited after they press the button to a link called /register.

In app.py, all the register function does is receive the input from the user, check if there really is anything written there at all and if the user has a nickname that was already taken.
After that, it inserts the data into the users table, which contain a special field called id, handled automatically by SQL, where it increments by one everytime a new row is added, to ensure
each user has a different id. The passwords inserted into the table are also hashed, to keep some level of security.

However, the register function does not actually starts a session, so after creating a profile, the user needs to reinsert their username and password in the login page, done in a form,
sending the info the log in function. This one checks if the username and password sent matches with the ones stored in the users table, and if nothing goes wrong, the session is started,
by storing the user id into it.

Next, the individual will now add something to ther empty list, which can be select via the navbar on top of the site, which now has more options since the user logged in. This is done via an if
clause in my layout.html, which changes the options in the navbar based on if the user is logged in or out, and also has a for loop, iterating over the links in theses options to find the
current page the user is in, and when it finds the right page, that section of it is featured in red.

The list page features an add function, which is done via a form section using a text box similar to the ones used in register and login pages, while also containing a select section, which contains fixed genres that the user can choose. When they write something and send to the server, the list function will check to see if the title is already on the list, and if it's not,
it will be inserted into the list tables, containing the genre, title and user id. The list table is also designed to keep track of the time in which each row was added, to ensure the order
at which to display each entry in the homepage. When the user enters the list page with some entries, it will show the entire user's list, while keeping the add option on the bottom of the page,
so this page is dynamic and changes based on what is on the current user's list. This is done through the list function sending a list of dictionaries to the page, containing the user's list, and jinja used on the html of the page, to receive the print, iterate over each element, and display it.

Now, the user can go into the homepage and below the beatiful logo displayed, the next title that needs to be consumed. This page was actually pretty simple, but the hard part was adding the next button, this was done by the index function sending the page the current user's list in ascending order of time, via a sql query. Next, a javascript code modifies an object with the id of display, initially containing nothing, and it basically works like a for loop, but it only increments the I variable when the button is clicked, and sends the element to the display object.

Finally, the remove function. This one is actually pretty simple by the app.py part. It receives the user's input of genre and title, checks to see if that row really exists and belongs to the user, and then removes it. The html side, on the other hand, is pretty complex, comprising two select parts of the form, the first one is the genre field, which, when selected, sends a query
to the server, in the get options function, receiving the genre as an argument, and returning a list of dictionaries containing the user's list of entries with that genre. Then, the script proceeds to read that list, converts it to json, iterates over every element of it while creating an option field, using each element values to populate both the option's title and value, and then appends the newly created option field to the secondSelect field created beforehand. There is also a logout function, all it does is end the session created on login.

## Conclusion:
While the project itself is quite simple, I  daresay it's an interesting idea overall, being able to see the media you want to watch in order, while also keeping it all on a
single site. The implementation here is basic, there is little to no use of CSS at all, so the site looks pretty rough, but it works as intended and utilizes most of what was
taught during the course, overall I'm pretty happy with the results and what was learned in the process of making it.


