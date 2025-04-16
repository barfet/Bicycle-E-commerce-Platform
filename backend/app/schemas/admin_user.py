from pydantic import BaseModel

# Schema for reading basic admin user info (e.g., for /admin/me)
class AdminUserRead(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True
    }

# We might add Create/Update schemas later if needed 