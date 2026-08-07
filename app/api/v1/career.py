"""Contract-aligned Career AI endpoints (workflow orchestration)."""

from __future__ import annotations

from acos_ai_contracts.models.cover_letter_request import CoverLetterRequest
from acos_ai_contracts.models.cover_letter_response import CoverLetterResponse
from acos_ai_contracts.models.interview_analysis_request import InterviewAnalysisRequest
from acos_ai_contracts.models.interview_analysis_response import InterviewAnalysisResponse
from acos_ai_contracts.models.resume_request import ResumeRequest
from acos_ai_contracts.models.resume_response import ResumeResponse
from fastapi import APIRouter, Depends

from app.api.dependencies import get_agentic_service
from app.orchestration.agentic.service import AgenticOrchestrationService

router = APIRouter(tags=["Career AI"])


@router.post(
    "/api/v1/ai/career/resume/generate",
    response_model=ResumeResponse,
    response_model_by_alias=True,
    summary="Generate tailored resume",
)
async def generate_resume(
    body: ResumeRequest,
    service: AgenticOrchestrationService = Depends(get_agentic_service),
) -> ResumeResponse:
    output = await service.run_workflow(
        "resume",
        {
            "user_id": body.user_id,
            "target_role": body.target_role,
            "experience_highlights": list(body.experience_highlights or []),
            "skills": list(body.skills or []),
        },
    )
    return ResumeResponse(
        content=str(output["content"]),
        format=str(output.get("format") or "markdown"),
    )


@router.post(
    "/api/v1/ai/career/interview/analyze",
    response_model=InterviewAnalysisResponse,
    response_model_by_alias=True,
    summary="Analyze interview transcript",
)
async def analyze_interview(
    body: InterviewAnalysisRequest,
    service: AgenticOrchestrationService = Depends(get_agentic_service),
) -> InterviewAnalysisResponse:
    output = await service.run_workflow(
        "interview",
        {
            "user_id": body.user_id,
            "interview_id": body.interview_id,
            "transcript": body.transcript,
            "job_description": body.job_description,
        },
    )
    return InterviewAnalysisResponse(
        summary=str(output["summary"]),
        strengths=output.get("strengths"),
        improvements=output.get("improvements"),
        score=output.get("score"),
    )


@router.post(
    "/api/v1/ai/career/cover-letter/generate",
    response_model=CoverLetterResponse,
    response_model_by_alias=True,
    summary="Generate cover letter",
)
async def generate_cover_letter(
    body: CoverLetterRequest,
    service: AgenticOrchestrationService = Depends(get_agentic_service),
) -> CoverLetterResponse:
    output = await service.run_workflow(
        "cover_letter",
        {
            "user_id": body.user_id,
            "target_role": body.target_role,
            "company_name": body.company_name,
            "highlights": list(body.highlights or []),
        },
    )
    return CoverLetterResponse(
        content=str(output["content"]),
        format=str(output.get("format") or "plain"),
    )
