
def infer_disease(features):
    tb = features.get('Total_Bilirubin', 0)
    db = features.get('Direct_Bilirubin', 0)
    alp = features.get('Alkaline_Phosphotase', 0)
    alt = features.get('Alamine_Aminotransferase', 0)
    ast = features.get('Aspartate_Aminotransferase', 0)
    tp = features.get('Total_Protiens', 0)
    alb = features.get('Albumin', 0)
    agr = features.get('Albumin_and_Globulin_Ratio', 1)
    age = features.get('Age', 0)
    diseases, reasons = [], []
    if tb > 2 and db > 1 and alp > 250 and alt < 100:
        diseases.append('Obstructive Jaundice / Cholestasis')
        reasons.append('High bilirubin and ALP with lower ALT suggests cholestasis.')
    if (alt > 150 or ast > 150) and abs(alt - ast) < 100:
        diseases.append('Acute Hepatitis (A/E or drug-induced)')
        reasons.append('Very high transaminases indicate acute hepatocellular injury.')
    if (alt > 70 or ast > 70) and agr < 1.0 and alb < 3.5:
        diseases.append('Chronic Viral Hepatitis (B/C likely)')
        reasons.append('Moderately elevated transaminases with low A/G ratio and low albumin suggest chronic hepatitis.')
    if ast / (alt + 1) > 1.5 and alb < 3.5 and age > 40:
        diseases.append('Alcoholic Liver Disease / Cirrhosis')
        reasons.append('AST >> ALT with low albumin suggests alcoholic damage or cirrhosis.')
    if alt > 40 and ast > 40 and alp < 150 and alb < 3.8:
        diseases.append('Non-alcoholic Fatty Liver Disease (NAFLD) / Steatosis')
        reasons.append('Mild-moderate transaminase elevation with normal ALP suggests fatty liver.')
    if alp > 300 and tb > 2:
        diseases.append('Primary Biliary/Cholestatic Disease')
        reasons.append('Very high ALP and bilirubin suggest cholestatic autoimmune processes.')
    if alb < 3.2 and agr < 0.9 and (ast > 80 or alt > 80):
        diseases.append('Cirrhosis / Advanced Fibrosis')
        reasons.append('Low albumin, low A/G ratio and elevated transaminases consistent with advanced disease.')
    if not diseases:
        diseases.append('Non-specific Liver Abnormality / Early-stage Disease')
        reasons.append('Lab abnormalities present but non-specific; further tests recommended.')
    return {'diseases': diseases, 'primary': diseases[0], 'explanation': reasons[0]}
