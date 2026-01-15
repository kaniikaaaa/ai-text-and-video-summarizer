/**
 * Input Validation and Sanitization Utilities
 * Provides security and data validation for text and video inputs
 */

// Text validation constants
const MAX_TEXT_LENGTH = 50000; // 50K characters
const MIN_TEXT_LENGTH = 50; // Minimum 50 characters
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

// Allowed file types
const ALLOWED_FILE_TYPES = {
  pdf: ['application/pdf'],
  txt: ['text/plain', 'text/html', 'application/txt']
};

/**
 * Sanitize text input to prevent XSS and malicious content
 */
export const sanitizeText = (text) => {
  if (!text) return '';
  
  // Convert to string
  let sanitized = String(text);
  
  // Remove null bytes
  sanitized = sanitized.replace(/\0/g, '');
  
  // Remove control characters (except newlines and tabs)
  sanitized = sanitized.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');
  
  // Normalize whitespace
  sanitized = sanitized.replace(/\s+/g, ' ');
  
  // Trim
  sanitized = sanitized.trim();
  
  return sanitized;
};

/**
 * Validate text input
 */
export const validateText = (text) => {
  const errors = [];
  
  if (!text || text.trim().length === 0) {
    errors.push('Text cannot be empty');
    return { isValid: false, errors };
  }
  
  const sanitized = sanitizeText(text);
  
  if (sanitized.length < MIN_TEXT_LENGTH) {
    errors.push(`Text must be at least ${MIN_TEXT_LENGTH} characters`);
  }
  
  if (sanitized.length > MAX_TEXT_LENGTH) {
    errors.push(`Text cannot exceed ${MAX_TEXT_LENGTH} characters (${sanitized.length} provided)`);
  }
  
  // Check for suspicious patterns
  const suspiciousPatterns = [
    /<script[\s\S]*?>[\s\S]*?<\/script>/gi,
    /<iframe[\s\S]*?>[\s\S]*?<\/iframe>/gi,
    /javascript:/gi,
    /on\w+\s*=/gi, // Event handlers like onclick=
  ];
  
  for (const pattern of suspiciousPatterns) {
    if (pattern.test(text)) {
      errors.push('Text contains potentially malicious content');
      break;
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    sanitized
  };
};

/**
 * Validate file upload
 */
export const validateFile = (file) => {
  const errors = [];
  
  if (!file) {
    errors.push('No file selected');
    return { isValid: false, errors };
  }
  
  // Check file size
  if (file.size > MAX_FILE_SIZE) {
    errors.push(`File size exceeds ${MAX_FILE_SIZE / (1024 * 1024)}MB limit (${(file.size / (1024 * 1024)).toFixed(2)}MB provided)`);
  }
  
  if (file.size === 0) {
    errors.push('File is empty');
  }
  
  // Check file type
  const fileName = file.name.toLowerCase();
  const fileExtension = fileName.split('.').pop();
  
  const isPDF = fileExtension === 'pdf' || ALLOWED_FILE_TYPES.pdf.includes(file.type);
  const isTXT = fileExtension === 'txt' || ALLOWED_FILE_TYPES.txt.includes(file.type);
  
  if (!isPDF && !isTXT) {
    errors.push('Invalid file type. Only PDF and TXT files are allowed');
  }
  
  // Check file name for suspicious patterns
  const suspiciousFilePatterns = [
    /\.\./, // Directory traversal
    /<|>/, // HTML tags
    /[<>:"\/\\|?*\x00-\x1f]/g, // Invalid filename characters
  ];
  
  for (const pattern of suspiciousFilePatterns) {
    if (pattern.test(fileName)) {
      errors.push('Invalid file name');
      break;
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    fileType: isPDF ? 'pdf' : 'txt',
    fileSize: file.size,
    fileName: file.name
  };
};

/**
 * Sanitize and validate YouTube URL
 */
export const validateYouTubeURL = (url) => {
  const errors = [];
  
  if (!url || url.trim().length === 0) {
    errors.push('URL cannot be empty');
    return { isValid: false, errors };
  }
  
  // Sanitize URL
  let sanitized = url.trim();
  
  // Remove whitespace
  sanitized = sanitized.replace(/\s/g, '');
  
  // Check URL length
  if (sanitized.length > 2048) {
    errors.push('URL is too long');
  }
  
  // Validate URL format
  let parsedURL;
  try {
    parsedURL = new URL(sanitized);
  } catch (e) {
    errors.push('Invalid URL format');
    return { isValid: false, errors, sanitized };
  }
  
  // Check protocol
  if (parsedURL.protocol !== 'http:' && parsedURL.protocol !== 'https:') {
    errors.push('Only HTTP/HTTPS URLs are allowed');
  }
  
  // Check if it's a YouTube URL
  const validYouTubeDomains = [
    'youtube.com',
    'www.youtube.com',
    'm.youtube.com',
    'youtu.be'
  ];
  
  const isYouTube = validYouTubeDomains.some(domain => 
    parsedURL.hostname === domain || parsedURL.hostname.endsWith('.' + domain)
  );
  
  if (!isYouTube) {
    errors.push('URL must be a valid YouTube link');
  }
  
  // Extract video ID
  let videoId = null;
  if (parsedURL.hostname.includes('youtu.be')) {
    videoId = parsedURL.pathname.substring(1).split('?')[0];
  } else if (parsedURL.hostname.includes('youtube.com')) {
    videoId = parsedURL.searchParams.get('v');
  }
  
  // Validate video ID format (YouTube IDs are 11 characters)
  if (videoId) {
    if (!/^[a-zA-Z0-9_-]{11}$/.test(videoId)) {
      errors.push('Invalid YouTube video ID format');
    }
  } else {
    errors.push('Could not extract video ID from URL');
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    sanitized,
    videoId
  };
};

/**
 * Validate summarization method
 */
export const validateSummarizationMethod = (method) => {
  const validMethods = ['textrank', 'transformer'];
  
  if (!validMethods.includes(method)) {
    return {
      isValid: false,
      errors: ['Invalid summarization method']
    };
  }
  
  return {
    isValid: true,
    errors: []
  };
};

/**
 * Validate max sentences parameter
 */
export const validateMaxSentences = (maxSentences) => {
  const errors = [];
  
  if (maxSentences === 'auto') {
    return { isValid: true, errors: [] };
  }
  
  const num = parseInt(maxSentences, 10);
  
  if (isNaN(num)) {
    errors.push('Max sentences must be a number or "auto"');
  } else if (num < 1 || num > 20) {
    errors.push('Max sentences must be between 1 and 20');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

/**
 * Display validation errors to user
 */
export const displayErrors = (errors) => {
  if (errors.length === 0) return;
  
  const errorMessage = errors.join('\n• ');
  alert('⚠️ Validation Error:\n\n• ' + errorMessage);
};

// Export constants for use in components
export const VALIDATION_CONSTANTS = {
  MAX_TEXT_LENGTH,
  MIN_TEXT_LENGTH,
  MAX_FILE_SIZE,
  ALLOWED_FILE_TYPES
};
