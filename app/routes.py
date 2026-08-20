import secrets
import string
from urllib.parse import urlparse

from flask import Blueprint, request, redirect

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import db
from app.models import URL


url_bp = Blueprint("url", __name__, url_prefix="/api")
redirect_bp = Blueprint("redirect", __name__)


def is_valid_url(url):
    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    while True:
        code = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        existing_url = URL.query.filter_by(
            short_code=code
        ).first()

        if not existing_url:
            return code


@url_bp.route("/shorten", methods=["POST"])
def shorten_url():

    if not request.is_json:
        return {
            "error": "Content-Type must be application/json"
        }, 415

    data = request.get_json(silent=True)

    if not data:
        return {
            "error": "Request body cannot be empty"
        }, 400

    original_url = data.get("url")

    if not original_url:
        return {
            "error": "URL is required"
        }, 400

    if not isinstance(original_url, str):
        return {
            "error": "URL must be a string"
        }, 400

    original_url = original_url.strip()

    if len(original_url) > 2048:
        return {
            "error": "URL cannot exceed 2048 characters"
        }, 400

    if not is_valid_url(original_url):
        return {
            "error": "Invalid URL. URL must start with http:// or https://"
        }, 400

    existing_url = URL.query.filter_by(
        original_url=original_url
    ).first()

    if existing_url:
        return {
            "message": "URL already shortened",
            "original_url": existing_url.original_url,
            "short_code": existing_url.short_code,
            "short_url": f"http://localhost:5000/{existing_url.short_code}",
            "clicks": existing_url.clicks
        }, 200

    short_code = generate_short_code()

    new_url = URL(
        original_url=original_url,
        short_code=short_code
    )

    try:
        db.session.add(new_url)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

        return {
            "error": "Could not generate a unique short code. Please try again."
        }, 500

    except SQLAlchemyError:
        db.session.rollback()

        return {
            "error": "Database error occurred"
        }, 500

    return {
        "message": "URL shortened successfully",
        "original_url": original_url,
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }, 201


@url_bp.route("/urls/<short_code>", methods=["GET"])
def get_url_stats(short_code):

    url = URL.query.filter_by(
        short_code=short_code
    ).first()

    if not url:
        return {
            "error": "Short URL not found"
        }, 404

    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "short_url": f"http://localhost:5000/{url.short_code}",
        "clicks": url.clicks,
        "created_at": url.created_at.isoformat()
    }, 200


@redirect_bp.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):

    url = URL.query.filter_by(
        short_code=short_code
    ).first()

    if not url:
        return {
            "error": "Short URL not found"
        }, 404

    url.clicks += 1

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        return {
            "error": "Database error occurred"
        }, 500

    return redirect(url.original_url)
