-> activate virtual environment
source .venv/bin/activate

-> start mongodb
sudo service mongod start

-> start the app
uvicorn app.main:app --reload
uvicorn app.main:app --reload --host 0.0.0.0

-> to update the requirements.txt
pip freeze > requirements.txt
