gunicorn -c server_config.py -w 4 -b 127.0.0.1:33201 server:start\(\)
