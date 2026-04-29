#!/usr/bin/env python3
"""
TMP Local Relay — forwards demo API requests to Anthropic.

Usage:
  pip install aiohttp
  python3 relay.py

Reads ANTHROPIC_API_KEY from environment. Demos call http://localhost:3001/v1/chat
instead of the Anthropic API directly — no key pasting in the browser required.

Test: curl http://localhost:3001/health
"""
import os
import asyncio
from aiohttp import web, ClientSession, ClientTimeout

PORT = 3001
ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages'

API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')


def cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


async def handle_options(request):
    return cors(web.Response(status=204))


async def handle_health(request):
    return cors(web.json_response({
        'status': 'ok',
        'key_loaded': bool(API_KEY),
        'key_prefix': API_KEY[:12] + '...' if API_KEY else None,
    }))


async def handle_chat(request):
    try:
        body = await request.json()
    except Exception:
        return cors(web.json_response({'error': 'Invalid JSON body'}, status=400))

    if not API_KEY:
        return cors(web.json_response(
            {'error': 'ANTHROPIC_API_KEY not set — restart relay.py after exporting the key'},
            status=500
        ))

    system = body.get('system', '')
    user = body.get('user', '')
    model = body.get('model', 'claude-sonnet-4-6')
    max_tokens = int(body.get('max_tokens', 1800))

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01',
    }
    payload = {
        'model': model,
        'max_tokens': max_tokens,
        'system': system,
        'messages': [{'role': 'user', 'content': user}],
    }

    try:
        async with ClientSession(timeout=ClientTimeout(total=120)) as session:
            async with session.post(ANTHROPIC_URL, headers=headers, json=payload) as r:
                data = await r.json()
                if r.status != 200:
                    msg = data.get('error', {}).get('message', f'Anthropic API HTTP {r.status}')
                    return cors(web.json_response({'error': msg}, status=502))
                content = data['content'][0]['text']
                return cors(web.json_response({'content': content}))
    except asyncio.TimeoutError:
        return cors(web.json_response({'error': 'Anthropic API timeout (120s)'}, status=504))
    except Exception as e:
        return cors(web.json_response({'error': str(e)}, status=502))


async def main():
    app = web.Application()
    app.router.add_route('OPTIONS', '/{path_info:.*}', handle_options)
    app.router.add_get('/health', handle_health)
    app.router.add_post('/v1/chat', handle_chat)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', PORT)
    await site.start()

    if not API_KEY:
        print(f'[RELAY] WARNING: ANTHROPIC_API_KEY not set — set it and restart before running demos.')
    else:
        print(f'[RELAY] Key loaded: {API_KEY[:12]}...')
    print(f'[RELAY] Listening on http://localhost:{PORT}')
    print(f'[RELAY] Test: curl http://localhost:{PORT}/health')
    print(f'[RELAY] Ctrl+C to stop')

    await asyncio.Event().wait()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n[RELAY] Stopped.')
