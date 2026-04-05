from pydantic import BaseModel


class BuyerHomeResponse(BaseModel):
    seller_name: str
    announcement: str
    stories_count: int
    grid_products_count: int


class BuyerStoryResponse(BaseModel):
    campaign_id: int
    campaign_name: str
    products_count: int
