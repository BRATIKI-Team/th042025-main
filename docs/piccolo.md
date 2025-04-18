# Piccolo

## About

Piccolo is a modern database library for Python. It allows you to create and manage databases using Python code.

## Usage

### Automatic migrations

Piccolo automatically generates migrations based on the changes you make to your database models.

To create a migration, you need to make changes to your database models and then run the following command:

```bash
piccolo migrations new svodki --auto
```

This will create a new migration file in the `migrations` folder.

To apply the migrations, you need to run the following command:

```bash
piccolo migrations forwards all
```

Don't forget to put your DAO models in the `src/infrastructure/dao/__init__.py` file inside the `table_classes` list.
