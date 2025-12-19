import pytest
from pydantic import ValidationError
from models.workshop_context import Attendee, WorkshopIngestionInput


# Attendee model tests
def test_attendee_valid():
    attendee = Attendee(
        name="Sarah Robinson",
        job_title="Platform Engineer",
        team="CE",
        company="IBM"
    )

    assert attendee.name == "Sarah Robinson"
    assert attendee.job_title == "Platform Engineer"
    assert attendee.team == "CE"
    assert attendee.company == "IBM"


def test_attendee_minimal_valid():
    attendee = Attendee(name="Alice")
    assert attendee.name == "Alice"
    assert attendee.job_title is None
    assert attendee.team is None
    assert attendee.company is None


def test_attendee_missing_name():
    with pytest.raises(ValidationError):
        Attendee(job_title="Engineer")


def test_attendee_invalid_types():
    with pytest.raises(ValidationError):
        Attendee(name=123)  # name must be string


# WorkshopIngestionInput tests
def test_workshop_input_valid_all_fields():
    data = WorkshopIngestionInput(
        workshop_date="2025-12-11",
        mural_url="https://mural.co/example",
        attendees=[
            Attendee(name="Bob", job_title="Engineer", team="Platform", company="IBM")
        ]
    )

    assert data.workshop_date == "2025-12-11"
    assert str(data.mural_url) == "https://mural.co/example"
    assert len(data.attendees) == 1
    assert data.attendees[0].name == "Bob"


def test_workshop_input_optional_fields_missing():
    data = WorkshopIngestionInput()

    assert data.workshop_date is None
    assert data.mural_url is None
    assert data.attendees is None


def test_workshop_input_invalid_url():
    with pytest.raises(ValidationError):
        WorkshopIngestionInput(
            workshop_date="2025-12-11",
            mural_url="not-a-valid-url"
        )


def test_workshop_input_invalid_attendee_list():
    # attendees must be list of Attendee objects or dicts convertible to Attendee
    with pytest.raises(ValidationError):
        WorkshopIngestionInput(
            attendees=["not-attendee"]
        )


def test_workshop_input_attendee_dict_conversion():
    data = WorkshopIngestionInput(
        attendees=[
            {"name": "Test Person", "job_title": "Designer"}
        ]
    )

    assert len(data.attendees) == 1
    assert isinstance(data.attendees[0], Attendee)
    assert data.attendees[0].name == "Test Person"


def test_workshop_input_multiple_attendees():
    data = WorkshopIngestionInput(
        attendees=[
            Attendee(name="Alice"),
            Attendee(name="Bob", company="OpenAI")
        ]
    )

    assert len(data.attendees) == 2
    assert data.attendees[0].name == "Alice"
    assert data.attendees[1].company == "OpenAI"


def test_workshop_date_string_valid():
    # No date validation is enforced, so it accepts any string
    data = WorkshopIngestionInput(workshop_date="yesterday")
    assert data.workshop_date == "yesterday"


def test_workshop_date_wrong_type():
    with pytest.raises(ValidationError):
        WorkshopIngestionInput(workshop_date=1234)
