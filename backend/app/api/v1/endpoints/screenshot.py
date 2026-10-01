from fastapi import APIRouter, HTTPException, UploadFile, File


router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)


@router.post(
    "/screenshot",
    summary="Analyze a screenshot",
)
async def analyze_screenshot(
    file: UploadFile = File(...),
):
    """
    Screenshot analysis will be implemented in Phase 9 using OCR.

    The endpoint exists now so the API contract is established,
    but it intentionally does not fabricate an analysis result.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A screenshot file is required.",
        )

    content_type = file.content_type or ""

    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are accepted.",
        )

    raise HTTPException(
        status_code=501,
        detail=(
            "Screenshot analysis is not available yet. "
            "OCR and image processing are scheduled for Phase 9."
        ),
    )
