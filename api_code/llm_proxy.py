"""
LLM Proxy Manager for RAG Answer Generation
Handles Ollama Cloud integration with fallback mechanisms
"""

import logging
import openai
from typing import Optional, Dict, List
from pathlib import Path
import subprocess
import time
import requests

logger = logging.getLogger(__name__)

class LLMProxyManager:
    """Manages LiteLLM proxy for answer generation with fallback support"""
    
    def __init__(self, config_path: str = "llm_proxy_config.yaml", port: int = 4000):
        self.config_path = Path(config_path)
        self.port = port
        self.base_url = f"http://0.0.0.0:{port}"
        self.client: Optional[openai.OpenAI] = None
        self.proxy_process = None
        self._is_running = False
        
    def start_proxy(self) -> bool:
        """Start LiteLLM proxy server"""
        try:
            # Check if already running
            if self._check_proxy_health():
                logger.info(f"✅ LLM proxy already running on port {self.port}")
                self._initialize_client()
                return True
            
            # Check if config file exists
            if not self.config_path.exists():
                logger.error(f"Config file not found: {self.config_path}")
                return False
            
            # Start proxy in background
            logger.info(f"🚀 Starting LLM proxy on port {self.port}...")
            
            # Kill any existing litellm processes
            try:
                subprocess.run(["pkill", "-f", "litellm"], check=False, capture_output=True)
            except:
                pass
            
            time.sleep(2)
            
            # Start new proxy
            self.proxy_process = subprocess.Popen(
                ["litellm", "--port", str(self.port), "--config", str(self.config_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for proxy to be ready
            max_retries = 30
            for i in range(max_retries):
                time.sleep(1)
                if self._check_proxy_health():
                    logger.info(f"✅ LLM proxy started successfully on port {self.port}")
                    self._initialize_client()
                    return True
                
            logger.error("Failed to start LLM proxy - timeout")
            return False
            
        except Exception as e:
            logger.error(f"Failed to start LLM proxy: {e}")
            return False
    
    def _check_proxy_health(self) -> bool:
        """Check if proxy is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _initialize_client(self):
        """Initialize OpenAI client for proxy"""
        try:
            self.client = openai.OpenAI(
                api_key="dummy-key",  # LiteLLM doesn't need real key for Ollama
                base_url=self.base_url
            )
            self._is_running = True
            logger.info("✅ OpenAI client initialized for LLM proxy")
        except Exception as e:
            logger.error(f"Failed to initialize client: {e}")
            self._is_running = False
    
    def generate_answer(
        self,
        question: str,
        context: str,
        is_arabic: bool = False,
        max_tokens: int = 500,
        temperature: float = 0.3
    ) -> str:
        """
        Generate answer using LLM with context from RAG
        
        Args:
            question: User's question
            context: Retrieved context from vector DB
            is_arabic: Whether the question is in Arabic
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Generated answer string
        """
        if not self._is_running or not self.client:
            logger.error("LLM proxy not running")
            return self._fallback_answer(question, context, is_arabic)
        
        try:
            # Create prompt based on language
            if is_arabic:
                system_prompt = """أنت مساعد ذكي متخصص في تحليل تقارير صندوق الاستثمارات العامة السعودي (PIF).
مهمتك هي تقديم إجابات دقيقة ومفصلة بناءً على السياق المقدم من التقارير السنوية.

قواعد الإجابة:
1. استخدم المعلومات من السياق المقدم فقط
2. قدم إجابات واضحة ومنظمة
3. اذكر الأرقام والإحصائيات عند توفرها
4. إذا كانت المعلومات غير كافية، اذكر ذلك بوضوح
5. لا تختلق معلومات غير موجودة في السياق"""

                user_prompt = f"""السياق من تقارير صندوق الاستثمارات العامة:
{context}

السؤال: {question}

قدم إجابة شاملة ودقيقة بناءً على السياق أعلاه. استخدم تنسيق واضح مع نقاط منظمة عند الضرورة."""

            else:
                system_prompt = """You are an intelligent assistant specialized in analyzing Saudi Arabia's Public Investment Fund (PIF) annual reports.
Your task is to provide accurate and detailed answers based on the provided context from annual reports.

Answer Guidelines:
1. Use only information from the provided context
2. Provide clear and well-structured answers
3. Include numbers and statistics when available
4. If information is insufficient, state it clearly
5. Do not fabricate information not in the context"""

                user_prompt = f"""Context from PIF Annual Reports:
{context}

Question: {question}

Provide a comprehensive and accurate answer based on the context above. Use clear formatting with organized bullet points when necessary."""

            # Call LLM through proxy
            response = self.client.chat.completions.create(
                model="rag-llm",  # This will use primary + fallbacks
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            answer = response.choices[0].message.content.strip()
            logger.info(f"✅ Generated answer using model: {response.model}")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating answer with LLM: {e}")
            return self._fallback_answer(question, context, is_arabic)
    
    def _fallback_answer(self, question: str, context: str, is_arabic: bool) -> str:
        """Fallback answer when LLM is unavailable"""
        if is_arabic:
            intro = "بناءً على المعلومات المتاحة في تقارير صندوق الاستثمارات العامة:\n\n"
        else:
            intro = "Based on the PIF annual reports:\n\n"
        
        # Simple context-based answer (existing behavior)
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
                self._is_running = False
                self.client = None
    
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
    """Get or create global LLM proxy instance"""
    global _proxy_instance
    if _proxy_instance is None:
        _proxy_instance = LLMProxyManager()
        _proxy_instance.start_proxy()
    return _proxy_instance
