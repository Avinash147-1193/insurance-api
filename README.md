
## Instalation
 `git clone` this repository to your machine, if you want to make any changes to the code.

## Create virtual environment and activate
from terminal go to project directory and run `virtualenv venv`,
follow this for details:  https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/
Ubuntu: `source venv/bin/activate` windows: `venv/Scripts/activate`

### Running the project

To install all dependencies on the virtual environment, run `pip3 install -r requirements.txt`.

### Running tests

Once inside the image's shell, run `python manage.py test`.

#### Start Django development server (local)

`python manage.py runserver 127.0.0.1:8000`

#### Create database migrations file

`python manage.py makemigrations`

#### Run migrations

`python manage.py migrate`