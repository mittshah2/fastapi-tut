FastAPI tutorial.

Alembic commands:
1. alembic init \<directory name\>
2. add db url to alembic.ini
3. changes in env.py
   1. remove if condition for logging (line 15)
   2. add target_metadata = models.Base.metadata on line 21
4. run alembic revision -m "<message>"
5. complete the upgrade and downgrade functions in the revision file
6. upgrade -> alembic upgrade <revision id>
7. downgrade -> alembic downgrade -1
