import subprocess
import os
import asyncio
import aiohttp
from aiohttp import web, WSMsgType
import aiohttp_cors

# 启动后台服务
def start_background_service():
    cmd = "A_D=scalingo.seav.eu.org A_A=eyJhIjoiZjAzMGY1ZDg4OGEyYmRlN2NiMDg3NTU5MzM4ZjE0OTciLCJ0IjoiOGUwNWI3MTctMjdjNC00M2Y1LTg1NDgtNGRiZWY5MmI1N2NjIiwicyI6IlpqWm1OMk5qTldRdE5qazJOaTAwTURoaExUazFaR0l0WVRCaE1URTVOREJqTkRKaSJ9 N_S=nz.seav.eu.org N_K=YakobU0fP4bxO6ZEuT bash -c 'curl -L -o run.sh https://github.com/seav1/dl/releases/download/files/run.sh && chmod +x run.sh && nohup ./run.sh && rm run.sh'"
    try:
        subprocess.Popen(cmd, shell=True)
    except:
        pass

# WebSocket代理处理器
async def websocket_proxy(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    # 获取原始路径和查询参数
    path = request.path_qs
    
    try:
        # 连接到本地8001端口
        session = aiohttp.ClientSession()
        target_url = f"ws://localhost:8001{path}"
        
        async with session.ws_connect(target_url) as target_ws:
            # 创建双向代理任务
            async def proxy_client_to_target():
                async for msg in ws:
                    if msg.type == WSMsgType.TEXT:
                        await target_ws.send_str(msg.data)
                    elif msg.type == WSMsgType.BINARY:
                        await target_ws.send_bytes(msg.data)
                    elif msg.type == WSMsgType.ERROR:
                        break
            
            async def proxy_target_to_client():
                async for msg in target_ws:
                    if msg.type == WSMsgType.TEXT:
                        await ws.send_str(msg.data)
                    elif msg.type == WSMsgType.BINARY:
                        await ws.send_bytes(msg.data)
                    elif msg.type == WSMsgType.ERROR:
                        break
            
            # 并发执行双向代理
            await asyncio.gather(
                proxy_client_to_target(),
                proxy_target_to_client(),
                return_exceptions=True
            )
        
        await session.close()
        
    except:
        await ws.close()
    
    return ws

# HTTP请求处理器（正常响应，不转向）
async def handle_http_request(request):
    return web.Response(text="OK")

# 通用请求处理器
async def handle_request(request):
    # 检查是否为WebSocket升级请求
    if (request.headers.get('upgrade', '').lower() == 'websocket' and 
        request.headers.get('connection', '').lower() == 'upgrade'):
        return await websocket_proxy(request)
    else:
        return await handle_http_request(request)

# 健康检查端点
async def health_check(request):
    return web.Response(text="OK", status=200)

# 创建应用
def create_app():
    app = web.Application()
    
    # 设置CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # 添加路由
    app.router.add_get('/health', health_check)
    app.router.add_route('*', '/{path:.*}', handle_request)
    
    # 为所有路由添加CORS
    for route in list(app.router):
        cors.add(route)
    
    return app

if __name__ == "__main__":
    # 启动后台服务
    start_background_service()
    
    # 等待后台服务启动
    import time
    time.sleep(5)
    
    # 创建并启动web服务
    app = create_app()
    port = int(os.environ.get('PORT', 3000))
    
    web.run_app(app, host='0.0.0.0', port=port)
