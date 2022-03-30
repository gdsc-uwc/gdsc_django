# Billbao (Codename:FlickBoutique) by Google Developer Student Clubs (University of the Western Cape)

## Information about directories

The project was codenamed as FlickBoutique, hence all project files use this codename.

### File structure:

- flickboutique - Contains all project files
    - /templates - Contains all HTML templates for the project
    - /forms.py - Contains all Django HTML
    - /models.py - Contains all Django models
    - /urls.py - Contains all the site's URLs
    - /views.py - Contains all views that process all HTTP GET and POST requests happening on the server.

- manage.py - Python program for managing or running the server


## How to run the project

This is a Django application, so you can either access the deployed version by going to [https://billbao.app], or by cloning this repository and running the command `python manage.py runserver` on the directory after installing all the required dependencies (refer to `requirements.txt`) and then visiting [localhost:8000] on your browser.

# Bugs noted by team
- After each push to the repository, the repo wipes all database data that was created via the deployed site.
- There is currently no way to process online payments, a placeholder view is used instead.

# Bugs and other issues noted from user feedback
- Users could not sign up using a phone number with a leading zero (this was fixed).
- There will sometimes be an exception that is thrown when clicking on the logo to return to the home page.
- There are no notifications given or sent when a message is sent between users.


