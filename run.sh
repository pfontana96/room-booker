#!/bin/sh
FILE=data/db.sqlite
if ! ( test -f "$FILE"); then
    # Si la base sqlite no existe, la creamos
    .venv/bin/python create_db.py
fi

# lanzamos la aplicacion
export FLASK_APP=project

.venv/bin/python flask run

exec $@