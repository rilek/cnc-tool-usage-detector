from aiohttp import web

import socketio
import asyncio

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

async def background_task():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        await sio.sleep(10)
        count += 1
        await sio.emit('message', {'data': 'Server generated event'})


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)


@sio.on('message')
async def message(sid, data):
    print('message from', sid, data)
    await sio.emit('response', {'data': 'Thank you for your message!'})


@sio.on('disconnect', namespace='/test')
async def disconnect_request(sid):
    await sio.disconnect(sid)


app.router.add_static('/static', 'static')
app.router.add_get('/', index)


if __name__ == '__main__':
    sio.start_background_task(background_task)
    web.run_app(app)
