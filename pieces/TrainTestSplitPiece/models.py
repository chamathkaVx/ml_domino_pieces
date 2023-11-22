from pydantic import BaseModel, Field
from typing import List


class InputModel(BaseModel):
    """
    Input data for TextSummarizerPiece
    """
    data = List[dict] = Field(
        title="Data",
        description="The data to be split.",
        json_schema_extra={"from_upstream": "always"}
    )
    test_data_size: float = Field(
        default=0.8,
        description="The size (%) of the test data.",
        title="Test Data Size",
    )
    random_state: int = Field(
        default=42,
        description="The random state for the split.",
        title="Random State",
    )


class OutputModel(BaseModel):
    """
    Output data for TextSummarizerPiece
    """
    train_data: List[dict]
    test_data: List[dict]