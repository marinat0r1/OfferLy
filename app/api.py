from fastapi import APIRouter
from .schemas import QueryRequest, QueryResponse
from .services import call_gpt_question, call_gpt_offer

router = APIRouter()

@router.post("/process", response_model=QueryResponse)
async def process_request(request: QueryRequest):
    if request.query_type == "question":
        gpt_output = call_gpt_question(request.content)
        return QueryResponse(
            query_type="question",
            input=request.content,
            output=gpt_output
        )
    elif request.query_type == "offer":
        gpt_output = call_gpt_offer(request.content, request.metadata)
        return QueryResponse(
            query_type="offer",
            input=request.content,
            output=gpt_output
        )
    else:
        return {"error": "Invalid query_type. Use 'question' or 'offer'."}
