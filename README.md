# deploy

I improvised a deployment with docker and docker-compose. (not docker db persistance)
I didn't mess with continuous integration for now. 

~~~
docker-compose up web
~~~

or

~~~
python manage.py migrate
python manage.py loaddata apps/users/fixtures/users.json
python manage.py runserver 0.0.0.0:8000
~~~


## password

bigboss@giuseppi.com default user  
all default users have y4v4J3cWbw password

# Notes about the design

django has multiple ways for write a view, the most simplest is the function view, the intermediate level is a class view, and "recently" it have the generics views, that is the top abstraction layer.

to this layer I have added a permission functionality based on "rest-framework generics"

I have chosen this layer just to show that I have a deep understanding of django.


## login and logout

why to implement if django already have it in django.contrib.auth.views ?

## confirmation messages

i do it in the simplest way with django.contrib.messages


## password strong

django.contrib.auth.password_validation already validate that password is strong

## UX / UI

I did not strain on the UI, as it is not my strong suit. about the UX, well, I think it's a generic UX of any crud interface