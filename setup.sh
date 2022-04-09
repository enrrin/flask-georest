#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:"$(pwd)/src"
export FLASK_APP="$(pwd)/src/app.py"
export FLASK_ENV="development"