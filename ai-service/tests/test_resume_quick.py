#!/usr/bin/env python3
"""Quick test for resume generator"""

import asyncio
import httpx
import json

async def test_resume():
    print('[TEST] Resume Generator Test')
    print('='*60)
    
    payload = {
        'prompt': 'Create a resume for a Senior Software Engineer with 5 years experience in Python, React, and AWS',
        'content_type': 'resume',
        'tone': 'professional',
        'length': 'medium',
        'user_id': 'test-resume'
    }
    
    print('[INFO] Generating resume...')
    prompt_preview = payload['prompt'][:80]
    print(f'[INFO] Prompt: {prompt_preview}...')
    
    full_content = ''
    provider_info = None
    stats = None
    
    async with httpx.AsyncClient(timeout=90.0) as client:
        async with client.stream('POST', 'http://localhost:8000/chat/stream', json=payload) as response:
            if response.status_code != 200:
                print(f'[FAIL] HTTP {response.status_code}')
                return
            
            print('[INFO] Streaming response...')
            print('-'*60)
            
            async for line in response.aiter_lines():
                if not line.startswith('data: '):
                    continue
                
                try:
                    data = json.loads(line[6:])
                    
                    if 'provider' in data:
                        provider_info = data
                        print(f'[INFO] Provider: {data.get("provider")} | Model: {data.get("model")}')
                    
                    elif 'delta' in data:
                        delta = data.get('delta', '')
                        full_content += delta
                        print(delta, end='', flush=True)
                    
                    elif 'done' in data and data['done']:
                        stats = data
                        print()
                
                except json.JSONDecodeError:
                    continue
    
    print('-'*60)
    if stats:
        print(f'[PASS] Resume generated successfully!')
        print(f'[INFO] Provider: {provider_info.get("provider")}')
        print(f'[INFO] Model: {provider_info.get("model")}')
        print(f'[INFO] Words: {stats.get("word_count", 0)}')
        print(f'[INFO] Characters: {stats.get("char_count", 0)}')
        print(f'[INFO] Content length: {len(full_content)} chars')
        print()
        print('[PASS] Resume generator is WORKING!')
    else:
        print('[FAIL] Resume generation failed')

if __name__ == '__main__':
    asyncio.run(test_resume())
