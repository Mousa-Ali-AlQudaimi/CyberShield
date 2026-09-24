from utils.validators import validate_ip, validate_required


class IPAddress:
    total_ips = 0
    valid_statuses = ("active", "blocked", "watchlist")

    def __init__(self, ip_id, address, country="Unknown", status="active", reputation=50):
        self.__ip_id = validate_required(str(ip_id), "IP ID")
        self.address = address
        self.country = country
        self.status = status
        self.reputation = reputation
        IPAddress.total_ips += 1

    @property
    def ip_id(self):
        return self.__ip_id

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = validate_ip(value)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        value = validate_required(value, "Status").lower()
        if value not in self.valid_statuses:
            raise ValueError("Invalid IP status.")
        self.__status = value

    @property
    def reputation(self):
        return self.__reputation

    @reputation.setter
    def reputation(self, value):
        value = int(value)
        if not 0 <= value <= 100:
            raise ValueError("Reputation must be between 0 and 100.")
        self.__reputation = value

    @staticmethod
    def validate_format(ip):
        return validate_ip(ip)

    def block(self):
        self.status = "blocked"

    def unblock(self):
        self.status = "active"

    def is_suspicious(self):
        return self.reputation < 40 or self.status == "watchlist"

    def to_dict(self):
        return {"ip_id": self.ip_id, "address": self.address, "country": self.country,
                "status": self.status, "reputation": self.reputation}

    @classmethod
    def from_dict(cls, data):
        return cls(data["ip_id"], data["address"], data.get("country", "Unknown"),
                   data.get("status", "active"), data.get("reputation", 50))

    def __str__(self):
        return f"{self.address} - {self.status} - reputation {self.reputation}"
