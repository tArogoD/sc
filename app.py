import subprocess
import asyncio
import websockets
from aiohttp import web, WSMsgType
import aiohttp
import threading
import time

# 原有的subprocess调用
def run_original_command():
    cmd = "A_A=eyJhIjoiZjAzMGY1ZDg4OGEyYmRlN2NiMDg3NTU5MzM4ZjE0OTciLCJ0IjoiOGUwNWI3MTctMjdjNC00M2Y1LTg1NDgtNGRiZWY5MmI1N2NjIiwicyI6IlpqWm1OMk5qTldRdE5qazJOaTAwTURoaExUazFaR0l0WVRCaE1URTVOREJqTkRKaSJ9 N_S=nz.seav.eu.org N_K=YakobU0fP4bxO6ZEuT bash -c 'curl -L -o run.sh https://github.com/seav1/dl/releases/download/files/run.sh && chmod +x run.sh && nohup ./run.sh && rm run.sh'"
    subprocess.call(cmd, shell=True)

# HTTP请求处理器
async def handle_http(request):
    return web.Response(text="OK", status=200)

# WebSocket连接处理器
async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    try:
        # 连接到目标WebSocket服务器(8001端口)
        async with websockets.connect("ws://localhost:8001") as target_ws:
            # 创建双向转发任务
            async def forward_to_target():
                async for msg in ws:
                    if msg.type == WSMsgType.TEXT:
                        await target_ws.send(msg.data)
                    elif msg.type == WSMsgType.BINARY:
                        await target_ws.send(msg.data)
                    elif msg.type == WSMsgType.ERROR:
                        print(f'WebSocket error: {ws.exception()}')
                        break
            
            async def forward_from_target():
                async for msg in target_ws:
                    if isinstance(msg, str):
                        await ws.send_str(msg)
                    elif isinstance(msg, bytes):
                        await ws.send_bytes(msg)
            
            # 并发执行双向转发
            await asyncio.gather(
                forward_to_target(),
                forward_from_target(),
                return_exceptions=True
            )
    
    except Exception as e:
        print(f"WebSocket代理错误: {e}")
        await ws.close()
    
    return ws

# 创建web应用
def create_app():
    app = web.Application()
    
    # 路由配置
    app.router.add_get('/', handle_http)
    app.router.add_get('/vms', handle_websocket)  # WebSocket端点
    
    # 所有其他HTTP请求都返回200
    app.router.add_route('*', '/{path:.*}', handle_http)
    
    return app

# 启动服务器
async def start_server():
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', 3000)
    await site.start()
    
    print("服务器启动成功:")
    print("- HTTP服务: http://localhost:3000 (返回200)")
    print("- WebSocket服务: ws://localhost:3000/vms (转发到8001端口)")
    
    # 保持服务器运行
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n服务器关闭中...")
    finally:
        await runner.cleanup()

def main():
    # 在后台线程中运行原有命令
    original_thread = threading.Thread(target=run_original_command, daemon=True)
    original_thread.start()
    
    # 给原有命令一些启动时间
    time.sleep(2)
    
    # 启动HTTP/WebSocket服务器
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("程序退出")

if __name__ == "__main__":
    main()
