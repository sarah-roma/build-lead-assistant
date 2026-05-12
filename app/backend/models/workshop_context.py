from pydantic import BaseModel, Field, HttpUrl, ValidationError
from typing import Optional, List
from fastapi import Form, HTTPException


class Attendee(BaseModel):
    name: str = Field(description="Full name of the attendee")
    job_title: Optional[str] = Field(default=None, description="Job title of the attendee")
    team: Optional[str] = Field(default=None, description="Team or department")
    company: Optional[str] = Field(default=None, description="Company the attendee works for")


class WorkshopIngestionInput(BaseModel):
    workshop_date: Optional[str] = Field(
        default=None,
        description="When was the workshop held?"
    )

    attendees: Optional[List[Attendee]] = Field(
        default=None,
        description="List of attendees with their job title, team, and company"
    )
    
    mural_url: Optional[HttpUrl] = Field(
        default=None,
        description="Link to any Mural board or collaborative workspace"
    )


# THIS FUNCTION BUILDS WorkshopIngestionInput FROM form-data
def workshop_form_dependency(
    workshop_date: Optional[str] = Form(None),
    mural_url: Optional[str] = Form(None),

    # attendees.* fields (repeatable in Swagger)
    attendee_names: Optional[List[str]] = Form(None),
    attendee_job_titles: Optional[List[str]] = Form(None),
    attendee_teams: Optional[List[str]] = Form(None),
    attendee_companies: Optional[List[str]] = Form(None),
):
    """ Build WorkshopIngestionInput from form fields, handling repeatable attendee fields."""
    attendees_list = []
    # Build attendees list from form fields (if provided)
    if attendee_names:
        for idx, name in enumerate(attendee_names):
            attendees_list.append(
                Attendee(
                    name=name,
                    job_title=attendee_job_titles[idx] if attendee_job_titles else None,
                    team=attendee_teams[idx] if attendee_teams else None,
                    company=attendee_companies[idx] if attendee_companies else None,
                )
            )
    try:
        return WorkshopIngestionInput(
            workshop_date=workshop_date,
            mural_url=mural_url,
            attendees=attendees_list
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())