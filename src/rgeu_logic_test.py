"""
RGEU Logic Validator - Standalone Test
This script simulates Revit BIM data to test the RGEU compliance engine.
"""

def validate_rgeu(rooms):
    # Dictionary of RGEU Minimums (Art. 67 and Art. 65)
    standards = {
        "Sala": 12.0,
        "Quarto": 10.5,
        "Cozinha": 6.0,
        "Min_Height": 2.70
    }
    
    print(f"{'Room Name':<15} | {'Area':<8} | {'Height':<8} | {'Status'}")
    print("-" * 55)

    for room in rooms:
        name = room['name']
        area = room['area']
        height = room['height']
        
        # Logic Check
        is_compliant = True
        reason = "Pass"

        # Check Height
        if height < standards["Min_Height"]:
            is_compliant = False
            reason = f"Height {height}m < 2.70m"
        
        # Check Area
        for key, min_area in standards.items():
            if key in name and area < min_area:
                is_compliant = False
                reason = f"Area {area}m2 < {min_area}m2"

        status = "✅ PASS" if is_compliant else f"❌ FAIL ({reason})"
        print(f"{name:<15} | {area:<8} | {height:<8} | {status}")

# Mock Data: Simulating what would come out of Revit/Dynamo
mock_bim_data = [
    {"name": "Sala de Estar", "area": 15.5, "height": 2.80},
    {"name": "Quarto 1", "area": 9.0, "height": 2.75},   # Should fail area
    {"name": "Cozinha", "area": 7.0, "height": 2.40},    # Should fail height
    {"name": "Quarto 2", "area": 11.0, "height": 2.70}
]

if __name__ == "__main__":
    print("Running RGEU Compliance Engine Mock Test...\n")
    validate_rgeu(mock_bim_data)
