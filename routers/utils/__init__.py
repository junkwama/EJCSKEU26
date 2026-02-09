from pydantic import BaseModel
from typing import Type, TypeVar
from utils.constants import ProjDepth

P = TypeVar('P', bound=BaseModel)

def apply_projection(
    data: object,
    FlatProjection: Type[P],
    ShallowProjection: Type[P],
    proj_type: ProjDepth = ProjDepth.SHALLOW,
) -> P:
    """
    Generic function to select between flat and shallow projections
    
    Args:
        data: SQLModel instance to convert
        FlatProjection: Flat projection class
        ShallowProjection: Shallow projection class
        proj_type: "flat" or "shallow" (default: "shallow")
    
    Returns:
        Projection instance of appropriate type

    """
    
    projection_class = FlatProjection if proj_type == ProjDepth.FLAT else ShallowProjection
    return projection_class.model_validate(data)
