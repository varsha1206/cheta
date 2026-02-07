# Cheta
*A lightweight, background personal assistant for your PC*

Cheta is a modular, extensible personal assistant designed to run quietly in the background and surface **high-value information at the right moment**. It focuses on **local-first execution**, **LLM-assisted reasoning**, and **minimal UI interruptions**, making it ideal for power users who live on their computers.

Cheta is under active development, with multiple assistant modules planned.

---

## Table of Contents
[1. Overview](#1-overview)  
[2. Current Features](#2-current-features)  
[3. Cheta Reactions (YouTube Recommendation Assistant)](#3-cheta-reactions--how-it-works)
[4. Configuration](#6-configuration) 
[5. Installation & Development](#7-installation--development)  
[6. Usage](#8-usage)  
[7. Roadmap](#9-roadmap) 

---

## 1. Overview

Cheta runs as a **CLI-launched background assistant** with a minimal GUI layer.  
Rather than demanding attention, Cheta **observes, reasons, and surfaces only what matters**.

Design goals:
- Tiny UI footprint  
- Background execution  
- Modular / extensible architecture   

---

## 2. Current Features

### Cheta Reactions (Available Now)

A smart YouTube reaction video recommender that:
- Fetches the latest videos from selected reaction channels
- Understands personal preferences (language, genre, shows, movies)
- Uses Gemini LLM reasoning to select **one best-fit video**
- Opens the selected video directly in the browser

More Cheta modules are currently in development.

---

## 3. Cheta Reactions – How It Works

1. User runs:  
   ```bash
   cheta reactions
   ```

2. Cheta:
   - Loads user preferences from local config
   - Fetches latest videos via the YouTube Data API
   - Sends structured video metadata to Gemini
   - Receives a structured output recommended by Gemini
   - Opens the video url automatically in Chrome

No scraping is used. Everything is API-driven and compliant.

---

## 4. Configuration

Cheta stores configuration locally, including:
- Preferred languages
- Favorite genres
- Liked movies and shows
- Selected YouTube channels

This data is used strictly as **runtime context** and is never used for training.

---

## 5. Installation & Development

> [!TIP]
> Make sure you have `uv` installed. If not install `uv` using `pipx install uv`

Install in editable mode:
```bash
 uv install -e .
```

Uninstall:
```bash
uv uninstall cheta
```

---

## 8. Usage

Run Cheta from anywhere:

```bash
cheta reactions
```

Future modules will follow the same pattern:
```bash
cheta [module_name]
```

---

## 9. Roadmap

Planned Cheta modules include:
- Background knowledge drip (language learning, concepts)
- Smart low-interruption notifications
- File system awareness assistant

---

Cheta is being built as a **long-term personal assistant platform**, not a single-purpose tool.
This is a project born out of personal interest and need. 
More features are actively in progress.
