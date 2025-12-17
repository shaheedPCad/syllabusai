from app.schemas.user import UserRead
from app.schemas.course import CourseCreate, CourseRead, CourseJoin
from app.schemas.document import DocumentRead
from app.schemas.chat import ChatRequest, ChatResponse, DocumentSource
from app.schemas.study import (
    Flashcard,
    FlashcardSet,
    FlashcardResponse,
    FlashcardRequest,
    QuizQuestion,
    QuizSet,
    QuizResponse,
    QuizRequest,
    StudyNoteRequest,
    StudyNoteResponse,
    StudyHistoryItem,
    StudyHistoryResponse,
)
from app.schemas.friend import FriendRead, FriendshipRead, FriendRequestCreate, FriendRequestAccept
from app.schemas.mentor import UserBasic, MentorProfileRead, MentorFollowCreate
from app.schemas.lesson import LessonCreate, LessonRead, LessonProgressRead, LessonProgressUpdate
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.schemas.inbox import MessageCreate, MessageRead
from app.schemas.dashboard import DashboardStats, CourseProgressStats

__all__ = [
    "UserRead",
    "CourseCreate",
    "CourseRead",
    "CourseJoin",
    "DocumentRead",
    "ChatRequest",
    "ChatResponse",
    "DocumentSource",
    "Flashcard",
    "FlashcardSet",
    "FlashcardResponse",
    "FlashcardRequest",
    "QuizQuestion",
    "QuizSet",
    "QuizResponse",
    "QuizRequest",
    "StudyNoteRequest",
    "StudyNoteResponse",
    "StudyHistoryItem",
    "StudyHistoryResponse",
    # Dashboard schemas
    "FriendRead",
    "FriendshipRead",
    "FriendRequestCreate",
    "FriendRequestAccept",
    "UserBasic",
    "MentorProfileRead",
    "MentorFollowCreate",
    "LessonCreate",
    "LessonRead",
    "LessonProgressRead",
    "LessonProgressUpdate",
    "TaskCreate",
    "TaskUpdate",
    "TaskRead",
    "MessageCreate",
    "MessageRead",
    "DashboardStats",
    "CourseProgressStats",
]
