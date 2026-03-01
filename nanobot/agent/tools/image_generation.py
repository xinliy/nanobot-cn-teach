"""Image generation tool using Alibaba DashScope Qwen Image Plus."""

import json
import os
from pathlib import Path
from typing import Any

from nanobot.agent.tools.base import Tool


class ImageGenerationTool(Tool):
    """Tool to generate images using DashScope Qwen Image Plus API."""

    def __init__(self, api_key: str | None = None):
        """
        Initialize the image generation tool.

        Args:
            api_key: DashScope API key. Falls back to DASHSCOPE_API_KEY env var,
                     then providers.dashscope.apiKey in ~/.nanobot/config.json.
        """
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY") or self._read_config_key()

    @staticmethod
    def _read_config_key() -> str | None:
        """Read DashScope API key from config.json as last-resort fallback."""
        try:
            config_path = Path.home() / ".nanobot" / "config.json"
            if config_path.exists():
                data = json.loads(config_path.read_text(encoding="utf-8"))
                return data.get("providers", {}).get("dashscope", {}).get("apiKey") or None
        except Exception:
            pass
        return None

    @property
    def name(self) -> str:
        return "image_generation"

    @property
    def description(self) -> str:
        return "Generate images from text prompts using Alibaba DashScope Qwen Image Plus. Supports descriptions in Chinese and English."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Image description in natural language (Chinese or English)"
                },
                "size": {
                    "type": "string",
                    "description": "Image size. Options: 1328*1328 (default), 1024*1024, 720*720, 512*512",
                    "enum": ["1328*1328", "1024*1024", "720*720", "512*512"]
                }
            },
            "required": ["prompt"]
        }

    async def execute(self, prompt: str, size: str = "1328*1328", **kwargs: Any) -> str:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Image description
            size: Image size (default: 1328*1328)

        Returns:
            Image URL or error message
        """
        if not self.api_key:
            return "❌ Error: DashScope API key not found. Set DASHSCOPE_API_KEY env var or add providers.dashscope.apiKey in ~/.nanobot/config.json."

        try:
            from dashscope import MultiModalConversation
        except ImportError:
            return "❌ Error: dashscope package not installed. Please install it with: pip install dashscope"

        try:
            messages = [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]

            response = MultiModalConversation.call(
                api_key=self.api_key,
                model="qwen-image-plus-2026-01-09",
                messages=messages,
                result_format='message',
                stream=False,
                watermark=False,
                prompt_extend=True,
                negative_prompt='',
                size=size
            )

            # Check response status
            if response.status_code == 200:
                choices = response.output.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", [])
                    for item in content:
                        if "image" in item:
                            return item["image"]
                return "❌ Error: Failed to extract image URL from API response"
            else:
                error_msg = getattr(response, 'message', 'Unknown error')
                return f"❌ API Error ({response.code}): {error_msg}"

        except Exception as e:
            return f"❌ Error executing image generation: {str(e)}"
