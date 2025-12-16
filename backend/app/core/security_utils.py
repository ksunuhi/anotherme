"""
Security utilities for input sanitization and validation
"""
import bleach


def sanitize_input(text: str, strip_all_tags: bool = True) -> str:
    """
    Sanitize user input to prevent XSS attacks

    Args:
        text: The input text to sanitize
        strip_all_tags: If True, removes all HTML tags. If False, allows safe tags.

    Returns:
        Sanitized text safe for storage and display
    """
    if not text:
        return text

    if strip_all_tags:
        # Remove all HTML tags - use for posts, comments, messages, bio
        # This converts <script>alert('xss')</script> to plain text
        cleaned = bleach.clean(
            text,
            tags=[],  # No tags allowed
            attributes={},  # No attributes allowed
            strip=True  # Remove tags completely
        )
    else:
        # Allow only safe HTML tags - currently not used, but available if needed
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'br', 'p']
        allowed_attrs = {}

        cleaned = bleach.clean(
            text,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )

    # Also strip any leading/trailing whitespace
    return cleaned.strip()


def sanitize_post_content(content: str) -> str:
    """Sanitize post content - plain text only"""
    return sanitize_input(content, strip_all_tags=True)


def sanitize_comment_content(content: str) -> str:
    """Sanitize comment content - plain text only"""
    return sanitize_input(content, strip_all_tags=True)


def sanitize_message_content(content: str) -> str:
    """Sanitize message content - plain text only"""
    return sanitize_input(content, strip_all_tags=True)


def sanitize_bio(bio: str) -> str:
    """Sanitize user bio - plain text only"""
    return sanitize_input(bio, strip_all_tags=True)


def sanitize_name(name: str) -> str:
    """Sanitize user name - plain text only, extra strict"""
    # Remove all HTML and special characters that could be used for attacks
    cleaned = bleach.clean(name, tags=[], attributes={}, strip=True)
    return cleaned.strip()
