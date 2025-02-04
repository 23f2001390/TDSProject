import os
import json
from pathlib import Path
import aiohttp
import asyncio
from datetime import datetime
import sqlite3
from typing import List, Dict

class TaskHandler:
    def __init__(self):
        self.api_token = os.environ.get("AIPROXY_TOKEN")
        if not self.api_token:
            raise ValueError("AIPROXY_TOKEN environment variable not set")
        
    async def _call_llm(self, prompt: str) -> str:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            async with session.post(
                "https://api.aiproxy.puneeth.org/v1/chat/completions",
                json={"messages": [{"role": "user", "content": prompt}]},
                headers=headers
            ) as response:
                result = await response.json()
                return result['choices'][0]['message']['content']

    def _validate_path(self, path: str) -> bool:
        """Ensure path is within /data directory"""
        path = Path(path).resolve()
        data_dir = Path("/data").resolve()
        return data_dir in path.parents

    async def execute(self, task: str) -> Dict:
        # Parse task using LLM
        parse_prompt = f"""Parse this task and identify:
1. Type of operation
2. Input files/paths
3. Output files/paths
4. Additional parameters

Task: {task}"""
        
        parsed = await self._call_llm(parse_prompt)
        task_info = json.loads(parsed)
        
        # Validate all paths
        for path in task_info.get("input_files", []) + task_info.get("output_files", []):
            if not self._validate_path(path):
                raise ValueError(f"Access to {path} is not allowed")

        # Execute based on task type
        task_type = task_info["type"]
        # Implement task execution logic here
        
        return {"status": "success"}
