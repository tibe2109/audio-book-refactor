#!/usr/bin/env python3
# Wrapper script for arf_01_pdf_structure_extractor skill
import sys
import os

# Add repo root to path
cur = os.path.dirname(os.path.abspath(__file__))
while cur and cur != os.path.dirname(cur):
    if os.path.exists(os.path.join(cur, "core", "extract_pdf_structure.py")):
        if cur not in sys.path:
            sys.path.insert(0, cur)
        break
    cur = os.path.dirname(cur)

from core.extract_pdf_structure import main

if __name__ == "__main__":
    main()
