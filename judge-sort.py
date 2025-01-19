import pandas as pd
judges = pd.DataFrame

try:
    judges = pd.read_csv("data-in/judges.csv")
except:
    raise FileNotFoundError("Failed to read CSV file. Ensure the judges.csv file exists")

expected_headers = ['Email', 'CC email (assistant or other colleague)', 'Mobile phone (Used only for comms at an event. No marketing.)', 'First name', 
                    'Last name', 'Job title', 'Company name', 'City', 'Preferred Pronouns', 'Ethnic Group', 
                    'If you are neurodivergent, please check this box so that we can get in touch with you to discuss any specific requirements you may have to ensure your experience with us is as productive and enjoyable as possible', 
                    'Are you part of an Agency Holding Company?', "If you selected 'Other', which one?\xa0", 'Company type', 'If you selected "Other", which one?', 
                    'Job Role/Department', 'Seniority Level', 'Years of Experience', 'Brand # 1', 'Brand # 2', 'Brand # 3', 'First choice for judging', 'Second choice for judging', 
                    '<p>If judging in-person on 5th September, are you able to join us for the drinks reception afterwards?</p>\n<p>(6pm-8pm)</p>',
                    'Have you judged for the Effies in the past?', 'If you’re new to Effie judging or would like a refresher we’re holding two online training sessions.\xa0 Please choose the session you would like to join.', 
                    'Dietary Restrictions/Allergies (for in-person judging)', 'Are you interested in any of the following?', 
                    'Conversion Date', 'Conversion Page', 'Conversion Title', 'Contact first name', 'Contact last name', 'Contact email', 'Contact ID']


if judges.columns.to_list() != expected_headers:
    print("This dataset does not contain the required headers.\nPlease ensure that you have placed the correct file in data-in/judges.csv")  

    missing_headers = [header for header in expected_headers if header not in judges.columns.to_list()]
    extra_headers = [header for header in judges.columns.to_list() if header not in expected_headers]
    
    error_message = "Header validation failed:\n"
    if missing_headers:
        error_message += f"  - Missing headers: {missing_headers}\n"
    if extra_headers:
        error_message += f"  - Unexpected headers: {extra_headers}\n"
    raise ValueError(error_message)