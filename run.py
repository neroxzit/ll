import threading
import os

def run_script(script_name):
    os.system(f'python3 {script_name}')

scripts = []

scripts.append('a_5365669433.py')#2024-03-10 05:26:52.182033

threads = []
for script in scripts:
    thread = threading.Thread(target=run_script, args=(script,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

