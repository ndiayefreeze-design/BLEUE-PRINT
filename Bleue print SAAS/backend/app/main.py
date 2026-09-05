try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, PlainTextResponse
except Exception:  # pragma: no cover - depends on local runtime compatibility
    FastAPI = None
    CORSMiddleware = None
    HTMLResponse = None
    PlainTextResponse = None

from backend.app.calculation import CalculationRequest, calculate_landed_cost, render_devis_html, render_devis_text
from backend.app.matching import LEGAL_NOTE, MatchRequest, match_product
from backend.app.tariffs import get_tariff_profile

if FastAPI is not None and CORSMiddleware is not None:
    app = FastAPI(title="BLEUE PRINT API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health_check():
        return {"status": "ok", "service": "bleue-print"}

    @app.get("/")
    def home():
        return {"message": "BLEUE PRINT API", "note": LEGAL_NOTE}

    @app.post("/match")
    def match_endpoint(payload: MatchRequest):
        return match_product(payload)

    @app.post("/calculate")
    def calculate_endpoint(payload: CalculationRequest):
        return calculate_landed_cost(payload)

    @app.post("/quote/export", response_class=HTMLResponse)
    def export_quote_endpoint(payload: CalculationRequest):
        result = calculate_landed_cost(payload)
        return HTMLResponse(
            render_devis_html(result),
            headers={"Content-Disposition": "attachment; filename=bleue-print-devis.html"},
        )

    @app.get("/tariff/{code_sh}")
    def tariff_endpoint(code_sh: str):
        return get_tariff_profile(code_sh)
else:
    app = None

    def health_check():
        return {"status": "ok", "service": "bleue-print"}

    def home():
        return {"message": "BLEUE PRINT API", "note": LEGAL_NOTE}

    def match_endpoint(payload: MatchRequest):
        return match_product(payload)

    def calculate_endpoint(payload: CalculationRequest):
        return calculate_landed_cost(payload)

    def export_quote_endpoint(payload: CalculationRequest):
        return render_devis_text(calculate_landed_cost(payload))

    def tariff_endpoint(code_sh: str):
        return get_tariff_profile(code_sh)
