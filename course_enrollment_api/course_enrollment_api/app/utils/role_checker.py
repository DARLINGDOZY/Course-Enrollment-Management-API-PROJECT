from fastapi import HTTPException, status, Query
from typing import Optional

def check_role(role: Optional[str], required_role: str):
    if not role or role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. Required role: {required_role}"
        )

def get_role_from_query(role: str = Query(...)):
    return role
