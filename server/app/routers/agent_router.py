import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.agent import QueryRequest, QueryResponse
from app.services.agent_service import AgentService
from app.dependencies import get_agent_service
from app.exceptions import (
    UnsafeSQLException,
    SQLGenerationException,
    DatabaseQueryException,
    GuardrailException,
    RateLimitException
)

router = APIRouter(prefix="/agent", tags=["Agent"])
logger = logging.getLogger(__name__)

@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def query_agent(
    payload: QueryRequest,
    service: AgentService = Depends(get_agent_service),
) -> QueryResponse:
    try:
        return service.run(payload.question)
    except UnsafeSQLException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except SQLGenerationException as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except DatabaseQueryException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except GuardrailException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except RateLimitException as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in POST /agent/query")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error. Please try again.",
        )