# Billbao (Codename:FlickBoutique) by Google Developer Student Clubs (University of the Western Cape)

## Information about directories

The project was codenamed as FlickBoutique, hence all project files use this codename.

## Technologies used

- HTML, CSS and JavaScript
- Python with Django
- Bootstrap
- MS Azure for the server
- PostgreSQL for the database

### File structure:

- flickboutique - Contains all project files
    - /templates - Contains all HTML templates for the project
    - /forms.py - Contains all Django HTML
    - /models.py - Contains all Django models
    - /urls.py - Contains all the site's URLs
    - /views.py - Contains all views that process all HTTP GET and POST requests happening on the server.

- manage.py - Python program for managing or running the server

## How to run the project

You may either access the deployed version by going to [https://billbao.app](https://billbao.app), or by cloning this repository and running the command `python manage.py runserver` on the directory after installing all the required dependencies (refer to `requirements.txt`, or run `pip install -r requirements.txt`) and then visit [localhost:8000](http://localhost:8000) on your browser. However, it is recommended that the deployed version be used instead.

## Bugs noted by team
- After each push to the repository, the repo wipes all user data that was created through the deployed site.This was fixed by moving to using a PostgreSQL database instead of SQLite.
- There is unfortunately currently no way to process online payments (as yet), a placeholder view is used instead.

## Bugs and other issues noted from user feedback
- Users also noticed that they could not log in after we updated the site. This was fixed by moving to PostgreSQL.
- Users could not sign up using a phone number with a leading zero (this was fixed by adding the ability to parse phone numbers).
- Users would be redirected to a nonexisitent URL when clicking on the logo to return to the home page from the messages page. (This was fixed by changing the `href` tag of the link in the navbar.)
- There are no device notifications given or sent when a message is sent between users.

## Technical answers on competition questions
- Google technology used: Google Fonts. Google Fonts was integrated into the application to make using custom fonts clean and quick for business users, without them having to worry about uploading their own fonts to the server, which would take up time and space. They can use custom fonts provided that they are on Google Fonts as well.