from fastapi import APIRouter, Depends, HTTPException,Request
from Schema.user_profile_schema import ProfileResponse, ProfileCreate
from sqlalchemy.orm import Session
from Utils.dependency import get_current_user
from Models.user_profile_setup import UserProfile
from Utils.calacutor import calculate_bmr, ACTIVITY_FACTORS
from Database.sql import get_db
router = APIRouter(prefix="/user_profile", tags=["user_profile"])

@router.post("/setup",response_model=ProfileResponse)
def setup_profile(payload:ProfileCreate, request:Request, current_user: int = Depends(get_current_user),db: Session = Depends(get_db),):
    #db : Session = request.state.db

    existing_profile = db.query(UserProfile).filter_by(user_id = current_user.id).first()
    if existing_profile:
        existing_profile.age = payload.age
        existing_profile.height_cm = payload.height_cm
        existing_profile.weight_kg = payload.weight_kg
        existing_profile.gender = payload.gender
        existing_profile.activity_level = payload.activity_level
    else:
        profile = UserProfile(
            user_id = current_user.id,
            **payload.dict()
        )
        db.add(profile)
    db.commit()

    try:
        bmr = calculate_bmr(payload.weight_kg, payload.height_cm, payload.age, payload.gender)
        multiplier = ACTIVITY_FACTORS.get(payload.activity_level, 1.2)
        recommended = int(round(bmr * multiplier))

        recommended = max(1000, recommended)
    except Exception as e:
        recommended = 0
        raise HTTPException(status_code=500, detail="Failed to calculate recommended calories")
    
    response = {
        "user_id": current_user.id,
        "age": payload.age,
        "height_cm": payload.height_cm,
        "weight_kg": payload.weight_kg,
        "gender": payload.gender,
        "activity_level": payload.activity_level,
        "recommended_calories": recommended
    }

    return response