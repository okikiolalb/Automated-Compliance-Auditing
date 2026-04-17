import logging
from typing import List
from .models import Room, RoomAuditResult, AuditFailure, AuditReport
from .rules import RGEU_RULES

logger = logging.getLogger(__name__)

class ComplianceEngine:
    def __init__(self, rules: dict = None):
        self.rules = rules or RGEU_RULES

    def audit_room(self, room: Room) -> RoomAuditResult:
        failures = []
        
        # Check Height (Art. 65)
        min_height = self.rules.get("min_height", 2.70)
        if room.height < min_height:
            failures.append(AuditFailure(
                rule_id="ART_65_HEIGHT", 
                reason=f"Height {room.height}m < {min_height}m"
            ))
        
        # Check Area (Art. 67)
        min_areas = self.rules.get("min_areas", {})
        for room_type, min_area in min_areas.items():
            # Simple substring match (e.g., "Sala de Estar" contains "Sala")
            if room_type.lower() in room.name.lower():
                if room.area < min_area:
                    failures.append(AuditFailure(
                        rule_id="ART_67_AREA",
                        reason=f"Area {room.area}m2 < {min_area}m2 for {room_type}"
                    ))
                break # Only apply the first matching rule

        is_compliant = len(failures) == 0
        
        return RoomAuditResult(
            room_id=room.id,
            room_name=room.name,
            is_compliant=is_compliant,
            failures=failures
        )

    def audit_project(self, rooms: List[Room]) -> AuditReport:
        logger.info(f"Starting audit for {len(rooms)} rooms.")
        results = [self.audit_room(room) for room in rooms]
        
        compliant_count = sum(1 for r in results if r.is_compliant)
        
        report = AuditReport(
            total_rooms=len(rooms),
            compliant_rooms=compliant_count,
            non_compliant_rooms=len(rooms) - compliant_count,
            results=results
        )
        logger.info(f"Audit complete. {compliant_count}/{len(rooms)} rooms compliant.")
        return report
