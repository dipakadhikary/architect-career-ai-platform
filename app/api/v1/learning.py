"""Contract-aligned Learning AI endpoints (workflow orchestration)."""

from __future__ import annotations

from acos_ai_contracts.models.evaluate_progress_request import EvaluateProgressRequest
from acos_ai_contracts.models.evaluate_progress_response import EvaluateProgressResponse
from acos_ai_contracts.models.generate_quiz200_response_questions_inner import (
    GenerateQuiz200ResponseQuestionsInner,
)
from acos_ai_contracts.models.quiz_request import QuizRequest
from acos_ai_contracts.models.quiz_response import QuizResponse
from acos_ai_contracts.models.recommend_next_topic_request import RecommendNextTopicRequest
from acos_ai_contracts.models.recommend_next_topic_response import RecommendNextTopicResponse
from fastapi import APIRouter, Depends

from app.api.dependencies import get_agentic_service
from app.orchestration.agentic.service import AgenticOrchestrationService

router = APIRouter(tags=["Learning AI"])


@router.post(
    "/api/v1/ai/learning/quiz/generate",
    response_model=QuizResponse,
    response_model_by_alias=True,
    summary="Generate learning quiz",
)
async def generate_quiz(
    body: QuizRequest,
    service: AgenticOrchestrationService = Depends(get_agentic_service),
) -> QuizResponse:
    output = await service.run_workflow(
        "quiz",
        {
            "user_id": body.user_id,
            "topic": body.topic,
            "difficulty": body.difficulty or "INTERMEDIATE",
            "question_count": body.question_count or 5,
        },
    )
    questions = [
        GenerateQuiz200ResponseQuestionsInner(
            prompt=str(item["prompt"]),
            choices=list(item["choices"]),
            correctAnswer=str(item["correctAnswer"]),
            explanation=item.get("explanation"),
        )
        for item in output.get("questions") or []
    ]
    return QuizResponse(
        quizId=str(output["quiz_id"]),
        topic=str(output["topic"]),
        questions=questions,
    )


@router.post(
    "/api/v1/ai/learning/topics/recommend-next",
    response_model=RecommendNextTopicResponse,
    response_model_by_alias=True,
    summary="Recommend next learning topic",
)
async def recommend_next_topic(
    body: RecommendNextTopicRequest,
    service: AgenticOrchestrationService = Depends(get_agentic_service),
) -> RecommendNextTopicResponse:
    output = await service.run_workflow(
        "recommend_topic",
        {
            "user_id": body.user_id,
            "plan_id": body.plan_id,
            "completed_topics": list(body.completed_topics or []),
            "goals": list(body.goals or []),
        },
    )
    return RecommendNextTopicResponse(
        topic=str(output["topic"]),
        rationale=output.get("rationale"),
        relatedTopics=output.get("related_topics"),
    )


@router.post(
    "/api/v1/ai/learning/progress/evaluate",
    response_model=EvaluateProgressResponse,
    response_model_by_alias=True,
    summary="Evaluate learning progress",
)
async def evaluate_progress(
    body: EvaluateProgressRequest,
    service: AgenticOrchestrationService = Depends(get_agentic_service),
) -> EvaluateProgressResponse:
    output = await service.run_workflow(
        "progress_evaluation",
        {
            "user_id": body.user_id,
            "plan_id": body.plan_id,
            "completed_topics": list(body.completed_topics or []),
            "quiz_scores": list(body.quiz_scores or []),
        },
    )
    return EvaluateProgressResponse(
        progressPercent=float(output["progress_percent"]),
        summary=str(output["summary"]),
        strengths=output.get("strengths"),
        focusAreas=output.get("focus_areas"),
    )
