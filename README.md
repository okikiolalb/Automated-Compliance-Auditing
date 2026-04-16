
https://github.com/user-attachments/assets/f22bba72-8070-4796-8069-6e7a0f7a0932


# Automated-Compliance-Auditing
An AI-powered BIM automation tool for Portuguese building code (RGEU) compliance, taking into account the proposed transiton to the "Código da Construção".
## Executive Summary
A technical solution for automating Portuguese building code {(RGEU) / "Código da Construção"} verification within BIM environments. 

## Key Features
* **Automated Audit:** Validates Art. 65 (Heights) and Art. 67 (Areas).
* **Visual Feedback:** Real-time color-coding of non-compliant zones.
* **Risk Management:** Minimizes the 15% manual error rate in "Simplex Urbanístico" filings.

## Why this matters for Product Management
This project demonstrates the ability to solve a localized B2B pain point by translating legal constraints into a scalable software logic. It highlights a focus on **User Experience for Architects** and **Process Optimization**.

### 🐍 Running the Python Logic Standalone (No Revit Required)
If you are on macOS or do not have Revit installed, you can verify the compliance logic using the included test suite.

#### Installation
1. Open your Terminal and navigate to the project folder.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Running the Engine
You can run the main execution script that accepts external JSON files as input or runs a mock demonstration:
```bash
# Run with mock data
python -m src.main
# Run with custom JSON file
python -m src.main --input path/to/bim_data.json --output report.json
```

#### Running Tests
This project includes a complete test suite:
```bash
python -m pytest tests/
```
   
## Contact
[Okikiola Layi-Balogun] - [www.linkedin.com/in/okikiola-layi-balogun]
