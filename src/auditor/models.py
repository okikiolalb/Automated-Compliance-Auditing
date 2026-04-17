from pydantic import BaseModel, Field
from typing import List

class Room(BaseModel):
    id: str
    name: str
    area: float = Field(..., gt=0)
    height: float = Field(..., gt=0)

class AuditFailure(BaseModel):
    rule_id: str
    reason: str

class RoomAuditResult(BaseModel):
    room_id: str
    room_name: str
    is_compliant: bool
    failures: List[AuditFailure] = []

class AuditReport(BaseModel):
    total_rooms: int
    compliant_rooms: int
    non_compliant_rooms: int
    results: List[RoomAuditResult]
