# 🚀 PIF RAG Chat - Complete Run Guide

## 📋 Table of Contents

1. [Pre-Flight Validation](#-pre-flight-validation)
2. [Service Setup](#-service-setup)
3. [Document Processing](#-document-processing)
4. [Running the Application](#-running-the-application)
5. [Service Management](#-service-management)
6. [Troubleshooting](#-troubleshooting)

---

## ✅ Pre-Flight Validation

**Before starting anything, run the validation script:**

```bash
python scripts/validate_setup.py
```

**Expected Output:**
```
🔍 PIF RAG CHAT - PRE-FLIGHT VALIDATION

📋 Checking: Python Version
----------------------------------------------------------------------
✅ Python 3.11.0

📋 Checking: Environment File
----------------------------------------------------------------------
✅ config/.env file exists

📋 Checking: API Keys
----------------------------------------------------------------------
✅ GROQ_API_KEY is configured (gsk_AxjMbAjDB...)

📋 Checking: Config Files
----------------------------------------------------------------------
✅ llm_proxy_config.yaml exists

📋 Checking: Data Directories
----------------------------------------------------------------------
✅ PDFs directory exists
✅ Outputs directory exists
✅ Qdrant directory exists

📋 Checking: PDF Files
----------------------------------------------------------------------
✅ Found 6 PDF file(s)
   • PIF Annual Report 2021-ar.pdf
   • PIF Annual Report 2021.pdf
   • PIF Annual Report 2022-ar.pdf

======================================================================
📊 VALIDATION SUMMARY
======================================================================
✅ Python Version
✅ Environment File
✅ API Keys
✅ Config Files
✅ Data Directories
✅ PDF Files

6/6 checks passed

🎉 ALL CHECKS PASSED!

🚀 Next steps:
   1. Check services: python scripts/check_services.py
   2. Process documents: python scripts/process_documents.py
   3. Start app: streamlit run app.py
```

**If validation fails:**
- Missing API key → See [Troubleshooting](#-troubleshooting)
- Missing PDFs → Place files in `data/pdfs/`
- Python version → Upgrade to Python 3.8+

---

## 🔧 Service Setup

### Step 1: Check Service Status

```bash
python scripts/check_services.py
```

**Expected Output:**
```
🔍 Checking PIF RAG Chat Services...

4️⃣ Checking Environment Variables...
✅ GROQ_API_KEY is set (gsk_AxjMbA...)

✅ Ollama (Embeddings)    → Running at http://localhost:11434/api/version
✅ Qdrant (Vector DB)     → Running at http://localhost:6333/collections
✅ LLM Proxy (Answers)    → Running at http://localhost:4000/health

======================================================================
✅ ALL SERVICES RUNNING
======================================================================

🚀 You can now:
   1. Process documents: python scripts/process_documents.py
   2. Start app: streamlit run app.py
```

---

### Step 2: Start Missing Services

#### 2.1 Ollama (Embeddings) - Local

**Windows:**
```bash
# Ollama auto-starts after installation
# Verify it's running:
curl http://localhost:11434/api/version

# If not running, reinstall from:
# https://ollama.com/download

# Pull the embedding model:
ollama pull qwen3-embedding
```

**Mac/Linux:**
```bash
# Start Ollama service (separate terminal)
ollama serve

# Pull model
ollama pull qwen3-embedding

# Verify
curl http://localhost:11434/api/version
```

**Expected Response:**
```json
{"version":"0.1.x"}
```

---

#### 2.2 Qdrant (Vector Database) - Docker

**Windows:**
```bash
python scripts/start_qdrant.py
```

**Mac/Linux:**
```bash
python scripts/start_qdrant.py
```

**Expected Output:**
```
======================================================================
🗄️  QDRANT VECTOR DATABASE - STARTUP SCRIPT
======================================================================
✅ Docker installed: Docker version 24.0.x

🚀 Starting Qdrant container...
✅ Container started: abc123def456

⏳ Waiting for Qdrant to be ready...
✅ Qdrant is ready! (took 3s)

======================================================================
✅ QDRANT STARTED SUCCESSFULLY
======================================================================

📍 REST API: http://localhost:6333
📍 gRPC: http://localhost:6334
📊 Dashboard: http://localhost:6333/dashboard
```

**Verify:**
```bash
curl http://localhost:6333/collections
# Should return: {"result":{"collections":[]}} 
```

---

#### 2.3 LLM Proxy (Answer Generation) - CRITICAL!

**Terminal 2 (KEEP THIS RUNNING!):**
```bash
python scripts/start_llm_proxy.py
```

**Expected Output (in ~10 seconds):**
```
✅ Loaded environment from .env
🚀 Starting LLM Proxy Server...
📋 Config: llm_proxy_config.yaml
🌐 Groq (Primary) + Ollama Cloud (Fallback)

Starting LLM proxy on http://localhost:4000
======================================================================
Press Ctrl+C to stop
======================================================================

⏳ Waiting for proxy to start (max 10 seconds)...
✅ LLM proxy started successfully in 6s!
   📍 Base URL: http://localhost:4000
   🤖 Primary: Groq (llama3-8b)
   🔄 Fallbacks: Ollama Cloud models

INFO:     Started server process [12345]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000
```

**⚠️ CRITICAL:** Keep this terminal open! The LLM proxy must run continuously.

**Verify (in another terminal):**
```bash
curl http://localhost:4000/health
# Should return: 200 OK
```

**If startup fails:**
```bash
# Check litellm is installed:
pip install --upgrade "litellm[proxy]" uvicorn pyyaml

# Verify environment variables:
python -c "import os; from dotenv import load_dotenv; load_dotenv('config/.env'); print(os.getenv('GROQ_API_KEY')[:20])"
```

---

## 📚 Document Processing

**First time only - Process PDFs and create vector database:**

```bash
python scripts/process_documents.py
```

**Expected Output:**
```
🔍 Checking required services...

✅ Qdrant: Running
✅ Ollama: Running

======================================================================
📚 PIF Annual Reports - Document Processing Pipeline
======================================================================

📂 Project directory: C:\Users\...\project-v2\API
🔍 Searching for PDF files...

======================================================================
🌐 Processing Arabic Reports
======================================================================

✅ [2021] Found: PIF Annual Report 2021-ar.pdf
   📍 Location: data\pdfs
   🔄 Processing...
INFO: Extraction completed in 45.23 seconds
INFO: ✅ Successfully created collection 'PIF Annual Report 2021-ar_collection'
INFO: Uploaded batch 1: points 1-100/256
INFO: Uploaded batch 2: points 101-200/256
INFO: Uploaded batch 3: points 201-256/256
INFO: ✅ Successfully uploaded all 256 points
   ✅ Successfully processed!

... (repeats for each file)

======================================================================
📊 PROCESSING SUMMARY
======================================================================
✅ Successfully processed: 6/6 files
❌ Failed/Missing: 0/6 files
```

**This process:**
1. Extracts text from PDFs (using Docling + OCR)
2. Creates semantic chunks (using HybridChunker)
3. Generates embeddings (using Ollama qwen3-embedding)
4. Uploads to Qdrant (6 collections total)

**Time estimate:** 5-10 minutes per document

**You only need to run this:**
- First time setup
- When adding new PDF files
- After deleting Qdrant storage

---

## 🎯 Running the Application

**Terminal 3 (after LLM proxy is running):**

```bash
streamlit run app.py --server.port=8080
```

**Or use the launcher:**
```bash
python scripts/run_streamlit.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8080
  Network URL: http://192.168.x.x:8080
```

**Open browser:** http://localhost:8080

**First interaction:**
1. App shows landing page
2. Click "💬 Start Chatting"
3. Enter your name
4. Start asking questions!

---

## 🔧 Service Management

### Service Startup Order

```
1️⃣ Qdrant (Vector Database)    → python scripts/start_qdrant.py
2️⃣ Ollama (Embeddings)         → ollama serve (or auto-starts)
3️⃣ LLM Proxy (Answers)         → python scripts/start_llm_proxy.py ⚠️ KEEP RUNNING
4️⃣ Streamlit App               → streamlit run app.py
```

### Quick Start Script (Windows)

**Create `START_ALL.bat`:**
```batch
@echo off
echo Starting PIF RAG Chat Services...

REM Start Qdrant
echo.
echo 1. Starting Qdrant...
python scripts\start_qdrant.py

REM Start LLM Proxy (in new window)
echo.
echo 2. Starting LLM Proxy (new window)...
start cmd /k python scripts\start_llm_proxy.py

REM Wait for proxy to be ready
echo.
echo Waiting for LLM Proxy to initialize (15 seconds)...
timeout /t 15 /nobreak

REM Start Streamlit
echo.
echo 3. Starting Streamlit App...
streamlit run app.py --server.port=8080

pause
```

**Run:**
```bash
START_ALL.bat
```

### Stopping Services

**Proper shutdown order:**

1. **Stop Streamlit (Terminal 3):**
   ```
   Press Ctrl+C
   ```

2. **Stop LLM Proxy (Terminal 2):**
   ```
   Press Ctrl+C
   ```

3. **Stop Qdrant:**
   ```bash
   docker stop pif-qdrant
   ```

4. **Stop Ollama (optional - Mac/Linux only):**
   ```bash
   pkill ollama
   ```

**Windows:** Ollama service continues running (this is fine)

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Issue 1: "GROQ_API_KEY not configured"

**Error:**
```
❌ GROQ_API_KEY not configured
   💡 Get free key: https://console.groq.com/keys
```

**Solution:**
1. Get free API key from https://console.groq.com/keys
2. Edit `config/.env`:
   ```env
   GROQ_API_KEY=gsk_your_actual_groq_key_here
   ```
3. Re-run validation:
   ```bash
   python scripts/validate_setup.py
   ```

---

#### Issue 2: LLM Proxy Not Starting

**Error:**
```
❌ Startup timeout (10s)
```

**Solution 1 - Check litellm installation:**
```bash
pip install --upgrade "litellm[proxy]" uvicorn pyyaml
```

**Solution 2 - Verify config file:**
```bash
# Check if file exists
ls config/llm_proxy_config.yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config/llm_proxy_config.yaml'))"
```

**Solution 3 - Check environment:**
```bash
# Load .env and check API key
python -c "from dotenv import load_dotenv; import os; load_dotenv('config/.env'); print('Key:', os.getenv('GROQ_API_KEY')[:20] if os.getenv('GROQ_API_KEY') else 'NOT SET')"
```

**Solution 4 - Manual start:**
```bash
litellm --config config/llm_proxy_config.yaml --port 4000
```

---

#### Issue 3: Ollama Connection Failed

**Error:**
```
❌ Ollama (Embeddings) → Not running
```

**Solution (Windows):**
```bash
# Reinstall Ollama from https://ollama.com/download
# Service should auto-start

# Pull model
ollama pull qwen3-embedding

# Verify
curl http://localhost:11434/api/version
```

**Solution (Mac/Linux):**
```bash
# Start service
ollama serve

# In another terminal, pull model
ollama pull qwen3-embedding
```

---

#### Issue 4: Qdrant Not Responding

**Error:**
```
❌ Qdrant (Vector DB) → Not running
```

**Solution:**
```bash
# Check if container exists
docker ps -a | grep qdrant

# Remove old container
docker rm -f pif-qdrant

# Start fresh
python scripts/start_qdrant.py
```

**If Docker is not installed:**
- Windows/Mac: https://www.docker.com/products/docker-desktop
- Linux: https://docs.docker.com/engine/install/

---

#### Issue 5: Port Already in Use

**Error:**
```
Port 4000 already in use
```

**Solution (Windows):**
```bash
# Find process using port
netstat -ano | findstr :4000

# Kill process (replace PID)
taskkill /F /PID <PID>
```

**Solution (Mac/Linux):**
```bash
# Find process
lsof -i :4000

# Kill process
kill -9 <PID>
```

---

#### Issue 6: Slow Answer Generation

**Symptoms:**
- Answers take >10 seconds
- Timeout errors

**Solution 1 - Check LLM proxy is running:**
```bash
curl http://localhost:4000/health
```

**Solution 2 - Check Groq API status:**
- Visit https://status.groq.com
- Verify your API key at https://console.groq.com/keys

**Solution 3 - Restart LLM proxy:**
```bash
# Stop (Ctrl+C in Terminal 2)
# Start again
python scripts/start_llm_proxy.py
```

---

#### Issue 7: No Embeddings Generated

**Error during document processing:**
```
Failed to embed query after 3 attempts
```

**Solution:**
```bash
# Verify Ollama is running
curl http://localhost:11434/api/version

# Check if model is available
ollama list | grep qwen3-embedding

# If not found, pull it
ollama pull qwen3-embedding

# Restart processing
python scripts/process_documents.py
```

---

### Debug Mode

**Enable debug output in chat:**
1. Click **◉** button in control panel
2. OR check "🐛 Debug Mode" in sidebar
3. View source information and confidence scores

**Example debug output:**
```
**🔍 Debug Info:**
• Sources: 3
• Confidence: 0.87
• Years: 2023 (0.87), 2022 (0.76), 2021 (0.65)
• History: 4 messages
```

---

## 📊 Performance Tips

### For Faster Document Processing:

1. **Use SSD storage** for `data/` folder
2. **Increase batch size** in `src/core/config.py`:
   ```python
   EMBED_BATCH_SIZE = 16  # Default: 8
   ```
3. **Allocate more RAM** to Docker (Qdrant)

### For Faster Query Response:

1. **Keep LLM proxy running** (don't restart frequently)
2. **Use wired internet** (not WiFi) for Groq API
3. **Enable debug mode** only when needed (adds overhead)

---

## 🎉 Success Checklist

**You're ready when you see:**

✅ **Validation passes** (6/6 checks)
```bash
python scripts/validate_setup.py
# 🎉 ALL CHECKS PASSED!
```

✅ **All services running**
```bash
python scripts/check_services.py
# ✅ ALL SERVICES RUNNING
```

✅ **Documents processed**
```bash
ls data/qdrant_storage/
# Should contain collection data
```

✅ **LLM proxy responding**
```bash
curl http://localhost:4000/health
# 200 OK
```

✅ **App accessible**
```
Open http://localhost:8080
Landing page loads with PIF logo
```

✅ **Chat works**
- Enter your name
- Ask: "What are PIF's main investments?"
- Get well-formatted LLM answer (not raw context)

---

## 📞 Getting Help

**If you're still stuck:**

1. **Check logs:**
   ```bash
   # LLM Proxy logs (Terminal 2)
   # Streamlit logs (Terminal 3)
   ```

2. **Run full diagnostic:**
   ```bash
   python scripts/validate_setup.py
   python scripts/check_services.py
   ```

3. **Report issue with:**
   - Python version: `python --version`
   - OS: Windows/Mac/Linux
   - Error messages from logs
   - Screenshot if UI-related

4. **GitHub Issues:**
   https://github.com/m-monirr/PIF-Annual-Report_RagProject/issues

---

**🚀 Happy chatting with PIF RAG Assistant!** 🇸🇦