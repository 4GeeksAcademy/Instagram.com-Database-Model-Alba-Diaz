from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)

    profile: Mapped["Profiles"] = relationship(
        back_populates="user", uselist=False)
    post: Mapped[list["Posts"]] = relationship(back_populates="user")
    comment: Mapped[list["Comments"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,

            "profile": self.profile.serialize(),
            "post": [post.serialize() for post in self.post],
            "comment": [comment.serialize() for comment in self.comment]

        }


class Followers(db.Model):
    __tablename__ = "followers"
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }


class Comments(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(10000), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="comment")

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Posts"] = relationship(back_populates="comment")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "user": self.user.serialize()

        }


class Posts(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_title: Mapped[str] = mapped_column(String(100))
    post_text: Mapped[str] = mapped_column(String(10000))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="post")
    comment: Mapped[list["Comments"]] = relationship(back_populates="post")
    media: Mapped[list["Medias"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_title": self.post_title,
            "post_text": self.post_text,
            "user": self.user.serialize(),
            "comment": [comment.serialize() for comment in self.comment],
            "media": [media.serialize() for media in self.media]

        }


class Profiles(db.Model):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(String(500))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="profile")

    def serialize(self):
        return {
            "id": self.id,
            "bio": self.bio,
            "user": self.user.serialize()
        }


class MyMedias(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class Medias(db.Model):
    __tablename__ = "medias"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MyMedias] = mapped_column(Enum(MyMedias), nullable=False)
    url: Mapped[str] = mapped_column(String(120), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Posts"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "url": self.url,
            "post_id": self.post_id,
            "post": self.post.serialize()
        }
