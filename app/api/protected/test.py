from typing import Any
from fastapi import APIRouter, Depends
from langchain_chroma import Chroma
from requests import Session
from app.core.exceptions import NotFound
from app.db.crud.user import get_user_by_firebase_uid
from app.dependencies import get_current_user, get_db, get_vectordb
from app.schemas.ai import QueryInput
from app.schemas.auth import TokenData
from app.schemas.user import User
from langchain.chains import RetrievalQA
from app.ai.base import llm


router = APIRouter(prefix="/test", tags=["test"])

@router.post("/me")
async def read_current_user(
    query_input: QueryInput,
    # token_data: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
    vectordb: Chroma = Depends(get_vectordb),
) -> Any:
    """
    현재 로그인한 사용자 정보 조회
    """

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever()
    )
    result = qa_chain.invoke({"query": query_input.query})
    return {"answer": result["result"]}