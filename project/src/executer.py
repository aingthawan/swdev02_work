import subprocess

p1 = subprocess.Popen(["python", "project\\src\\ELT_scrape.py"])
p2 = subprocess.Popen(["python", "project\\src\\basic_gui.py"])
# wait for both processes to finish
p1.wait()
p2.wait()