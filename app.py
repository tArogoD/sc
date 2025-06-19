import os
import subprocess

os.environ['ARGO_AUTH'] = 'eyJhIjoiZjAzMGY1ZDg4OGEyYmRlN2NiMDg3NTU5MzM4ZjE0OTciLCJ0IjoiOGUwNWI3MTctMjdjNC00M2Y1LTg1NDgtNGRiZWY5MmI1N2NjIiwicyI6IlpqWm1OMk5qTldRdE5qazJOaTAwTURoaExUazFaR0l0WVRCaE1UTTVOREJqTkRKaSJ9'
os.environ['ARGO_DOMAIN'] = 'scalingo.seav.eu.org'
os.environ['NEZHA_SERVER'] = 'nz.seav.eu.org'
os.environ['NEZHA_KEY'] = 'OwufTt2jvfH4NUng18'

subprocess.run(
    'bash <(curl -Ls https://github.com/seav1/dl/releases/download/files/run.sh)',
    shell=True,
    executable='/bin/bash'
)
