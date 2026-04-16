import json
import argparse
import sys
import logging
from pydantic import ValidationError
from src.auditor.engine import ComplianceEngine
from src.auditor.models import Room

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Automated Compliance Auditing (RGEU)")
    parser.add_argument("--input", "-i", type=str, help="Path to input JSON file containing room data")
    parser.add_argument("--output", "-o", type=str, help="Path to output JSON report", default=None)
    
    args = parser.parse_args()

    # If no input, run a mock demonstration
    if not args.input:
        logger.info("No input file provided. Running mock data demonstration...")
        mock_data = [
            {"id": "1", "name": "Sala de Estar", "area": 15.5, "height": 2.80},
            {"id": "2", "name": "Quarto 1", "area": 9.0, "height": 2.75},
            {"id": "3", "name": "Cozinha", "area": 7.0, "height": 2.40},
            {"id": "4", "name": "Quarto 2", "area": 11.0, "height": 2.70}
        ]
    else:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                mock_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to read input file: {e}")
            sys.exit(1)

    try:
        rooms = [Room(**data) for data in mock_data]
    except ValidationError as e:
        logger.error(f"Data validation error:\n{e}")
        sys.exit(1)

    engine = ComplianceEngine()
    report = engine.audit_project(rooms)

    report_json = report.model_dump_json(indent=2)
    
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report_json)
            logger.info(f"Report saved to {args.output}")
        except Exception as e:
            logger.error(f"Failed to write output file: {e}")
            sys.exit(1)
    else:
        print("\n--- AUDIT REPORT ---")
        print(report_json)

if __name__ == "__main__":
    main()
