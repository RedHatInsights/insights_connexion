Insights Connexion
===========================================

This is a python package intended to be used as a base for an Insights Platform REST API application. It does all the boilerplate required to use a Postgres database with Connexion/Flask API. 

Installation
--------------------
```
pipenv install -e "git+git://github.com/RedHatInsights/insights_connexion.git#egg=insights_connexion" -d
```

Required Project Structure
--------------------
- api/
- app.py
- config.ini
- db/
  - models.py
- swagger/ 
  - api.spec.yaml
- test/
  - test.py
  - values.json

**app.py**
```
import insights_connexion.app as app

app.start()
```

**swagger/api.spec.yaml**

This is the Swagger spec for the REST API. It will be used by [Connexion](https://github.com/zalando/connexion/) to automatically serve and validate the routes.

**test/test.py**

This is where you will define your tests. The following is an example of how to use this package's OATTS test runner


**test/values.json**

This is passed to oatts --customValuesFile. See [oatts](https://github.com/google/oatts) for details.

**db/models.py**

This is where the SQLAlchemy models are defined. They can be defined anywhere, this location is just an example. Here's an example how to define them:

```
from insights_connexion.db.base import Base
from sqlalchemy import Column, String


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(String, primary_key=True)
```

**api/**

This is the directory Connexion will look in for the endpoint handling functions. Each endpoint needs a separate file. See the [Connexion routing docs](https://connexion.readthedocs.io/en/latest/routing.html) for details.

**config.ini**

This contains all the application's configuration parameters. Each environment gets a separate section, e.g. dev, qa, prod. It requires at least the following parameters in the [DEFAULT] section (substituting the values for your app):
```
[DEFAULT]
db_name = tagservice
db_user = tagservice
db_password = tagservice
db_host = localhost
db_port = 5746
log_level = INFO
debug = True
port = 8080
db_pool_size = 30
db_max_overflow = 100

```

Migrations
--------------------
Migrations should be managed by alembic. Follow the [alembic doc](https://alembic.zzzcomputing.com/en/latest/tutorial.html#the-migration-environment) to initialize the directory structure and create the database migration scripts.

Running The App
--------------------
`pipenv run python app.py`
