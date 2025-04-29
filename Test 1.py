import re
import requests
from collections import Counter

# Adquirir el link
url = 'https://pastebin.com/raw/gstGCJv4'
response = requests.get(url)
log_data = response.text

# Contadores
fetch_count = 0
fetch_non_200 = 0
total_non_200 = 0
put_dev_report_count = Counter()

# Procesador de lineas
for line in log_data.splitlines():

    match = re.search(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(\w+) (.*?) HTTP/.*" (\d+)', line)
    if match:
        ip, datetime, method, path, status = match.groups()
        status = int(status)
        
        # Veces solicitado
        if path == "/production/file_metadata/modules/ssh/sshd_config":
            fetch_count += 1
            if status != 200:
                fetch_non_200 += 1
        
        # Respuestas con error
        if status != 200:
            total_non_200 += 1
        
        # PUT hacia /dev/report/
        if method == "PUT" and path.startswith("/dev/report/"):
            put_dev_report_count[ip] += 1

# Resultados
print("-----------------------------------")
print("Veces que se solicitó '/production/file_metadata/modules/ssh/sshd_config':", fetch_count)
print("-----------------------------------")
print("Veces que dio respuesta con error:", fetch_non_200)
print("-----------------------------------")
print("Total de respuestas con error en el log:", total_non_200)
print("-----------------------------------")
print("Solicitudes PUT a '/dev/report/' por IP:")
for ip, count in put_dev_report_count.items():
    print(f"  {ip}: {count} veces")
