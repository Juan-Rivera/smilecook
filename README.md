# smilecook
Recipe-sharing platform in which users can create accounts and share their own recipes with other users


Project structure:
```

.
├── migrations
|   ├── versions
|   |   ├── 06a629b95cbc_.py
|   |   └── da55315d0028_.py
|   ├── README
|   ├── alembic.ini
|   ├── env.py
|   └── script.py.mako
├── models
|   ├── user.py
|   └── recipe.py
├── resources
|   ├── recipe.py
|   ├── token.py
|   └── user.py
├── schemas
|   ├── pagination.py
|   ├── user.py
|   └── recipe.py
├── static
|   └── images
|       └── assets
├── .gitignore
├── README.md
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
└── utils.py

```

* migrations/ - holds migration database tables
* models/ - holds endpoints models
* resources/ - holds endpoints resources
* schemas/ - holds schemas for data validation
* static/ - holds images/assets for avatar upload feature
* app.py - flask application initialization
* config.py - holds config options for database
* extensions.py - holds database initialization
* requirements - holds all packages needed for project


## Running 

1. Clone repository.
2. pip install requirements.txt
3. Run app.py 

## Usage
### Recipe List Endpoints
GET localhost:5000/recipes

RESPONSE
```json
{
    "data": [
        {
            "description": "This is a lovely egg salad recipe.",
            "id": 1,
            "name": "Egg Salad"
        },
        {
            "description": "This is a lovely tomato pasta recipe.",
            "id": 2,
            "name": "Tomato Pasta"
        }
    ]
}
```
POST localhost:5000/recipes

REQUEST
```json
{
    "name": "Cheese Pizza",
    "description": "This is a lovely cheese pizza",
    "number_of_servings": 2,
    "cook_time": 30,
    "directions": "This is how you make it"
}
```
RESPONSE
```json
{
    "id": 3,
    "name": "Cheese Pizza",
    "description": "This is a lovely cheese pizza",
    "number_of_servings": 2,
    "cook_time": 30,
    "directions": "This is how you make it"
}
```

### Recipe Endpoints
GET localhost:5000/recipes/3
```json
{
    "id": 3,
    "name": "Cheese Pizza",
    "description": "This is a lovely cheese pizza",
    "number_of_servings": 2,
    "cook_time": 30,
    "directions": "This is how you make it"
}
```

PUT localhost:5000/recipes/3

REQUEST
```json
{
    "name": "Lovley Cheese Pizza",
    "description": "This is a lovely cheese pizza",
    "number_of_servings": 3,
    "cook_time": 30,
    "directions": "This is how you make it"
}
```
RESPONSE
```json
{
    "id": 3,
    "name": "Lovley Cheese Pizza",
    "description": "This is a lovely cheese pizza",
    "number_of_servings": 3,
    "cook_time": 30,
    "directions": "This is how you make it"
}
```
DELETE localhost:5000/recipes/3

RESPONSE
```json
{
  "message": "recipe succesfully deleted"
}
```
### Recipe Publish Endpoints
PUT localhost:5000/recipes/3/publish

RESPONSE
```json
{}
```
DELETE localhost:5000/recipes/3/publish

RESPONSE
```json
{}
```
