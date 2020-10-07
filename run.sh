#!/bin/sh
FILE=data/db.sqlite
if ! ( test -f "$FILE"); then
    # Si la base sqlite no existe, la creamos
    python create_db.py
fi

# lanzamos la aplicacion
export FLASK_APP=project

python -m flask run --host=0.0.0.0

exec $@