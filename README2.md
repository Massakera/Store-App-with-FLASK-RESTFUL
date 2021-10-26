# Store-App-with-FLASK-RESTFUL

I've build this API to study REST and Flask restful. After the basic structure now i'm adding new features to advance my study. 

## Features Added:
- Serialization with Marshmallow and Flask marshmallow
- Email confirmation
- Postman documentation for tests (Doing).

## Structure of the API:

- ``api.py`` In app.py we'll initialize and configure our Flask application. We'll also set up our API resources. This file is the entry point to our REST API.
- ``db.py`` In this file we'll create our database Python object, so that other files can import it. All other files import the database variable from this file.
The reason for creating a separate file containing just this is precisely so it's easier to import, and to avoid Python's circular imports.

### Models

``models/item.py`` 

The ItemModel contains a definition of what data our application deals with, and ways to interact with that data. Essentially it is a class with four properties:

- ``id``;
- ``name``;
- ``price``; and
- ``store_id``.

``models/store.py``

The StoreModel is another definition of data our application deals with. It contains two properties:

- ``id``; and
- ``name``.

In addition, because every ItemModel has a store_id property, StoreModels are able to use SQLAlchemy to find the ones that have a store_id equal to the StoreModel's id. 
It can do that by using SQLAlchemy's db.relationship().

``models/user.py``

The UserModel is the final data definition in our API. They contain:

``id``;
``username``; and
``password``.

### Resources

Finally, the resource is what defines how clients will interact with our REST API. In the resource we can define the endpoints where clients will have to send requests, as well as any data they have to send in that request.
For example, we could define that when clients send a ``GET`` request to ``/item/chair``, our API will respond with data of an item called chair. That data could be loaded from our database.

If in doubt, read (When to define a Resource and when to define a Model)[/1_structure_of_api/structure_faq.html#when-should-i-define-a-resource-vs-a-model].

In addition, ``resources/item.py`` also defines an ``ItemList`` resource which can be used to retrieve multiple items at once via the API. 

``resources/store.py``

In a similar way to the ``Item`` resource, the ``Store`` resource defines how users interact with our API.

Users will be able to get stores, create them, and delete them. Similarly a ``StoreList`` resource is defined to retrieve all stores in our API.

``resources/user.py``

These resources are quite different from the other two because they do not only deal with creating and updating data in our application, they also deal with various user flows like authentication, token refresh, log outs, and more.
