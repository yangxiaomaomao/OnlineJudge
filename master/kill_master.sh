sudo kill -9 $(ps aux | grep "[p]ython -B master.py" | awk '{print $2}')