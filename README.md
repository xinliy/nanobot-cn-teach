<div align="center">
  <img src="nanobot_logo.png" alt="nanobot" width="500">
  <h1>nanobot-cn-teach</h1>
  <p><strong>China-network-friendly fork of <a href="https://github.com/HKUDS/nanobot">nanobot</a></strong></p>
  <p>
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
    <img src="https://img.shields.io/badge/LLM-DashScope%20(Qwen)-orange" alt="DashScope">
    <img src="https://img.shields.io/badge/Chat-Feishu-E9DBFC" alt="Feishu">
    <img src="https://img.shields.io/badge/Search-Bocha-blue" alt="Bocha">
    <img src="https://img.shields.io/badge/No%20VPN-Required-brightgreen" alt="No VPN">
  </p>
</div>

> **Forked from [HKUDS/nanobot](https://github.com/HKUDS/nanobot)** (MIT License)
>
> This fork adapts nanobot for **China mainland network**. All APIs (LLM, search, image generation, chat) work directly without VPN.

## What's Different from Upstream

| Area | Upstream (HKUDS/nanobot) | This Fork |
|------|--------------------------|-----------|
| **LLM Provider** | OpenRouter, Anthropic, OpenAI, etc. | DashScope (Qwen) via `providers.custom` |
| **Web Search** | Brave Search | Bocha CN Search |
| **Image Generation** | -- | DashScope Qwen Image Plus (auto-registered tool) |
| **Feishu Channel** | Basic support | External image auto-upload fix (image_key) |
| **Network** | Requires global access | All CN-accessible, no VPN needed |

## Quick Start

### 1. Install

```bash
git clone https://github.com/xinliy/nanobot-cn-teach.git
cd nanobot-cn-teach
pip install -e .
```

### 2. Initialize

```bash
nanobot onboard
```

### 3. Configure (`~/.nanobot/config.json`)

```json
{
  "providers": {
    "custom": {
      "apiKey": "sk-your-dashscope-key",
      "apiBase": "https://dashscope.aliyuncs.com/compatible-mode/v1"
    },
    "dashscope": {
      "apiKey": "sk-your-dashscope-key"
    }
  },
  "agents": {
    "defaults": {
      "model": "qwen-max"
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  },
  "tools": {
    "webSearch": {
      "provider": "bocha",
      "apiKey": "your-bocha-key"
    }
  }
}
```

- `providers.custom` — powers the LLM (Qwen via OpenAI-compatible endpoint)
- `providers.dashscope` — powers image generation (same key, different API)
- Get your DashScope API key at [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com)
- Get your Bocha API key at [bochaai.com](https://www.bochaai.com)

### 4. Run

```bash
# CLI chat
nanobot agent

# Feishu bot
nanobot gateway
```

## Features

### Image Generation

The LLM auto-discovers and calls the image generation tool when users ask for images:

```
User: 生成一张小红书风格的花店图片
Bot: [generates and sends image via Feishu]
```

Supports Chinese & English prompts, sizes: 1328×1328, 1024×1024, 720×720, 512×512.

### Feishu Setup

Uses **WebSocket** long connection — no public IP required.

1. Visit [Feishu Open Platform](https://open.feishu.cn/app) → Create a new app → Enable **Bot** capability
2. **Permissions**: Add `im:message`
3. **Events**: Add `im.message.receive_v1`, select **Long Connection** mode
4. Copy **App ID** and **App Secret** → add to config → publish the app
5. Run `nanobot gateway`

## CLI Reference

| Command | Description |
|---------|-------------|
| `nanobot onboard` | Initialize config & workspace |
| `nanobot agent` | Interactive CLI chat |
| `nanobot agent -m "..."` | Single-turn chat |
| `nanobot gateway` | Start Feishu (and other) channels |
| `nanobot status` | Show status |

## Acknowledgments

Forked from [HKUDS/nanobot](https://github.com/HKUDS/nanobot) — an ultra-lightweight personal AI assistant. All credit for the core agent architecture goes to the original authors.
