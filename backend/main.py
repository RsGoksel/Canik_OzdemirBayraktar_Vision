from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import os
import tempfile
from gemini_service import analyze_shelf, analyze_store_navigation, extract_text_ocr

app = FastAPI(title="Vision Assistant API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
# Smart path detection that works in both local and Railway environments
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_frontend_directory():
    """Find frontend directory by checking multiple possible locations"""
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    
    logger.info(f"Current file: {current_file}")
    logger.info(f"Current directory: {current_dir}")
    logger.info(f"Working directory: {os.getcwd()}")
    
    # List all possible frontend locations to check
    possible_paths = [
        # Relative to current file's directory
        os.path.join(current_dir, "frontend"),
        os.path.join(current_dir, "..", "frontend"),
        os.path.join(current_dir, "..", "..", "frontend"),
        # From working directory
        os.path.join(os.getcwd(), "frontend"),
        # Absolute Railway paths
        "/app/frontend",
        "/app/backend/frontend",
    ]
    
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        exists = os.path.exists(abs_path)
        logger.info(f"Checking: {abs_path} - Exists: {exists}")
        if exists:
            # Verify it actually contains index.html
            index_path = os.path.join(abs_path, "index.html")
            if os.path.exists(index_path):
                logger.info(f"✓ Found frontend with index.html at: {abs_path}")
                return abs_path
            else:
                logger.warning(f"Found directory but missing index.html: {abs_path}")
    
    logger.error("Frontend directory not found in any expected location!")
    return None

frontend_path = find_frontend_directory()

if frontend_path:
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    logger.info(f"✓ Frontend static files mounted at /static from: {frontend_path}")
else:
    logger.error("✗ Frontend directory not found! Static files will not be served.")

@app.get("/")
async def root():
    """Serve the main frontend page"""
    if frontend_path and os.path.exists(frontend_path):
        frontend_index = os.path.join(frontend_path, "index.html")
        logger.info(f"Looking for index.html at: {frontend_index}")
        if os.path.exists(frontend_index):
            logger.info("Serving index.html")
            return FileResponse(frontend_index)
    logger.warning("Frontend not found, serving API status JSON")
    return {"message": "Vision Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Vision Assistant API"}

@app.post("/api/analyze-shelf")
async def analyze_shelf_endpoint(file: UploadFile = File(...)):
    """
    Analyze shelf image and extract product information
    
    Args:
        file: Uploaded image file
    
    Returns:
        JSON response with product information
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Analyze the shelf
        result = analyze_shelf(temp_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        if result:
            return JSONResponse(content={
                "success": True,
                "analysis": result,
                "type": "shelf"
            })
        else:
            raise HTTPException(status_code=500, detail="Analysis failed")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/api/analyze-navigation")
async def analyze_navigation_endpoint(file: UploadFile = File(...)):
    """
    Analyze store environment and provide navigation instructions
    
    Args:
        file: Uploaded image file
    
    Returns:
        JSON response with navigation instructions
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Analyze navigation
        result = analyze_store_navigation(temp_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        if result:
            return JSONResponse(content={
                "success": True,
                "analysis": result,
                "type": "navigation"
            })
        else:
            raise HTTPException(status_code=500, detail="Analysis failed")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/api/extract-text")
async def extract_text_endpoint(file: UploadFile = File(...)):
    """
    Extract text from image using OCR
    
    Args:
        file: Uploaded image file
    
    Returns:
        JSON response with extracted text
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Extract text
        result = extract_text_ocr(temp_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        if result:
            return JSONResponse(content={
                "success": True,
                "text": result,
                "type": "ocr"
            })
        else:
            raise HTTPException(status_code=500, detail="OCR failed")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
