# Product-usage-flask-app

## How to run the code
The code uses pipenv for dependency management.

1. To run it the first time you'll need to create the virtual environment. To install the dependencies you can type:
> pipenv install

2. To activate the environment after successful installation of dependencies. Type:
> pipenv shell

3. If the app is being run for the first time the database will also need to be initialized. To properly initialize run:

> flask db upgrade

4. Once the environment has been activated. The app can be run by simply typing:
> flask run


## Run code through Docker
1. To build the Dockerfile. Run:
> docker build -t my-flask-app .

where my-flask-app can also be replaced by any other name of your choosing

2. To run the image. Run:
> docker run -d -p 5000:5000 my-flask-app

The name of the name of the image (my-flask-app) should match name provided in step 1 above
