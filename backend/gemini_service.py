import os
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from typing import Optional
import tempfile

# API Key Configuration - Read from environment variable
API_KEY = os.environ.get('GOOGLE_API_KEY', 'AIzaSyDoOcXuFOnynSSFmNVM1zGGGFLTllVw_R4')

genai.configure(api_key=API_KEY)

# Generation Configuration
generation_config = GenerationConfig(
    max_output_tokens=2048,
    temperature=0.1,
    top_p=0.9,
    top_k=30
)

def prep_image(image_path: str, max_width: int = 1600, max_height: int = 2300):
    """
    Prepare and upload image to Gemini API
    
    Args:
        image_path: Path to the image file
        max_width: Maximum width for resizing
        max_height: Maximum height for resizing
    
    Returns:
        Uploaded file object from Gemini API
    """
    try:
        with Image.open(image_path) as img:
            img.thumbnail((max_width, max_height))
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                temp_path = temp_file.name
                img.save(temp_path, format='PNG')
            
            # Upload to Gemini
            sample_file = genai.upload_file(path=temp_path, display_name="Vision")
            
            # Clean up temp file
            os.remove(temp_path)
            
            return sample_file
    except Exception as e:
        raise Exception(f"Image preparation error: {str(e)}")


def analyze_shelf(image_path: str) -> Optional[str]:
    """
    Analyze shelf image and extract product information
    
    Args:
        image_path: Path to the shelf image
    
    Returns:
        Extracted information about products, prices, and contents
    """
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    
    try:
        sample_file = prep_image(image_path)
        
        prompt = """
        Bu bir market rafı fotoğrafıdır. Görme engelli bir kullanıcı için detaylı analiz yap:
        
        1. ÜRÜNLER: Rafta gördüğün tüm ürünleri listele
        2. FİYATLAR: Her ürünün fiyatını belirt (eğer görünüyorsa)
        3. İÇERİK BİLGİSİ: Ürünlerin içeriği, gramaj, adet bilgisi
        4. KONUM: Ürünlerin rafta nerede olduğunu tarif et (üst raf, alt raf, sağ, sol)
        5. ÖZEL NOTLAR: İndirim, promosyon, son kullanma tarihi gibi önemli bilgiler
        
        Cevabını açık, net ve sesli okumaya uygun şekilde ver. Her bilgiyi ayrı satırlarda sun.
        """
        
        response = model.generate_content([sample_file, prompt], generation_config=generation_config)
        
        return ''.join([part.text for part in response.parts]) if response.parts else None
    
    except Exception as e:
        raise Exception(f"Shelf analysis error: {str(e)}")


def analyze_store_navigation(image_path: str) -> Optional[str]:
    """
    Analyze store environment and provide navigation instructions
    
    Args:
        image_path: Path to the store interior image
    
    Returns:
        Navigation instructions for the visually impaired user
    """
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    
    try:
        sample_file = prep_image(image_path)
        
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
        
        response = model.generate_content([sample_file, prompt], generation_config=generation_config)
        
        return ''.join([part.text for part in response.parts]) if response.parts else None
    
    except Exception as e:
        raise Exception(f"Navigation analysis error: {str(e)}")


def extract_text_ocr(image_path: str) -> Optional[str]:
    """
    Extract text from image using OCR
    
    Args:
        image_path: Path to the image
    
    Returns:
        Extracted text content
    """
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    
    try:
        sample_file = prep_image(image_path)
        
        prompt = "Bu görseldeki tüm metinleri oku ve çıkar. Metinleri olduğu gibi, düzenli şekilde sun."
        
        response = model.generate_content([sample_file, prompt], generation_config=generation_config)
        
        return ''.join([part.text for part in response.parts]) if response.parts else None
    
    except Exception as e:
        raise Exception(f"OCR error: {str(e)}")
