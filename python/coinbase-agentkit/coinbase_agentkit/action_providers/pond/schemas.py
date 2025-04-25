"""Schemas for Allora action provider."""

from pydantic import BaseModel, Field


class BaseWalletSummarySchema(BaseModel):
    """Input schema for getting Base wallet summary."""
    
    address: str = Field(..., description="The Base address to summarize")
    duration_months: int = Field(..., description="Duration in months (1, 3, 6, or 12)")
