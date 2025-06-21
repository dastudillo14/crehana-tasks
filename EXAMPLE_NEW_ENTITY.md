# Ejemplo: Agregar Nueva Entidad "User"

Este documento muestra cómo agregar una nueva entidad `User` siguiendo la estructura modular refactorizada.

## 1. Crear la Entidad de Dominio

```python
# src/domain/entities/user.py
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self):
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def change_role(self, new_role: UserRole):
        self.role = new_role
        self.updated_at = datetime.utcnow()
```

## 2. Actualizar el __init__.py de entidades

```python
# src/domain/entities/__init__.py
from .task_list import TaskList
from .task import Task, TaskStatus, TaskPriority
from .user import User, UserRole

__all__ = ["TaskList", "Task", "TaskStatus", "TaskPriority", "User", "UserRole"]
```

## 3. Crear el Repositorio de Dominio

```python
# src/domain/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.user import User, UserRole


class UserRepository(ABC):
    """Repository interface for User operations"""
    
    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[User]:
        """Get all users"""
        pass
    
    @abstractmethod
    async def get_by_role(self, role: UserRole) -> List[User]:
        """Get users by role"""
        pass
    
    @abstractmethod
    async def get_active_users(self) -> List[User]:
        """Get all active users"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Update a user"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete a user"""
        pass
```

## 4. Actualizar el __init__.py de repositorios

```python
# src/domain/repositories/__init__.py
from .task_list_repository import TaskListRepository
from .task_repository import TaskRepository
from .user_repository import UserRepository

__all__ = ["TaskListRepository", "TaskRepository", "UserRepository"]
```

## 5. Crear los DTOs

```python
# src/application/dtos/user_dtos.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from ...domain.entities.user import UserRole


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.USER


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total_count: int
    active_count: int
```

## 6. Actualizar el __init__.py de DTOs

```python
# src/application/dtos/__init__.py
from .task_list_dtos import (
    CreateTaskListRequest, UpdateTaskListRequest, TaskListResponse,
    TaskListWithTasksResponse, TaskListWithFilteredTasksResponse
)
from .task_dtos import (
    CreateTaskRequest, UpdateTaskRequest, UpdateTaskStatusRequest, TaskResponse,
    TaskFilterRequest
)
from .user_dtos import (
    CreateUserRequest, UpdateUserRequest, UserResponse, UserListResponse
)

__all__ = [
    "CreateTaskListRequest", "UpdateTaskListRequest", "TaskListResponse",
    "TaskListWithTasksResponse", "TaskListWithFilteredTasksResponse",
    "CreateTaskRequest", "UpdateTaskRequest", "UpdateTaskStatusRequest", "TaskResponse",
    "TaskFilterRequest",
    "CreateUserRequest", "UpdateUserRequest", "UserResponse", "UserListResponse"
]
```

## 7. Crear los Casos de Uso

```python
# src/application/use_cases/user_use_cases.py
from datetime import datetime
from typing import List, Optional
from ...domain.entities.user import User, UserRole
from ...domain.repositories.user_repository import UserRepository
from ..dtos.user_dtos import (
    CreateUserRequest, UpdateUserRequest, UserResponse, UserListResponse
)


class UserUseCases:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        """Create a new user"""
        # Check if user with email already exists
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        user = User(
            email=request.email,
            name=request.name,
            role=request.role,
            created_at=datetime.utcnow()
        )
        
        created_user = await self.user_repo.create(user)
        
        return UserResponse(
            id=created_user.id,
            email=created_user.email,
            name=created_user.name,
            role=created_user.role,
            is_active=created_user.is_active,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at
        )

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        """Get a user by ID"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    async def get_all_users(self) -> UserListResponse:
        """Get all users with statistics"""
        users = await self.user_repo.get_all()
        active_users = await self.user_repo.get_active_users()
        
        user_responses = [
            UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]
        
        return UserListResponse(
            users=user_responses,
            total_count=len(users),
            active_count=len(active_users)
        )

    async def update_user(self, user_id: int, request: UpdateUserRequest) -> Optional[UserResponse]:
        """Update a user"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None
        
        # Update fields if provided
        if request.name is not None:
            user.name = request.name
        if request.role is not None:
            user.change_role(request.role)
        if request.is_active is not None:
            if request.is_active:
                user.activate()
            else:
                user.deactivate()
        
        updated_user = await self.user_repo.update(user)
        
        return UserResponse(
            id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
            role=updated_user.role,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        return await self.user_repo.delete(user_id)
```

## 8. Actualizar el __init__.py de casos de uso

```python
# src/application/use_cases/__init__.py
from .task_list_use_cases import TaskListUseCases
from .task_use_cases import TaskUseCases
from .user_use_cases import UserUseCases

__all__ = ["TaskListUseCases", "TaskUseCases", "UserUseCases"]
```

## 9. Crear el Modelo de Infraestructura

```python
# src/infrastructure/models/user_model.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum
from ..database import Base
from ...domain.entities.user import UserRole


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
```

## 10. Actualizar el __init__.py de modelos

```python
# src/infrastructure/models/__init__.py
from .task_list_model import TaskListModel
from .task_model import TaskModel
from .user_model import UserModel

__all__ = ["TaskListModel", "TaskModel", "UserModel"]
```

## 11. Crear el Repositorio de Infraestructura

```python
# src/infrastructure/repositories/user_repository.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from ...domain.entities.user import User, UserRole
from ...domain.repositories.user_repository import UserRepository
from ..models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            name=user.name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        
        return User(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    async def get_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        db_user = result.scalar_one_or_none()
        
        if not db_user:
            return None
        
        return User(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            role=db_user.role,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    async def get_all(self) -> List[User]:
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        
        return [
            User(
                id=db_user.id,
                email=db_user.email,
                name=db_user.name,
                role=db_user.role,
                is_active=db_user.is_active,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
            for db_user in db_users
        ]

    async def get_by_role(self, role: UserRole) -> List[User]:
        stmt = select(UserModel).where(UserModel.role == role)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        
        return [
            User(
                id=db_user.id,
                email=db_user.email,
                name=db_user.name,
                role=db_user.role,
                is_active=db_user.is_active,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
            for db_user in db_users
        ]

    async def get_active_users(self) -> List[User]:
        stmt = select(UserModel).where(UserModel.is_active == True)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        
        return [
            User(
                id=db_user.id,
                email=db_user.email,
                name=db_user.name,
                role=db_user.role,
                is_active=db_user.is_active,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
            for db_user in db_users
        ]

    async def update(self, user: User) -> User:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                name=user.name,
                role=user.role,
                is_active=user.is_active,
                updated_at=user.updated_at
            )
        )
        
        await self.session.execute(stmt)
        await self.session.commit()
        
        return user

    async def delete(self, user_id: int) -> bool:
        stmt = delete(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        return result.rowcount > 0
```

## 12. Actualizar el __init__.py de repositorios de infraestructura

```python
# src/infrastructure/repositories/__init__.py
from .task_list_repository import SQLAlchemyTaskListRepository
from .task_repository import SQLAlchemyTaskRepository
from .user_repository import SQLAlchemyUserRepository

__all__ = ["SQLAlchemyTaskListRepository", "SQLAlchemyTaskRepository", "SQLAlchemyUserRepository"]
```

## 13. Crear las Rutas de la API

```python
# src/api/user_routes.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.database import get_db_session
from ..infrastructure.repositories import SQLAlchemyUserRepository
from ..application.use_cases import UserUseCases
from ..application.dtos import (
    CreateUserRequest, UpdateUserRequest, UserResponse, UserListResponse
)

user_router = APIRouter(prefix="/users", tags=["Users"])


async def get_user_use_cases(session: AsyncSession = Depends(get_db_session)) -> UserUseCases:
    user_repo = SQLAlchemyUserRepository(session)
    return UserUseCases(user_repo)


@user_router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Create a new user"""
    try:
        return await use_cases.create_user(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/", response_model=UserListResponse)
async def get_all_users(
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Get all users with statistics"""
    return await use_cases.get_all_users()


@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Get a specific user by ID"""
    user = await use_cases.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UpdateUserRequest,
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Update a user"""
    user = await use_cases.update_user(user_id, request)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Delete a user"""
    success = await use_cases.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
```

## 14. Actualizar app.py

```python
# app.py (agregar al final)
from src.api.user_routes import user_router

# Include routers
app.include_router(task_list_router)
app.include_router(task_router)
app.include_router(user_router)  # Nueva línea
```

## Resumen

Con esta nueva estructura modular, agregar una nueva entidad como `User` es mucho más sencillo y organizado:

1. **Separación clara**: Cada archivo tiene una responsabilidad específica
2. **Fácil navegación**: Todo el código relacionado con User está en archivos específicos
3. **Escalabilidad**: No afecta el código existente de Task y TaskList
4. **Mantenibilidad**: Cambios en User no impactan otras entidades
5. **Testing**: Pruebas más granulares y organizadas

La arquitectura hexagonal se mantiene intacta, solo la organización interna ha mejorado significativamente. 