from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ocr_utils import ocr_local
import base64
import os
from openpyxl import Workbook

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

class OCRRequest(BaseModel):
    image: str  # Imagen en base64

class ExcelRequest(BaseModel):
    headers: list
    rows: list

app = FastAPI(title="API OCR Local Tesseract")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ocr")
async def ocr_image(request: OCRRequest):
    try:
        if not request.image or "," not in request.image:
            raise ValueError("Imagen base64 inválida o no enviada.")
        _, base64_data = request.image.split(",", 1)
        image_bytes = base64.b64decode(base64_data)

        text = ocr_local(image_bytes)
        return {"text": text, "campos": {}}
    except Exception as e:
        print("Error en /ocr:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/exportar_excel")
async def export_to_excel(data: ExcelRequest):
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Datos OCR"

        if data.headers:
            ws.append(data.headers)
        for row in data.rows:
            ws.append(row)

        output_file = os.path.join(EXPORT_DIR, "datos_extraidos.xlsx")
        wb.save(output_file)

        return {"message": "Archivo Excel generado correctamente.", "path": output_file}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def root():
    return {"message": "API OCR Local lista."}

# Para pruebas locales
if __name__ == "__main__":
    import uvicorn
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
