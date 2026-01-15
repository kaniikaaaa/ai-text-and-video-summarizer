"""
Resume Preprocessor
Cleans and structures resume text BEFORE summarization
Handles contact info, sections, and formatting
"""

import re

class ResumePreprocessor:
    """
    Preprocesses resume text to improve summarization quality
    Separates contact info, structures sections properly
    """
    
    def __init__(self):
        # Contact patterns
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        
        # Section keywords
        self.section_keywords = [
            'education', 'experience', 'skills', 'projects', 'work experience',
            'professional experience', 'technical skills', 'achievements',
            'certifications', 'awards', 'summary', 'objective', 'profile'
        ]
    
    def is_resume(self, text):
        """Check if text is likely a resume"""
        text_lower = text.lower()
        indicators = 0
        
        # Check for common resume elements
        if re.search(self.email_pattern, text):
            indicators += 2
        if re.search(self.phone_pattern, text):
            indicators += 2
        if any(kw in text_lower for kw in ['linkedin', 'github']):
            indicators += 1
        if sum(1 for kw in self.section_keywords if kw in text_lower) >= 2:
            indicators += 2
        
        return indicators >= 3
    
    def extract_contact_info(self, text):
        """Extract and separate contact information"""
        contact_info = {
            'name': None,
            'email': None,
            'phone': None,
            'github': None,
            'linkedin': None,
            'location': None
        }
        
        lines = text.split('\n')
        
        # First non-empty line is usually the name
        for line in lines[:5]:
            if line.strip() and len(line.strip().split()) <= 4:
                # Likely a name (short, at the top)
                if not any(char.isdigit() for char in line) and '@' not in line:
                    contact_info['name'] = line.strip()
                    break
        
        # Extract email
        email_matches = re.findall(self.email_pattern, text)
        if email_matches:
            contact_info['email'] = email_matches[0]
        
        # Extract phone
        phone_matches = re.findall(self.phone_pattern, text)
        if phone_matches:
            contact_info['phone'] = phone_matches[0]
        
        # Extract GitHub
        github_patterns = [
            r'github\.com/([a-zA-Z0-9_-]+)',
            r'github[:\s]*([a-zA-Z0-9_-]+)',
            r'@([a-zA-Z0-9_-]+)\s*github'
        ]
        for pattern in github_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contact_info['github'] = match.group(1)
                break
        
        # Extract LinkedIn
        linkedin_patterns = [
            r'linkedin\.com/in/([a-zA-Z0-9_-]+)',
            r'linkedin[:\s]*([a-zA-Z0-9_-]+)',
            r'@([a-zA-Z0-9_-]+)\s*linkedin'
        ]
        for pattern in linkedin_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contact_info['linkedin'] = match.group(1)
                break
        
        return contact_info
    
    def clean_contact_line(self, text):
        """Clean messy contact info line"""
        # Fix common issues in contact lines
        
        # Add space after email
        text = re.sub(r'(\.com|\.in|\.org)([A-Z])', r'\1. \2', text)
        
        # Fix "phone" word
        text = re.sub(r'phone\s*\(', r'Phone: (', text, flags=re.IGNORECASE)
        
        # Fix "github" word
        text = re.sub(r'github\s*([a-z])', r'GitHub: \1', text, flags=re.IGNORECASE)
        
        # Fix "linkedin" word
        text = re.sub(r'linkedin\s*([a-z])', r'LinkedIn: \1', text, flags=re.IGNORECASE)
        
        # Add commas between contact items
        # Pattern: email followed by word
        text = re.sub(r'(\.com|\.in|\.org)\s+([a-zA-Z])', r'\1, \2', text)
        
        # Pattern: phone followed by word
        text = re.sub(r'(\d{4})\s+([a-zA-Z])', r'\1, \2', text)
        
        return text
    
    def structure_sections(self, text):
        """Add proper structure to resume sections"""
        lines = text.split('\n')
        structured_lines = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if line is a section heading
            is_section = any(kw == line_lower or kw in line_lower for kw in self.section_keywords)
            
            if is_section:
                # Add extra spacing before section
                if structured_lines:
                    structured_lines.append('')
                structured_lines.append(f"\n{line.upper()}")
                structured_lines.append('')
            else:
                structured_lines.append(line)
        
        return '\n'.join(structured_lines)
    
    def preprocess(self, text):
        """Main preprocessing function"""
        if not self.is_resume(text):
            return text  # Not a resume, return as-is
        
        # Extract contact info
        contact_info = self.extract_contact_info(text)
        
        # Clean contact lines
        lines = text.split('\n')
        cleaned_lines = []
        
        contact_section_added = False
        
        for i, line in enumerate(lines):
            # Check if this line has contact info
            has_email = '@' in line
            has_phone = any(char.isdigit() for char in line) and ('phone' in line.lower() or '(' in line)
            has_social = 'github' in line.lower() or 'linkedin' in line.lower()
            
            if i < 10 and (has_email or has_phone or has_social):
                # This is likely a contact info line
                if not contact_section_added:
                    # Add structured contact section
                    if contact_info['name']:
                        cleaned_lines.append(f"{contact_info['name']}")
                        cleaned_lines.append('')
                    
                    cleaned_lines.append("CONTACT INFORMATION:")
                    
                    if contact_info['email']:
                        cleaned_lines.append(f"  Email: {contact_info['email']}")
                    if contact_info['phone']:
                        cleaned_lines.append(f"  Phone: {contact_info['phone']}")
                    if contact_info['github']:
                        cleaned_lines.append(f"  GitHub: {contact_info['github']}")
                    if contact_info['linkedin']:
                        cleaned_lines.append(f"  LinkedIn: {contact_info['linkedin']}")
                    
                    cleaned_lines.append('')
                    contact_section_added = True
                # Skip original messy contact line
                continue
            else:
                # Regular content line
                cleaned_lines.append(line)
        
        # Join lines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Structure sections
        cleaned_text = self.structure_sections(cleaned_text)
        
        return cleaned_text


# Singleton instance
preprocessor = ResumePreprocessor()

def preprocess_resume(text):
    """
    Main entry point for resume preprocessing
    Call this BEFORE summarization
    """
    return preprocessor.preprocess(text)
