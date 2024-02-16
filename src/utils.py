def get_aspect(company_profile: dict, aspect_name: str):
    return company_profile[aspect_name] if aspect_name in company_profile else None