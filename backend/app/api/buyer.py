from fastapi import APIRouter

from app.schemas.buyer import BuyerHomeResponse, BuyerStoryResponse

router = APIRouter(prefix="/buyer", tags=["buyer"])


@router.get("/home", response_model=BuyerHomeResponse)
def get_buyer_home() -> BuyerHomeResponse:
    return BuyerHomeResponse(
        seller_name="SnapBuy Demo Seller",
        announcement="Welcome to SnapBuy V1",
        stories_count=0,
        grid_products_count=0,
    )


@router.get("/campaigns/{campaign_id}/story", response_model=BuyerStoryResponse)
def get_campaign_story(campaign_id: int) -> BuyerStoryResponse:
    return BuyerStoryResponse(campaign_id=campaign_id, campaign_name=f"Campaign {campaign_id}", products_count=0)
