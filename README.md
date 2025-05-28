sudo ufw allow 8080/tcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server_run.py
python client_run.py