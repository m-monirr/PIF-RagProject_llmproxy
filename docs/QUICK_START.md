# 🚀 PIF RAG Chat - Quick Start Guide

## ✅ Current Status: All Services Running!

Great! Your environment is ready. Follow these steps:

---

## Step 1: Process Documents (First Time Only)

Place your PDF files in the project root or `data/pdfs/` folder, then run:

```bash
python -m scripts.process_documents
```

**Expected PDFs:**
- `PIF Annual Report 2021.pdf` (English)
- `PIF Annual Report 2022.pdf` (English)
- `PIF-2023-Annual-Report-EN.pdf` (English)
- `PIF Annual Report 2021-ar.pdf` (Arabic)
- `PIF Annual Report 2022-ar.pdf` (Arabic)
- `PIF-2023-Annual-Report-AR.pdf` (Arabic)

**This will:**
- ✅ Extract text from PDFs
- ✅ Create semantic chunks
- ✅ Generate embeddings using Ollama
- ✅ Upload to Qdrant vector database

**Time:** 5-15 minutes depending on PDF sizes

---

## Step 2: Start the Application

```bash
streamlit run app.py --server.port=8080
```

**Or use the launcher:**
```bash
python scripts/run_streamlit.py
```

**Access at:** http://localhost:8080

---

## 🎯 Daily Workflow (After Initial Setup)

### Quick Check

```bash
python scripts/check_services.py
```

### Start Missing Services

**If Qdrant is not running:**
```bash
python scripts/start_qdrant.py
```

**If LLM Proxy is not running:**
```bash
# Terminal 1
python scripts/start_llm_proxy.py
# Keep this running!
```

**If Ollama is not running (usually auto-starts):**
```bash
ollama serve
```

### Start the App

```bash
# Terminal 2 (or Terminal 1 if LLM proxy not needed yet)
streamlit run app.py
```

---

## 📋 Service Management Cheat Sheet

### Check All Services
```bash
python scripts/check_services.py
```

### Qdrant (Vector Database)
```bash
# Start
python scripts/start_qdrant.py

# Check
curl http://localhost:6333/collections

# View logs
docker logs -f pif-qdrant

# Stop
docker stop pif-qdrant

# Restart
docker restart pif-qdrant

# Remove and start fresh
docker rm -f pif-qdrant
python scripts/start_qdrant.py
```

### Ollama (Embeddings)
```bash
# Check status
ollama list

# Pull model (if not already done)
ollama pull qwen3-embedding

# Verify running
curl http://localhost:11434/api/version
```

### LLM Proxy (Answer Generation)
```bash
# Start (keep terminal open!)
python scripts/start_llm_proxy.py

# Check health
curl http://localhost:4000/health

# Stop
# Press Ctrl+C in the terminal running the proxy
```

---

## 🐛 Troubleshooting

### Service Not Running

**Problem:** Service check shows ❌

**Solution:**
1. Check the specific service section above
2. Start the service
3. Run `python scripts/check_services.py` again

### Port Already in Use

**Problem:** "Port 4000/6333/8080 already in use"

**Solution:**
```bash
# Windows - Find and kill process
netstat -ano | findstr :4000
taskkill /F /PID <PID>

# Or restart the service
docker restart pif-qdrant  # for Qdrant
```

### Documents Not Processing

**Problem:** "No valid chunks found"

**Solution:**
1. Check PDF files are in correct location
2. Verify Ollama is running: `ollama list`
3. Check Qdrant is accessible: `curl http://localhost:6333/collections`

### LLM Proxy Errors

**Problem:** "Model list not initialized" or connection errors

**Solution:**
1. Stop the proxy (Ctrl+C)
2. Check Groq API key in `config/.env`:
   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
3. Restart: `python scripts/start_llm_proxy.py`

### App Shows Fallback Answers

**Problem:** Answers start with "Based on the PIF annual reports:" without AI formatting

**Solution:**
- LLM proxy is not running
- Start it: `python scripts/start_llm_proxy.py` (in separate terminal)
- Keep it running while using the app

---

## 📁 File Locations

**Configuration:**
- `config/llm_proxy_config.yaml` - LLM routing
- `config/.env` - API keys and settings

**Data:**
- `data/pdfs/` - Source PDF files (recommended location)
- `data/outputs/` - Extraction results
- `data/qdrant_storage/` - Vector database persistence

**Scripts:**
- `scripts/check_services.py` - Check all services
- `scripts/start_qdrant.py` - Start Qdrant
- `scripts/start_llm_proxy.py` - Start LLM proxy
- `scripts/process_documents.py` - Process PDFs
- `scripts/cleanup_old_structure.py` - Remove old files

---

## 🎉 Success Indicators

You'll know everything is working when:

✅ `python scripts/check_services.py` shows all green
✅ Document processing completes without errors
✅ Streamlit app opens at http://localhost:8080
✅ Chat responses are well-formatted with AI-generated answers (not just raw context)
✅ Follow-up questions appear after each answer

---

## 💡 Pro Tips

1. **Keep LLM proxy running:** Once started, leave it in a dedicated terminal
2. **Use service check often:** Run before processing or starting app
3. **Docker persistence:** Qdrant data persists in `data/qdrant_storage/`
4. **Process once:** You only need to process PDFs once (or when adding new reports)
5. **Debug mode:** Enable in sidebar to see source information and confidence scores

---

## 🆘 Need Help?

1. Check `docs/RUN_GUIDE.md` for detailed troubleshooting
2. Run `python scripts/check_services.py` to diagnose issues
3. Check logs:
   - Qdrant: `docker logs pif-qdrant`
   - LLM Proxy: Terminal output
   - Streamlit: Terminal output

---

**Ready to start? Run:**

```bash
# If PDFs not processed yet:
python -m scripts.process_documents

# Start the app:
streamlit run app.py
```

🎊 **Enjoy exploring PIF's investment data!** 🇸🇦
