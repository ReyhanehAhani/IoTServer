python -m pip install -r requirements.txt
export FLASK_APP=iotserver
export FLASK_ENV=production
python -m flask run --host=0.0.0.0
