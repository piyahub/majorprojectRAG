from fastapi import Header, HTTPException, status
from app.core.config import settings

def admin_required(
    x_admin_key: str = Header(..., alias="x-admin-key")
):
    if x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    return x_admin_key
