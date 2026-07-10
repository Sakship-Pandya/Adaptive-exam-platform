import re
from pathlib import Path
from uuid import uuid4


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing unsafe characters.

    Strips non-alphanumeric characters (except ``._-``) from the file
    stem and normalises the extension to lowercase.  Consecutive
    underscores are collapsed into one.

    Args:
        filename: The original filename including its extension.

    Returns:
        A filesystem-safe version of the filename.

    Example::

        >>> sanitize_filename("Machine Learning (Final).pdf")
        'Machine_Learning_Final.pdf'
    """
    path = Path(filename)

    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", path.stem)
    stem = re.sub(r"_+", "_", stem).strip("_")

    return f"{stem}{path.suffix.lower()}"


def get_file_extension(filename: str) -> str:
    """Extract the file extension in lowercase without the leading dot.

    Args:
        filename: The filename to extract the extension from.

    Returns:
        The lowercase extension string (e.g. ``"pdf"``).
        Returns an empty string if no extension is present.

    Example::

        >>> get_file_extension("notes.PDF")
        'pdf'
    """
    return Path(filename).suffix.lower().lstrip(".")


def generate_object_name(filename: str) -> str:
    """Generate a UUID-based object name preserving the original extension.

    Replaces the filename stem with a random UUID4 hex string to
    guarantee uniqueness in the storage bucket.

    Args:
        filename: The original filename whose extension will be kept.

    Returns:
        A unique object name in the form ``<uuid4_hex>.<ext>``.

    Example::

        >>> generate_object_name("notes.pdf")  # doctest: +SKIP
        '8e89d4d0fdad4db6a7fa2d93b95bcb9f.pdf'
    """
    extension = Path(filename).suffix.lower()

    return f"{uuid4().hex}{extension}"


def generate_storage_key(
    workspace_id,
    upload_session_id,
    file_role: str,
    filename: str,
) -> str:
    role = file_role.strip().lower().replace("_", "-")

    object_name = generate_object_name(filename)

    return (
        f"workspaces/"
        f"{workspace_id}/"
        f"uploads/"
        f"{upload_session_id}/"
        f"{role}/"
        f"{object_name}"
    )