import pymongo


class DBHandler:
    """Class to handle database connection and updates."""

    def __init__(self) -> None:
        self.myclient = pymongo.MongoClient(
            "mongodb+srv://msuser:LZANoBO7yJWettwR@mshriek.4bfxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        )
        self.db = self.myclient["hubspotVirtualSDRDev"]
        self.col = self.db["profiles"]

    def __enter__(self):
        # Return the object itself when entering the context
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the MongoDB client connection here
        self.myclient.close()

    def get_company_profile(self, company_name):
        """Retrieve a company's profile from the database."""
        company_profile = self.col.find_one({"company_name": company_name})
        return company_profile

    def update_company_profile(self, company_name, updates):
        """Update a company's profile in the database."""
        self.col.update_one({"company_name": company_name}, {"$set": updates})
