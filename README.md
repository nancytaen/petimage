# flask_jinja_app
This is a basic skeleton flask app coherent with the application factory model.
The app includes database setup which utilizes sqlalchemy ORM and blueprints to organize views directory. 
This app is ideal for medium to large sized application, or for anyone who like their code to be neat and well organized.

## Cloning the repository
Anyone is free to clone this repository to estbablish a basic flask-jinja application setup.
However, it is advised that you remove the venv directory inside the repository, and create your own virtualenv directory. 
Please activate your own virtualenv, and install all packages listed in requirements.txt by
```
pip install -r requirements.txt --no-index
```

Also note that you must create your own .flaskenv file, and add database uri for the file to run.
