from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from html import escape
from pathlib import Path

LEGAL_NOTE = "Estimation à titre indicatif — la classification tarifaire officielle et la déclaration en douane relèvent exclusivement d'un commissionnaire en douane agréé via GAINDE."


@dataclass
class CalculationRequest:
    code_sh: str
    product_label: str
    cif_value: float
    customs_rate: float = 0.0
    rs_rate: float = 0.0
    pc_rate: float = 0.0
    vat_rate: float = 0.18
    specific_taxes: float = 0.0
    origin_country: str = ""
    freight_value: float = 0.0
    insurance_value: float = 0.0


@dataclass
class TaxBreakdown:
    customs: float = 0.0
    rs: float = 0.0
    pc: float = 0.0
    vat: float = 0.0
    specific_taxes: float = 0.0
    subtotal_before_vat: float = 0.0
    total: float = 0.0


@dataclass
class DocumentRequirement:
    name: str
    required: bool = False
    note: str = ""


@dataclass
class CalculationResult:
    legal_note: str
    code_sh: str
    product_label: str
    cif_value: float
    freight_value: float = 0.0
    insurance_value: float = 0.0
    breakdown: TaxBreakdown = field(default_factory=TaxBreakdown)
    total_cost: float = 0.0
    documents: list[DocumentRequirement] = field(default_factory=list[DocumentRequirement])
    currency: str = "CFA"


def calculate_landed_cost(request: CalculationRequest) -> CalculationResult:
    cif_value = request.cif_value + request.freight_value + request.insurance_value
    customs = cif_value * request.customs_rate
    rs = cif_value * request.rs_rate
    pc = cif_value * request.pc_rate
    specific_taxes = cif_value * request.specific_taxes
    subtotal_before_vat = cif_value + customs + rs + pc + specific_taxes
    vat = subtotal_before_vat * request.vat_rate
    total = subtotal_before_vat + vat

    breakdown = TaxBreakdown(
        customs=customs,
        rs=rs,
        pc=pc,
        vat=vat,
        specific_taxes=specific_taxes,
        subtotal_before_vat=subtotal_before_vat,
        total=total,
    )

    docs = [
        DocumentRequirement("Facture commerciale", True, "Facture du fournisseur obligatoire."),
        DocumentRequirement("BL / connaissement", True, "Document de transport et preuve de réception."),
        DocumentRequirement("Certificat d'origine", False, "Obligatoire selon l'origine et le type de produit."),
        DocumentRequirement("Certificat sanitaire", False, "À vérifier selon la catégorie."),
        DocumentRequirement("Certificat phytosanitaire", False, "À vérifier selon les produits agricoles."),
    ]

    return CalculationResult(
        legal_note=LEGAL_NOTE,
        code_sh=request.code_sh,
        product_label=request.product_label,
        cif_value=cif_value,
        freight_value=request.freight_value,
        insurance_value=request.insurance_value,
        breakdown=breakdown,
        total_cost=total,
        documents=docs,
        currency="CFA",
    )


def generate_pdf_devis(result: CalculationResult, output_path: str | Path) -> str:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "BLEUE PRINT - Devis estimatif",
        "===========================",
        f"Produit: {result.product_label}",
        f"Code SH: {result.code_sh}",
        f"CIF: {result.cif_value:,.2f} {result.currency}",
        "",
        "Détail des taxes:",
        f"Droit de douane: {result.breakdown.customs:,.2f} {result.currency}",
        f"Redevance statistique: {result.breakdown.rs:,.2f} {result.currency}",
        f"Prélèvement communautaire: {result.breakdown.pc:,.2f} {result.currency}",
        f"Taxe spécifique: {result.breakdown.specific_taxes:,.2f} {result.currency}",
        f"TVA: {result.breakdown.vat:,.2f} {result.currency}",
        f"Total estimé: {result.total_cost:,.2f} {result.currency}",
        "",
        "Documents généralement requis:",
    ]

    for document in result.documents:
        status = "Obligatoire" if document.required else "Selon cas"
        lines.append(f"- {document.name} ({status}) : {document.note}")

    lines.append("")
    lines.append(result.legal_note)

    content = "\n".join(lines)
    destination.write_text(content, encoding="utf-8")
    return str(destination)


def render_devis_text(result: CalculationResult) -> str:
    lines = [
        "BLEUE PRINT - Devis estimatif",
        "===========================",
        f"Produit: {result.product_label}",
        f"Code SH: {result.code_sh}",
        f"Valeur marchandise: {result.cif_value - result.freight_value - result.insurance_value:,.2f} {result.currency}",
        f"Fret: {result.freight_value:,.2f} {result.currency}",
        f"Assurance: {result.insurance_value:,.2f} {result.currency}",
        f"Valeur CIF: {result.cif_value:,.2f} {result.currency}",
        "",
        "Détail des taxes:",
        f"Droit de douane: {result.breakdown.customs:,.2f} {result.currency}",
        f"Redevance statistique: {result.breakdown.rs:,.2f} {result.currency}",
        f"Prélèvement communautaire: {result.breakdown.pc:,.2f} {result.currency}",
        f"Taxe spécifique: {result.breakdown.specific_taxes:,.2f} {result.currency}",
        f"TVA: {result.breakdown.vat:,.2f} {result.currency}",
        f"Total estimé: {result.total_cost:,.2f} {result.currency}",
        "",
        result.legal_note,
    ]
    return "\n".join(lines)


def render_devis_html(result: CalculationResult) -> str:
        documents = "".join(
                f'<li><strong>{escape(document.name)}</strong><span>{"Obligatoire" if document.required else "Selon cas"}</span></li>'
                for document in result.documents
        )
        merchandise_value = result.cif_value - result.freight_value - result.insurance_value
        rows = [
                ("Marchandise", merchandise_value),
                ("Fret", result.freight_value),
                ("Assurance", result.insurance_value),
                ("Droit de douane", result.breakdown.customs),
                ("Redevance statistique", result.breakdown.rs),
                ("Prélèvement communautaire", result.breakdown.pc),
                ("Taxe spécifique", result.breakdown.specific_taxes),
                ("TVA", result.breakdown.vat),
        ]
        cost_rows = "".join(
                f'<tr><td>{label}</td><td>{value:,.2f} {result.currency}</td></tr>'
                for label, value in rows
        )
        return f"""<!doctype html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>BLEUE PRINT - Devis estimatif</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Space+Mono:wght@400;700&display=swap');
        @import url('https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@400,500,600,700&display=swap');
        :root {{ --violet: #4A2B5C; --violet-deep: #20101E; --paper: #FCFBFD; --ink: #0D0B0F; --steel: #625D66; --line: #DCD7DF; }}
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; background: var(--paper); color: var(--ink); font-family: "Cabinet Grotesk", "Segoe UI", sans-serif; }}
        .sheet {{ max-width: 860px; margin: 32px auto; padding: 52px 58px; background: white; border-top: 6px solid var(--ink); box-shadow: 0 18px 45px rgba(32,16,30,.12); }}
        header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; padding-bottom: 34px; border-bottom: 1px solid var(--line); }}
        .brand {{ color: var(--ink); font-family: Fraunces, Georgia, serif; font-weight: 800; letter-spacing: .08em; font-size: 22px; }}
        .subtitle {{ margin-top: 8px; color: var(--steel); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; }}
        .stamp {{ color: var(--ink); border: 1px solid var(--ink); padding: 9px 12px; font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }}
        .intro {{ padding: 34px 0 26px; }}
        .eyebrow {{ color: var(--ink); font-size: 11px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }}
        h1 {{ margin: 10px 0 8px; color: var(--ink); font-family: Fraunces, Georgia, serif; font-size: 34px; line-height: 1.05; }}
        .product {{ color: var(--steel); font-size: 16px; }}
        .code {{ display: inline-block; margin-top: 18px; padding: 9px 12px; background: #F0EAF2; color: var(--ink); font-family: "Space Mono", monospace; font-weight: 700; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }}
        h2 {{ margin: 0 0 14px; color: var(--ink); font-size: 15px; letter-spacing: .08em; text-transform: uppercase; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td {{ padding: 11px 0; border-bottom: 1px solid var(--line); font-size: 14px; }}
        td:last-child {{ text-align: right; color: var(--ink); font-family: "Space Mono", monospace; font-weight: 700; white-space: nowrap; }}
        .total {{ margin-top: 20px; padding: 18px 0; border-top: 2px solid var(--violet); border-bottom: 2px solid var(--violet); display: flex; justify-content: space-between; gap: 16px; font-weight: 800; }}
        .total strong {{ color: var(--violet); font-family: "Space Mono", monospace; white-space: nowrap; }}
        ul {{ padding: 0; margin: 0; list-style: none; }}
        li {{ display: flex; justify-content: space-between; gap: 16px; padding: 10px 0; border-bottom: 1px solid var(--line); font-size: 13px; }}
        li span {{ color: var(--steel); white-space: nowrap; }}
        footer {{ margin-top: 38px; padding-top: 18px; border-top: 1px solid var(--line); color: var(--steel); font-family: "Space Mono", monospace; font-size: 10px; line-height: 1.6; }}
        .actions {{ max-width: 860px; margin: 0 auto 32px; text-align: right; }}
        button {{ border: 0; padding: 12px 18px; background: var(--ink); color: white; cursor: pointer; font-weight: 700; }}
        @media print {{ body {{ background: white; }} .sheet {{ margin: 0; box-shadow: none; max-width: none; }} .actions {{ display: none; }} }}
        @media (max-width: 680px) {{ .sheet {{ margin: 0; padding: 32px 22px; }} header, .grid {{ display: block; }} .stamp {{ display: inline-block; margin-top: 20px; }} .grid > section + section {{ margin-top: 30px; }} }}
    </style>
</head>
<body>
    <main class="sheet">
        <header><div><div class="brand">X BLEUE PRINT</div><div class="subtitle">Calcul de conformité douanière</div></div><div class="stamp">Devis estimatif</div></header>
        <section class="intro"><div class="eyebrow">Sénégal · CEDEAO · UEMOA</div><h1>Plan de coût importation</h1><div class="product">{escape(result.product_label)}</div><div class="code">CODE SH {escape(result.code_sh)}</div></section>
        <div class="grid"><section><h2>Décomposition</h2><table>{cost_rows}</table><div class="total"><span>Total estimé</span><strong>{result.total_cost:,.2f} {result.currency}</strong></div></section><section><h2>Documents</h2><ul>{documents}</ul></section></div>
        <footer>Généré avec BLEUE PRINT — {date.today().isoformat()}<br>{escape(result.legal_note)}</footer>
    </main>
    <div class="actions"><button onclick="window.print()">Imprimer / enregistrer en PDF</button></div>
</body>
</html>"""
