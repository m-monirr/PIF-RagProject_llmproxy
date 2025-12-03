# 🚀 Running PIF RAG Chat - QUICK START

## ⚡ Quick Start (Step-by-Step)

### Step 1: Check All Services

```bash
python scripts/check_services.py
```

This will tell you what's running and what needs to be started.

### Step 2: Start Qdrant (if not running)

```bash
python scripts/start_qdrant.py
```

Expected output:
```
Qdrant is already running.
```

If not running, it will start Qdrant and show:
```
Starting Qdrant...
Qdrant started successfully.
```

### Step 3: Start Ollama (if not running)

```bash
python scripts/start_ollama.py
```

Expected output:
```
Ollama is already running.
```

If not running, it will start Ollama and show:
```
Starting Ollama...
Ollama started successfully.
```

### Step 4: Start LLM Proxy (CRITICAL - Keep Running!)

**Terminal 2 (KEEP THIS OPEN!):**
```bash
cd "c:\Users\Mohamed\Desktop\ai career\pif-rag\project-v2\API"

python scripts/start_llm_proxy.py
```

**Expected Output:**
```
🚀 Starting LLM Proxy Server (Direct Import Method)...
This bypasses CLI issues and works with Python 3.13
Press Ctrl+C to stop

✅ LLM Proxy initialized successfully!
   📍 Base URL: http://0.0.0.0:4000
   🤖 Model: Ollama Cloud (qwen2.5:3b)
   🔄 Fallback: llama3.2:3b

Now you can start the main application with: python rag_chat_ui.py

INFO:     Started server process [12040]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
```

**⚠️ Keep Terminal 2 open! The LLM proxy must be running!**

**💡 No need to pull qwen2.5:3b or llama3.2:3b locally - they run on Ollama Cloud!**

## 📊 Step 2: Process Documents (First Time Only)

**Terminal 3:**

```bash
# Navigate to project directory
cd "c:\Users\Mohamed\Desktop\ai career\pif-rag\project-v2\API"

# Process PDFs and create embeddings (updated path)
python scripts/process_documents.py
```

**This will:**
- Extract text from PDFs
- Create chunks
- Generate embeddings using Ollama (local)
- Upload to Qdrant

**Expected output:**
```
INFO:__main__:Extraction completed in X.XX seconds
INFO:api_code.qdrant_utils:✅ Successfully created collection 'PIF_Annual_Report_2023_collection'
INFO:api_code.qdrant_utils:Uploaded batch 1: points 1-100/XXX
...
INFO:api_code.qdrant_utils:✅ Successfully processed and verified XXX chunks
```

## 🎯 Step 3: Start the Application

**⚠️ CRITICAL: Ensure LLM Proxy (Terminal 2) is still running!**

**In Terminal 3 (after processing is complete) or Terminal 4:**

```bash
# New Streamlit-based UI
streamlit run app.py --server.port=8080

# Or use the launcher script
python run_streamlit.py
```

**Expected output:**
```
NiceGUI ready to go on http://localhost:8080
```

## 🌐 Step 4: Access the Application

Open your browser and navigate to:
```
http://localhost:8080
```

## 📋 Service Startup Order (IMPORTANT!)

```
1️⃣ Qdrant (Vector Database)    → Terminal 1 (background)
2️⃣ LLM Proxy (Ollama Cloud)    → Terminal 2 (MUST BE RUNNING!)
3️⃣ Process Documents           → Terminal 3 (one-time only)
4️⃣ Main Application            → Terminal 3 or 4
```

## 🧪 Testing the Setup

### Test 1: Basic Question (English)
```
What are PIF's main investment sectors in 2023?
```

### Test 2: Arabic Question
```
ما هي استراتيجية صندوق الاستثمارات العامة؟
```

### Test 3: Year-Specific Question
```
How many jobs did PIF create in 2022?
```

## 🐛 Troubleshooting

### Issue 1: "LLM proxy not running" Error

**Error:** Chat shows errors or fallback answers only

**Solution:**
```bash
# Check if LLM proxy is running
curl http://localhost:4000/health

# If not running, start it in Terminal 2:
python start_llm_proxy_alternative.py

# Then restart the main application
```

### Issue 2: Ollama Not Running

**Error:** `Failed to connect to Ollama`

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If not, start it:
ollama serve
```

### Issue 3: Qdrant Not Running

**Error:** `Could not connect to Qdrant`

**Solution:**
```bash
# Check if Docker container is running
docker ps

# If not running, start it:
docker run -d -p 6333:6333 -p 6334:6334 -v "%cd%\qdrant_storage":/qdrant/storage qdrant/qdrant
```

### Issue 4: LLM Proxy Won't Start

**Error:** Import errors or timeout

**Solution:**
```bash
# Update packages
pip install --upgrade "litellm[proxy]" uvicorn pyyaml

# Try alternative startup:
python start_llm_proxy_alternative.py
```

### Issue 5: Port Already in Use

**Error:** `Port 4000 already in use`

**Solution:**
```bash
# Find process using port 4000
netstat -ano | findstr :4000

# Kill the process (replace PID with actual process ID)
taskkill /F /PID <PID>
```

## 📝 Quick Start Summary

**Correct Terminal Sequence:**

**Terminal 1 - Qdrant (Background):**
```bash
docker run -d -p 6333:6333 -p 6334:6334 -v "%cd%\qdrant_storage":/qdrant/storage qdrant/qdrant
```

**Terminal 2 - LLM Proxy (KEEP RUNNING!):**
```bash
python start_llm_proxy_alternative.py
```

**Terminal 3 - Process Documents (First Time) + Application:**
```bash
# First time only:
python -m api_code.main

# Then start app:
python rag_chat_ui.py
```

## 🛑 Stopping Everything (Proper Shutdown)

**Shutdown Order:**

1. **Stop the application (Terminal 3/4):** Press `Ctrl+C`
2. **Stop LLM proxy (Terminal 2):** Press `Ctrl+C`
3. **Stop Qdrant:**
   ```bash
   docker ps  # Find container ID
   docker stop <container_id>
   ```
4. **Stop Ollama:** (Windows usually keeps it running, which is fine)
   ```bash
   # Mac/Linux only:
   pkill ollama
   ```

## 📊 Monitoring Services

### Check All Services Status
```bash
# Check Ollama (embeddings)
curl http://localhost:11434/api/version

# Check Qdrant (vector DB)
curl http://localhost:6333/collections

# Check LLM Proxy (answer generation) - CRITICAL!
curl http://localhost:4000/health
```

### Expected Responses
- Ollama: `{"version":"..."}`
- Qdrant: `{"collections":[...]}`
- LLM Proxy: `200 OK` status

## 💡 Pro Tips

1. **Always start LLM Proxy first**: Before running `rag_chat_ui.py`, ensure Terminal 2 shows LLM proxy running
2. **Keep services running**: Once started, Qdrant and LLM proxy can run in the background
3. **Process PDFs once**: You only need to run `python -m api_code.main` when you add new PDFs
4. **Internet required**: Ollama Cloud needs active connection
5. **Check health endpoints**: Use curl commands to verify all services before starting the app

## 🎉 Success Indicators

You'll know everything is working when:

✅ **Ollama (embeddings)**: `curl http://localhost:11434/api/version` returns version
✅ **Qdrant (vector DB)**: `curl http://localhost:6333/collections` returns collections
✅ **LLM Proxy (CRITICAL!)**: Terminal 2 shows `Uvicorn running on http://0.0.0.0:4000`
✅ **LLM Proxy health**: `curl http://localhost:4000/health` returns 200
✅ **Application**: `NiceGUI ready to go on http://localhost:8080`
✅ **Chat works**: Answers are well-formatted and use LLM (not just context dumps)

## 🔍 Verify LLM Integration

**To confirm LLM is being used (not just context fallback):**

1. Open chat at http://localhost:8080
2. Ask: "What are PIF's main investment sectors?"
3. **Expected**: Well-formatted, natural answer with bullet points
4. **If fallback**: You'll see raw context starting with "Based on the PIF annual reports:"

If you see fallback answers, check Terminal 2 - the LLM proxy must be running!