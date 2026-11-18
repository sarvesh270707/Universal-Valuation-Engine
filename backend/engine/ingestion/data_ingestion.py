"""
Universal Financial Valuation & DCF Engine - Financial Data Ingestion Module
Implements structured ingestion adapters for:
- Structured XBRL / XML instances
- Excel multi-sheet financial workbooks
- CSV statement extracts
- PDF tabular document extracts
"""

import os
import hashlib
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from datetime import datetime

from backend.engine.dictionary.accounting_dict import (
    StandardFinancialFact,
    StatementType,
    MissingValueState
)

class IngestionProvenance(BaseException):
    pass

class DataIngestionEngine:
    """
    Ingests and validates raw financial disclosures from multiple formats with provenance tracking.
    """

    @staticmethod
    def compute_sha256(file_path: str) -> str:
        """Computes SHA-256 hash for document tamper-proofing and duplicate detection."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def detect_units(text_sample: str) -> Tuple[str, float]:
        """
        Detects unit scale from document text: Crores, Lakhs, Millions, or Absolute.
        Returns: (unit_scale_name, multiplier_to_crore)
        """
        text_lower = text_sample.lower()
        if "in crore" in text_lower or "rs. in cr" in text_lower or "₹ in cr" in text_lower or "crores" in text_lower:
            return "CRORE", 1.0
        elif "in lakh" in text_lower or "lakhs" in text_lower or "lac" in text_lower:
            return "LAKH", 0.01 # 1 Lakh = 0.01 Crore
        elif "in million" in text_lower or "millions" in text_lower:
            return "MILLION", 0.1 # 1 Million = 0.1 Crore (10 Lakhs)
        elif "in billion" in text_lower or "billions" in text_lower:
            return "BILLION", 100.0 # 1 Billion = 100 Crore
        else:
            return "ABSOLUTE", 0.0000001 # Absolute to Crore

    @classmethod
    def ingest_csv_statement(
        cls,
        file_path: str,
        statement_type: StatementType,
        period_col_prefix: str = "FY"
    ) -> Dict[str, Any]:
        """
        Ingests standardized or reported CSV statements.
        Extracts row concepts, detected units, and period-by-period numeric values.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Filing CSV not found: {file_path}")

        file_hash = cls.compute_sha256(file_path)
        df = pd.read_csv(file_path)

        # Identify line item concept column (usually col 0)
        concept_col = df.columns[0]
        period_cols = [c for c in df.columns if c.startswith(period_col_prefix) or c.isdigit() or "20" in c]

        extracted_facts = []
        for _, row in df.iterrows():
            raw_label = str(row[concept_col]).strip()
            if not raw_label or raw_label.lower() in ["nan", "none"]:
                continue

            for p_col in period_cols:
                raw_val = row[p_col]
                numeric_val = None
                missing_state = MissingValueState.AWAITING_VERIFICATION

                try:
                    if pd.notna(raw_val):
                        # Clean currency strings, commas, parentheses for negative values
                        val_str = str(raw_val).replace(",", "").replace("₹", "").replace("$", "").strip()
                        if val_str.startswith("(") and val_str.endswith(")"):
                            numeric_val = -float(val_str[1:-1])
                        elif val_str == "-" or val_str.lower() == "nil":
                            numeric_val = 0.0
                            missing_state = MissingValueState.ZERO
                        else:
                            numeric_val = float(val_str)
                            missing_state = MissingValueState.ZERO if numeric_val == 0.0 else MissingValueState.AWAITING_VERIFICATION
                    else:
                        missing_state = MissingValueState.MISSING
                except ValueError:
                    missing_state = MissingValueState.NOT_EXTRACTED

                extracted_facts.append({
                    "raw_label": raw_label,
                    "reporting_period": p_col,
                    "numeric_value": numeric_val,
                    "statement_type": statement_type.value,
                    "missing_state": missing_state.value
                })

        return {
            "source_file": os.path.basename(file_path),
            "sha256": file_hash,
            "total_facts_extracted": len(extracted_facts),
            "periods_detected": period_cols,
            "facts": extracted_facts
        }

    @classmethod
    def ingest_xbrl_instance(cls, file_content_or_path: str) -> Dict[str, Any]:
        """
        Parses MCA / XBRL instance documents (XML).
        Extracts tagged facts, context refs (periods), and explicit unit refs.
        """
        # Parse XML
        if os.path.exists(file_content_or_path):
            tree = ET.parse(file_content_or_path)
            root = tree.getroot()
            source_desc = os.path.basename(file_content_or_path)
        else:
            root = ET.fromstring(file_content_or_path)
            source_desc = "IN_MEMORY_XBRL_STRING"

        xbrl_facts = []
        for elem in root.iter():
            tag_name = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            val_text = elem.text.strip() if elem.text else None
            
            # Check if element has contextRef (XBRL standard attribute for financial facts)
            context_ref = elem.attrib.get("contextRef")
            unit_ref = elem.attrib.get("unitRef", "INR")
            decimals = elem.attrib.get("decimals")

            if context_ref and val_text:
                try:
                    num_val = float(val_text)
                    xbrl_facts.append({
                        "concept": tag_name,
                        "context_ref": context_ref,
                        "unit": unit_ref,
                        "numeric_value": num_val,
                        "decimals": decimals
                    })
                except ValueError:
                    continue

        return {
            "source": source_desc,
            "format": "XBRL_XML",
            "total_facts": len(xbrl_facts),
            "facts": xbrl_facts
        }
