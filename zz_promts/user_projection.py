from typing import List, Optional
from pydantic import BaseModel, Field, computed_field, field_validator
from beanie import PydanticObjectId
from datetime import date, datetime

from models.application.projection import (
    ApplicationProjAuthentificatedFlat,
    ApplicationProjBasic,
    ApplicationProjPrivateFlat,
    ApplicationProjPublicFlat,
)
from models.utils.utils import (
    DataAllRecords,
    DataRecord,
    Permission,
    UserAccessState,
    UserRole,
    Username,
)


class UserProjBasic(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    usernames: List[DataRecord[Username]] = Field(exclude=True)

    @computed_field
    @property
    def username(self) -> str | None:
        if not self.usernames:
            return None
        else:
            ordered_usernames = self.usernames.copy()
            ordered_usernames.sort(key=lambda a: a.updated_on, reverse=True)
            return f"@{ordered_usernames[0].value}"


class UserProjPublicFlat(UserProjBasic):
    firstname: str
    middlename: str | None = None
    lastname: str

    # fullname
    @computed_field
    @property
    def fullname(self) -> str:
        if self.middlename:
            return f"{self.firstname} {self.middlename} {self.lastname}"
        else:
            return f"{self.firstname} {self.lastname}"

    gender: str
    is_verified: bool

    # state
    state: DataAllRecords[DataRecord[UserAccessState]] | UserAccessState

    @field_validator("state")
    @classmethod
    def format_state(cls, value) -> UserAccessState:
        if isinstance(value, DataAllRecords[DataRecord[UserAccessState]]):
            return value.current.value
        return value

    created_on: datetime
    role: UserRole

    # Role base data
    applications: Optional[List[ApplicationProjBasic]] = Field(default_factory=list)
    agency: Optional["AgencyProjBasic"] = Field(None)

    def model_dump(self, **kwards):
        # NOTE: The exclusion theorie via model_dump should be defined at the toppest level 
        # Inorder to be inherited by child
        # We even handle exclusion of field that are present only in some children models her
        # We do this only at the top leve to avoid overriding exclusion logic of parents
        
        kwards.setdefault("exclude", set())
        if not UserRole.is_candidate(self.role):
            # only Candidates have applications
            kwards["exclude"].add("applications")
        else:
            # Candidates don't have permissions
            kwards["exclude"].add("permissions")

        if not UserRole.is_admin(self.role):
            # only Admins have agency
            kwards["exclude"].add("agency")

        return super().model_dump(**kwards)


class UserProjPublicShallow(UserProjPublicFlat):
    applications: Optional[List[ApplicationProjPublicFlat]] = Field(
        default_factory=list
    )
    agency: Optional["AgencyProjPublicFlat"] = Field(None)


class UserProjAuthentificatedFlat(UserProjPublicFlat):
    pass


class UserProjAuthentificatedShallow(
    UserProjAuthentificatedFlat, UserProjPublicShallow
):
    applications: Optional[List[ApplicationProjAuthentificatedFlat]] = Field(
        default_factory=list
    )
    agency: Optional["AgencyProjAuthentificatedFlat"] = Field(None)


class UserProjPrivateFlat(UserProjAuthentificatedFlat):
    birthdate: date

    # age
    @computed_field
    @property
    def age(self) -> int:
        bd = self.birthdate
        today = date.today()
        return today.year - bd.year - ((bd.month, bd.day) < (today.month, today.day))

    contacts: object
    address: object
    email: str

    permissions: Optional[List[Permission]] = Field(default_factory=list)


class UserProjPrivateShallow(UserProjPrivateFlat, UserProjAuthentificatedShallow):
    applications: Optional[List[ApplicationProjPrivateFlat]] = Field(
        default_factory=list
    )
    agency: Optional["AgencyProjPrivateFlat"] = Field(None)
