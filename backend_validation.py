"""
Backend Input Validation and Sanitization
Security layer for text and video summarization endpoints
"""

import re
from urllib.parse import urlparse, parse_qs

# Validation constants
MAX_TEXT_LENGTH = 50000  # 50K characters
MIN_TEXT_LENGTH = 50
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_EXTENSIONS = ['pdf', 'txt']


def sanitize_text(text):
    """Remove potentially malicious content from text"""
    if not text:
        return ''
    
    # Convert to string
    text = str(text)
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove control characters (except newlines and tabs)
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Trim
    text = text.strip()
    
    return text


def validate_text(text):
    """Validate text input for summarization"""
    errors = []
    
    if not text or not text.strip():
        errors.append('Text cannot be empty')
        return False, errors, None
    
    # Sanitize text
    sanitized = sanitize_text(text)
    
    # Check length
    if len(sanitized) < MIN_TEXT_LENGTH:
        errors.append(f'Text must be at least {MIN_TEXT_LENGTH} characters')
    
    if len(sanitized) > MAX_TEXT_LENGTH:
        errors.append(f'Text cannot exceed {MAX_TEXT_LENGTH} characters')
    
    # Check for suspicious patterns
    suspicious_patterns = [
        r'<script[\s\S]*?>[\s\S]*?</script>',
        r'<iframe[\s\S]*?>[\s\S]*?</iframe>',
        r'javascript:',
        r'on\w+\s*=',  # Event handlers
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            errors.append('Text contains potentially malicious content')
            break
    
    return len(errors) == 0, errors, sanitized


def validate_file(file, filename):
    """Validate uploaded file"""
    errors = []
    
    if not file or not filename:
        errors.append('No file provided')
        return False, errors
    
    # Check file extension
    file_ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        errors.append(f'Invalid file type. Only {", ".join(ALLOWED_FILE_EXTENSIONS)} files allowed')
    
    # Check filename for suspicious patterns
    if re.search(r'[<>:"/\\|?*\x00-\x1f]', filename):
        errors.append('Invalid filename characters')
    
    if '..' in filename:
        errors.append('Invalid filename (directory traversal detected)')
    
    return len(errors) == 0, errors


def validate_youtube_url(url):
    """Validate and sanitize YouTube URL"""
    errors = []
    
    if not url or not url.strip():
        errors.append('URL cannot be empty')
        return False, errors, None, None
    
    # Sanitize URL
    sanitized = url.strip().replace(' ', '')
    
    # Check URL length
    if len(sanitized) > 2048:
        errors.append('URL is too long')
        return False, errors, None, None
    
    # Parse URL
    try:
        parsed = urlparse(sanitized)
    except Exception as e:
        errors.append(f'Invalid URL format: {str(e)}')
        return False, errors, None, None
    
    # Check protocol
    if parsed.scheme not in ['http', 'https']:
        errors.append('Only HTTP/HTTPS URLs are allowed')
    
    # Check if it's a YouTube URL
    valid_domains = ['youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be']
    
    if not any(parsed.hostname == domain or (parsed.hostname and parsed.hostname.endswith('.' + domain)) 
               for domain in valid_domains):
        errors.append('URL must be a valid YouTube link')
        return False, errors, None, None
    
    # Extract video ID
    video_id = None
    
    if 'youtu.be' in parsed.hostname:
        # Format: https://youtu.be/VIDEO_ID
        video_id = parsed.path.lstrip('/').split('?')[0].split('/')[0]
    elif 'youtube.com' in parsed.hostname:
        # Format: https://youtube.com/watch?v=VIDEO_ID
        query_params = parse_qs(parsed.query)
        video_id = query_params.get('v', [None])[0]
    
    # Validate video ID format (YouTube video IDs are 11 characters)
    if video_id:
        if not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
            errors.append('Invalid YouTube video ID format')
            video_id = None
    else:
        errors.append('Could not extract video ID from URL')
    
    return len(errors) == 0, errors, sanitized, video_id


def validate_summarization_method(method):
    """Validate summarization method parameter"""
    valid_methods = ['textrank', 'transformer']
    
    if method not in valid_methods:
        return False, [f'Invalid method. Must be one of: {", ".join(valid_methods)}']
    
    return True, []


def validate_max_sentences(max_sentences):
    """Validate max_sentences parameter"""
    if max_sentences == 'auto':
        return True, [], 'auto'
    
    # Try to convert to integer
    try:
        num = int(max_sentences)
        
        if num < 1 or num > 20:
            return False, ['max_sentences must be between 1 and 20'], None
        
        return True, [], num
    
    except (ValueError, TypeError):
        return False, ['max_sentences must be a number or "auto"'], None


def validate_request_body(data):
    """Validate JSON request body"""
    if not data:
        return False, ['Empty request body']
    
    if not isinstance(data, dict):
        return False, ['Invalid request format']
    
    return True, []


# Rate limiting helper (simple implementation)
request_counts = {}

def check_rate_limit(ip_address, limit=100, window=60):
    """
    Simple rate limiting check
    limit: max requests per window
    window: time window in seconds
    """
    import time
    
    current_time = time.time()
    
    # Clean old entries
    request_counts[ip_address] = [
        timestamp for timestamp in request_counts.get(ip_address, [])
        if current_time - timestamp < window
    ]
    
    # Check if limit exceeded
    if len(request_counts.get(ip_address, [])) >= limit:
        return False, f'Rate limit exceeded. Max {limit} requests per {window} seconds'
    
    # Add current request
    if ip_address not in request_counts:
        request_counts[ip_address] = []
    request_counts[ip_address].append(current_time)
    
    return True, None
