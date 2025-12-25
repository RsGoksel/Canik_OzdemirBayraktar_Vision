import os
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from typing import Optional
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key Configuration - Read from environment variable
API_KEY = os.environ.get('GOOGLE_API_KEY', 'AIzaSyDoOcXuFOn.. ..')

# Validate API Key
if not API_KEY:
    logger.error("CRITICAL: GOOGLE_API_KEY not found in environment variables!")
    raise ValueError("GOOGLE_API_KEY is required but not set")
else:
    # Log masked API key for debugging
    masked_key = API_KEY[:10] + "..." + API_KEY[-4:] if len(API_KEY) > 14 else "***"
    logger.info(f"Google API Key loaded: {masked_key}")

try:
    genai.configure(api_key=API_KEY)
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    raise

# Generation Configuration
generation_config = GenerationConfig(
    max_output_tokens=2048,
    temperature=0.1,
    top_p=0.9,
    top_k=30
)

def prep_image(image_path: str, max_width: int = 1600, max_height: int = 2300):
    """
    Prepare image for Gemini API (returns PIL Image object)
    
    Args:
        image_path: Path to the image file
        max_width: Maximum width for resizing
        max_height: Maximum height for resizing
    
    Returns:
        PIL Image object ready for Gemini API
    """
    logger.info(f"Starting image preparation: {image_path}")
    try:
        # Open and validate image
        logger.debug(f"Opening image file: {image_path}")
        img = Image.open(image_path)
        original_size = img.size
        logger.info(f"Original image size: {original_size}")
        
        # Convert to RGB if needed (for compatibility)
        if img.mode != 'RGB':
            logger.info(f"Converting image from {img.mode} to RGB")
            img = img.convert('RGB')
        
        # Resize if necessary
        img.thumbnail((max_width, max_height))
        new_size = img.size
        logger.info(f"Resized image to: {new_size}")
        
        logger.info("Image prepared successfully (direct PIL Image)")
        return img
        
    except FileNotFoundError as e:
        logger.error(f"Image file not found: {image_path}")
        raise Exception(f"Görsel dosyası bulunamadı: {str(e)}")
    except Exception as e:
        logger.error(f"Image preparation failed: {str(e)}", exc_info=True)
        raise Exception(f"Görsel hazırlama hatası: {str(e)}")


def analyze_shelf(image_path: str) -> Optional[str]:
    """
    Analyze shelf image and extract product information
    
    Args:
        image_path: Path to the shelf image
    
    Returns:
        Extracted information about products, prices, and contents
    """
    logger.info("=" * 50)
    logger.info("STARTING SHELF ANALYSIS")
    logger.info("=" * 50)
    
    try:
        # Initialize model
        model_name = "gemini-2.5-flash"
        logger.info(f"Initializing Gemini model: {model_name}")
        model = genai.GenerativeModel(model_name=model_name)
        logger.info("Model initialized successfully")
        
        # Prepare image (returns PIL Image)
        img = prep_image(image_path)
        
        prompt = """
        Bu bir market rafı fotoğrafıdır. Görme engelli bir kullanıcı için detaylı analiz yap:
        
        1. ÜRÜNLER: Rafta gördüğün tüm ürünleri listele
        2. FİYATLAR: Her ürünün fiyatını belirt (eğer görünüyorsa)
        3. İÇERİK BİLGİSİ: Ürünlerin içeriği, gramaj, adet bilgisi
        4. KONUM: Ürünlerin rafta nerede olduğunu tarif et (üst raf, alt raf, sağ, sol)
        5. ÖZEL NOTLAR: İndirim, promosyon, son kullanma tarihi gibi önemli bilgiler
        
        Cevabını açık, net ve sesli okumaya uygun şekilde ver. Her bilgiyi ayrı satırlarda sun.
        """
        
        logger.info("Sending request to Gemini API with PIL Image...")
        response = model.generate_content([img, prompt], generation_config=generation_config)
        logger.info("Received response from Gemini API")
        
        if response.parts:
            result = ''.join([part.text for part in response.parts])
            logger.info(f"Analysis successful. Response length: {len(result)} characters")
            return result
        else:
            logger.warning("No response parts received from Gemini API")
            return None
    
    except Exception as e:
        logger.error(f"Shelf analysis failed: {str(e)}", exc_info=True)
        raise Exception(f"Raf analizi hatası: {str(e)}")


def analyze_store_navigation(image_path: str) -> Optional[str]:
    """
    Analyze store environment and provide navigation instructions
    
    Args:
        image_path: Path to the store interior image
    
    Returns:
        Navigation instructions for the visually impaired user
    """
    logger.info("Starting store navigation analysis")
    
    try:
        model_name = "gemini-2.5-flash"
        logger.info(f"Initializing model: {model_name}")
        model = genai.GenerativeModel(model_name=model_name)
        
        img = prep_image(image_path)
        
        prompt = """
        Bu bir market içi fotoğrafıdır. Görme engelli bir kullanıcıya navigasyon yardımı sağla:
        
        1. GENEL DÜZEN: Ortamı tarif et (koridor, kasa alanı, ürün reyonları vb.)
        2. YÖNLER: Kullanıcıya net yön talimatları ver:
           - İlerle / Dur / Geri dön
           - Sağa dön / Sola dön
           - Kaç adım ilerlemeli
        3. REYON BİLGİSİ: Hangi ürün gruplarının nerede olduğunu belirt
        4. ENGELLERİ FARK ET: Yolda engel, kalabalık, merdiven vb. varsa uyar
        5. HEDEF KONUMA ULAŞIM: "X ürünü için sola dön ve 5 adım ilerle" gibi spesifik talimatlar ver
        
        Talimatları basit, kısa cümlelerle ve sesli okumaya uygun şekilde ver.
        Her talimatı ayrı satırda sun.
        """
        
        logger.info("Sending navigation analysis request...")
        response = model.generate_content([img, prompt], generation_config=generation_config)
        
        if response.parts:
            logger.info("Navigation analysis successful")
            return ''.join([part.text for part in response.parts])
        else:
            logger.warning("No response parts for navigation")
            return None
    
    except Exception as e:
        logger.error(f"Navigation analysis failed: {str(e)}", exc_info=True)
        raise Exception(f"Navigasyon analizi hatası: {str(e)}")


def extract_text_ocr(image_path: str) -> Optional[str]:
    """
    Extract text from image using OCR
    
    Args:
        image_path: Path to the image
    
    Returns:
        Extracted text content
    """
    logger.info("Starting OCR text extraction")
    
    try:
        model_name = "gemini-2.5-flash"
        logger.info(f"Initializing model: {model_name}")
        model = genai.GenerativeModel(model_name=model_name)
        
        img = prep_image(image_path)
        
        prompt = "Bu görseldeki tüm metinleri oku ve çıkar. Metinleri olduğu gibi, düzenli şekilde sun."
        
        logger.info("Sending OCR request...")
        response = model.generate_content([img, prompt], generation_config=generation_config)
        
        if response.parts:
            logger.info("OCR extraction successful")
            return ''.join([part.text for part in response.parts])
        else:
            logger.warning("No text extracted")
            return None
    
    except Exception as e:
        logger.error(f"OCR extraction failed: {str(e)}", exc_info=True)
        raise Exception(f"Metin okuma hatası: {str(e)}")
