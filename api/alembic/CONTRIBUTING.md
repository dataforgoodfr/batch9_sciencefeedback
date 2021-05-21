All alembic commands (see https://alembic.sqlalchemy.org/en/latest/api/commands.html) are available by doing:

```
./{COMMAND_NAME} alembic <command> <option1> <option2>...
```

Prefer to create a revision file this way:
```
./{COMMAND_NAME} alembic revision -m \"add foo id to bar\"
```

It will create an `add_foo_id_to_bar.py` revision file.

There is a little convention for writing the name of the revision file. First, when your migration is a granular operation, try to be closed to the name of the sql query behind:
  - `add_foo_id_to_bar` instead of `create_foo_id_in_bar`,
  - `alter_foo_to_nullable_in_bar` instead of `modify_foo_to_nullable_in_bar`
  - `drop_foo_from_bar` instead of `remove_foo_in_bar`,

Syntax of the file name is in underscore_case except for the camelCase variable name, like `25359c25c211_alter_myCamelCase_to_nullable_in_bar`.
