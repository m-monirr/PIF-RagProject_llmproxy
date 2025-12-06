"""
LLM Proxy Manager for RAG Answer Generation
Handles Groq + Ollama Cloud integration with fallback mechanisms
"""

import logging
import openai
from typing import Optional, Dict, List
import subprocess
import time
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# CRITICAL: Load environment variables before starting proxy
env_path = Path(__file__).parent.parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

LLM_PROXY_BASE_URL = "http://localhost:4000"

class LLMProxyManager:
    """Manages LiteLLM proxy for answer generation with fallback support"""
    
    def __init__(self, config_path: str = "config/llm_proxy_config.yaml", port: int = 4000):
        self.config_path = Path(config_path)
        self.port = port
        self.base_url = f"http://localhost:{port}"
        self.client: Optional[openai.OpenAI] = None
        self.proxy_process = None
        self._proxy_pid = None  # Track our own process only
        
    def _kill_existing_processes(self):
        """Kill only OUR litellm process (safer approach)"""
        if self._proxy_pid:
            try:
                import psutil
                proc = psutil.Process(self._proxy_pid)
                logger.info(f"Killing our litellm process (PID: {self._proxy_pid})")
                proc.kill()
                proc.wait(timeout=3)
                self._proxy_pid = None
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            except Exception as e:
                logger.warning(f"Error killing process: {e}")
        
        time.sleep(1)  # Brief wait
    
    def start_proxy(self) -> bool:
        """Start LiteLLM proxy server with fast startup (max 10s)"""
        try:
            # Quick health check (1 retry, 2s timeout)
            if self._check_proxy_health(max_retries=1, timeout=2):
                logger.info(f"✅ LLM proxy already running on port {self.port}")
                self._initialize_client()
                return True
            
            if not self.config_path.exists():
                logger.error(f"Config file not found: {self.config_path}")
                return False
            
            # Kill our old process if exists
            self._kill_existing_processes()
            
            logger.info(f"🚀 Starting LLM proxy on port {self.port}...")
            logger.info(f"📋 Using config: {self.config_path.absolute()}")
            
            cmd = [
                "litellm",
                "--port", str(self.port),
                "--config", str(self.config_path.absolute())
            ]
            
            logger.info(f"Running command: {' '.join(cmd)}")
            
            # Start process and track PID
            self.proxy_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            self._proxy_pid = self.proxy_process.pid
            
            # FAST STARTUP: Max 10 seconds (5 retries × 2 seconds)
            logger.info("⏳ Waiting for proxy to start (max 10 seconds)...")
            max_retries = 5  # Reduced from 20
            for i in range(max_retries):
                # Check if process died
                if self.proxy_process.poll() is not None:
                    stdout, stderr = self.proxy_process.communicate()
                    logger.error(f"❌ Proxy process died")
                    logger.error(f"STDERR:\n{stderr[:500]}")
                    return False
                
                time.sleep(2)
                
                if self._check_proxy_health(max_retries=1, timeout=2):
                    logger.info(f"✅ LLM proxy started successfully in {(i+1)*2}s!")
                    logger.info(f"   📍 Base URL: {self.base_url}")
                    logger.info(f"   🤖 Primary: Groq (llama3-8b)")
                    logger.info(f"   🔄 Fallbacks: Ollama Cloud models")
                    self._initialize_client()
                    return True
                
                if i == max_retries - 1:
                    logger.error("❌ Startup timeout (10s)")
            
            # Get error output
            if self.proxy_process:
                try:
                    stdout, stderr = self.proxy_process.communicate(timeout=2)
                    if stderr:
                        logger.error(f"STDERR:\n{stderr[:500]}")
                except:
                    pass
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to start LLM proxy: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _check_proxy_health(self, max_retries=1, timeout=2) -> bool:
        """Quick health check with configurable retries"""
        for attempt in range(max_retries):
            try:
                endpoint = f"http://localhost:{self.port}/health"
                response = requests.get(endpoint, timeout=timeout)
                if response.status_code == 200:
                    return True
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                pass
            except Exception:
                pass
            
            if attempt < max_retries - 1:
                time.sleep(0.5)
        
        return False
    
    def _initialize_client(self):
        """Initialize OpenAI client with CORRECT timeout placement"""
        try:
            # CORRECT: timeout is a client parameter, NOT in create() call
            self.client = openai.OpenAI(
                api_key="dummy-key",
                base_url=self.base_url,
                timeout=20.0,  # This is correct - client-level timeout
                max_retries=1
            )
            logger.info("✅ OpenAI client initialized for LLM proxy")
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            self.client = None
    
    def _is_proxy_alive(self) -> bool:
        """Runtime check: Is proxy actually alive RIGHT NOW?"""
        # Check process is still running
        if self.proxy_process and self.proxy_process.poll() is not None:
            logger.warning("Proxy process died")
            return False
        
        # Quick health check
        return self._check_proxy_health(max_retries=1, timeout=2)
    
    def generate_answer(
        self,
        question: str,
        context: str,
        is_arabic: bool = False,
        chat_history: List[Dict] = None,
        max_tokens: int = 500,
        temperature: float = 0.3
    ) -> str:
        """Generate answer with RUNTIME health check"""
        # CRITICAL: Check if proxy is ACTUALLY alive before each call
        if not self.client or not self._is_proxy_alive():
            logger.warning("LLM proxy not available, using fallback")
            return self._fallback_answer(question, context, is_arabic)
        
        try:
            # Format chat history
            history_context = ""
            if chat_history and len(chat_history) > 0:
                recent_history = chat_history[-8:] if len(chat_history) > 8 else chat_history
                
                if is_arabic:
                    history_context = "\n\nالمحادثة السابقة:\n"
                    for msg in recent_history:
                        role = "المستخدم" if msg['role'] == 'user' else "المساعد"
                        history_context += f"{role}: {msg['content']}\n"
                else:
                    history_context = "\n\nPrevious conversation:\n"
                    for msg in recent_history:
                        role = "User" if msg['role'] == 'user' else "Assistant"
                        history_context += f"{role}: {msg['content']}\n"
            
            # Create prompt
            if is_arabic:
                system_prompt = """أنت مساعد ذكي متخصص في تحليل تقارير صندوق الاستثمارات العامة السعودي (PIF).
مهمتك هي تقديم إجابات دقيقة ومفصلة بناءً على السياق المقدم من التقارير السنوية.

قواعد الإجابة:
1. استخدم المعلومات من السياق المقدم فقط
2. راعِ المحادثة السابقة لفهم السياق الكامل
3. قدم إجابات واضحة ومنظمة
4. اذكر الأرقام والإحصائيات عند توفرها
5. إذا كانت المعلومات غير كافية، اذكر ذلك بوضوح
6. لا تختلق معلومات غير موجودة في السياق"""

                user_prompt = f"""السياق من تقارير صندوق الاستثمارات العامة:
{context}
{history_context}

السؤال الحالي: {question}

قدم إجابة شاملة ودقيقة بناءً على السياق والمحادثة السابقة. استخدم تنسيق واضح مع نقاط منظمة عند الضرورة."""

            else:
                system_prompt = """You are an intelligent assistant specialized in analyzing Saudi Arabia's Public Investment Fund (PIF) annual reports.
Your task is to provide accurate and detailed answers based on the provided context from annual reports.

Answer Guidelines:
1. Use only information from the provided context
2. Consider previous conversation for full context understanding
3. Provide clear and well-structured answers
4. Include numbers and statistics when available
5. If information is insufficient, state it clearly
6. Do not fabricate information not in the context"""

                user_prompt = f"""Context from PIF Annual Reports:
{context}
{history_context}

Current Question: {question}

Provide a comprehensive and accurate answer based on the context and previous conversation. Use clear formatting with organized bullet points when necessary."""

            # CORRECT: timeout is in client init, NOT here
            try:
                response = self.client.chat.completions.create(
                    model="rag-llm",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                    # REMOVED: timeout=20.0 (incorrect - not an OpenAI field)
                )
                
                answer = response.choices[0].message.content.strip()
                logger.info(f"✅ Generated answer using: {response.model}")
                return answer
                
            except openai.APITimeoutError:
                logger.error("API timeout")
                return self._fallback_answer(question, context, is_arabic)
            except openai.APIConnectionError as e:
                logger.error(f"Connection error: {e}")
                return self._fallback_answer(question, context, is_arabic)
            except openai.BadRequestError as e:
                logger.error(f"Bad request: {e}")
                return self._fallback_answer(question, context, is_arabic)
                
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return self._fallback_answer(question, context, is_arabic)
    
    def _fallback_answer(self, question: str, context: str, is_arabic: bool) -> str:
        """Fallback answer when LLM is unavailable"""
        if is_arabic:
            intro = "بناءً على المعلومات المتاحة في تقارير صندوق الاستثمارات العامة:\n\n"
        else:
            intro = "Based on the PIF annual reports:\n\n"
        
        return intro + context[:800] + "..."
    
    def stop_proxy(self):
        """Stop the LLM proxy server"""
        if self.proxy_process:
            try:
                self.proxy_process.terminate()
                self.proxy_process.wait(timeout=5)
                logger.info("✅ LLM proxy stopped")
            except:
                self.proxy_process.kill()
            finally:
                self.client = None
                self._proxy_pid = None
    
    def __enter__(self):
        """Context manager entry"""
        self.start_proxy()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_proxy()


# Global proxy instance (singleton pattern)
_proxy_instance: Optional[LLMProxyManager] = None

def get_llm_proxy() -> LLMProxyManager:
    """Get or create global LLM proxy instance with FAST health check"""
    global _proxy_instance
    if _proxy_instance is None:
        _proxy_instance = LLMProxyManager()
        
        # FAST check: 1 retry, 2 second timeout
        logger.info("🔍 Checking for LLM proxy...")
        
        if _proxy_instance._check_proxy_health(max_retries=1, timeout=2):
            _proxy_instance._initialize_client()
            logger.info("✅ Connected to LLM proxy")
        else:
            logger.warning("⚠️  LLM proxy not available - will use context fallback")
            logger.warning("   Start proxy: python scripts/start_llm_proxy.py")
            
    return _proxy_instance