"""
Smart Document Formatter
Intelligently detects document structure and creates formatted summaries
Handles resumes, reports, structured documents with proper formatting
"""

import re
from nltk.tokenize import sent_tokenize
from collections import Counter

class SmartDocumentFormatter:
    """
    Intelligently formats summaries based on document structure
    Preserves headings, bullets, sections, and hierarchy
    """
    
    def __init__(self):
        # Section indicators
        self.section_keywords = [
            'education', 'experience', 'skills', 'projects', 'work experience',
            'summary', 'objective', 'achievements', 'certifications', 'awards',
            'contact', 'profile', 'professional summary', 'technical skills',
            'languages', 'interests', 'hobbies', 'references', 'about'
        ]
        
        # Bullet indicators
        self.bullet_patterns = [
            r'^\s*[•●○◦▪▫■□-]\s+',  # Bullet symbols
            r'^\s*\d+[\.\)]\s+',     # Numbered lists
            r'^\s*[a-z][\.\)]\s+',   # Lettered lists
            r'^\s*>\s+',             # Blockquote style
        ]
    
    def detect_document_type(self, text):
        """Detect if document is resume, report, article, etc."""
        text_lower = text.lower()
        
        # Resume indicators
        resume_keywords = ['education', 'experience', 'skills', 'email', 'phone', 'linkedin', 'github']
        resume_score = sum(1 for kw in resume_keywords if kw in text_lower)
        
        # Report indicators
        report_keywords = ['introduction', 'methodology', 'results', 'conclusion', 'abstract']
        report_score = sum(1 for kw in report_keywords if kw in text_lower)
        
        # Article indicators
        article_keywords = ['author', 'published', 'journal', 'article', 'abstract']
        article_score = sum(1 for kw in article_keywords if kw in text_lower)
        
        scores = {
            'resume': resume_score,
            'report': report_score,
            'article': article_score,
            'general': 1  # Default
        }
        
        return max(scores, key=scores.get)
    
    def detect_structure(self, text):
        """
        Detect document structure: sections, headings, bullets, etc.
        Returns structured data about the document
        """
        lines = text.split('\n')
        structure = {
            'sections': [],
            'bullets': [],
            'headings': [],
            'paragraphs': [],
            'has_structure': False
        }
        
        current_section = None
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            # Check if line is a heading (short, possibly all caps, no punctuation)
            is_heading = self._is_heading(line_stripped)
            if is_heading:
                current_section = line_stripped
                structure['sections'].append({
                    'title': current_section,
                    'line': i,
                    'content': []
                })
                structure['headings'].append(line_stripped)
                structure['has_structure'] = True
                continue
            
            # Check if line is a bullet point
            is_bullet = self._is_bullet(line)
            if is_bullet:
                bullet_text = self._clean_bullet(line)
                structure['bullets'].append(bullet_text)
                if structure['sections']:
                    structure['sections'][-1]['content'].append({
                        'type': 'bullet',
                        'text': bullet_text
                    })
                structure['has_structure'] = True
                continue
            
            # Regular paragraph text
            if structure['sections']:
                structure['sections'][-1]['content'].append({
                    'type': 'paragraph',
                    'text': line_stripped
                })
            else:
                structure['paragraphs'].append(line_stripped)
        
        return structure
    
    def _is_heading(self, line):
        """Check if line is likely a heading"""
        # Criteria for heading:
        # - Short (< 50 chars)
        # - May be all caps
        # - No ending punctuation
        # - May contain section keywords
        
        if len(line) > 50:
            return False
        
        # Check if it's a section keyword
        if any(kw in line.lower() for kw in self.section_keywords):
            return True
        
        # Check if mostly uppercase
        if len([c for c in line if c.isupper()]) > len(line) * 0.5:
            return True
        
        # Check if ends without punctuation
        if line and line[-1] not in '.!?,;:':
            # Count words - headings typically have few words
            words = line.split()
            if 1 <= len(words) <= 5:
                return True
        
        return False
    
    def _is_bullet(self, line):
        """Check if line is a bullet point"""
        for pattern in self.bullet_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    def _clean_bullet(self, line):
        """Remove bullet symbols from line"""
        for pattern in self.bullet_patterns:
            line = re.sub(pattern, '', line)
        return line.strip()
    
    def create_formatted_summary(self, original_text, summary_sentences):
        """
        Create intelligently formatted summary
        Preserves document structure and adds appropriate formatting
        """
        doc_type = self.detect_document_type(original_text)
        structure = self.detect_structure(original_text)
        
        if not structure['has_structure']:
            # Simple paragraph format
            return self._format_simple_summary(summary_sentences)
        
        # Structured format
        if doc_type == 'resume':
            return self._format_resume_summary(structure, summary_sentences, original_text)
        elif structure['sections']:
            return self._format_sectioned_summary(structure, summary_sentences)
        elif structure['bullets']:
            return self._format_bulleted_summary(summary_sentences)
        else:
            return self._format_simple_summary(summary_sentences)
    
    def _format_simple_summary(self, sentences):
        """Simple paragraph format"""
        if isinstance(sentences, str):
            sentences = sent_tokenize(sentences)
        
        # Group into paragraphs (3-4 sentences each)
        paragraphs = []
        current = []
        
        for sent in sentences:
            current.append(sent)
            if len(current) >= 3:
                paragraphs.append(' '.join(current))
                current = []
        
        if current:
            paragraphs.append(' '.join(current))
        
        return '\n\n'.join(paragraphs)
    
    def _format_bulleted_summary(self, sentences):
        """Format as bullet points"""
        if isinstance(sentences, str):
            sentences = sent_tokenize(sentences)
        
        bullets = [f"• {sent.strip()}" for sent in sentences if sent.strip()]
        return '\n'.join(bullets)
    
    def _format_sectioned_summary(self, structure, sentences):
        """Format with sections and appropriate sub-formatting"""
        if isinstance(sentences, str):
            sentences = sent_tokenize(sentences)
        
        formatted = []
        sentences_per_section = max(1, len(sentences) // len(structure['sections']))
        
        for i, section in enumerate(structure['sections']):
            # Add section heading
            formatted.append(f"\n{section['title'].upper()}")
            formatted.append('-' * len(section['title']))
            
            # Add sentences for this section
            start_idx = i * sentences_per_section
            end_idx = start_idx + sentences_per_section
            section_sentences = sentences[start_idx:end_idx]
            
            # Check if section had bullets in original
            had_bullets = any(item['type'] == 'bullet' for item in section['content'])
            
            if had_bullets:
                # Format as bullets
                for sent in section_sentences:
                    formatted.append(f"  • {sent.strip()}")
            else:
                # Format as paragraph
                formatted.append(f"  {' '.join(section_sentences)}")
            
            formatted.append('')  # Empty line between sections
        
        return '\n'.join(formatted)
    
    def _format_resume_summary(self, structure, sentences, original_text):
        """Special formatting for resumes"""
        if isinstance(sentences, str):
            sentences = sent_tokenize(sentences)
        
        formatted = []
        
        # Extract key information
        contact_info = self._extract_contact_info(original_text)
        if contact_info:
            formatted.append("CONTACT INFORMATION")
            formatted.append("-" * 20)
            for key, value in contact_info.items():
                formatted.append(f"  • {key.title()}: {value}")
            formatted.append('')
        
        # Process sections
        for section in structure['sections']:
            section_title = section['title'].upper()
            formatted.append(f"\n{section_title}")
            formatted.append('-' * len(section_title))
            
            # Find relevant sentences for this section
            section_lower = section['title'].lower()
            relevant_sentences = [
                s for s in sentences 
                if any(word in s.lower() for word in section_lower.split())
            ]
            
            if not relevant_sentences:
                relevant_sentences = sentences[:2]  # Fallback
            
            # Format based on content type
            had_bullets = any(item['type'] == 'bullet' for item in section['content'])
            
            if had_bullets or 'experience' in section_lower or 'project' in section_lower:
                # Use bullet points
                for sent in relevant_sentences:
                    formatted.append(f"  • {sent.strip()}")
            else:
                # Use paragraph
                formatted.append(f"  {' '.join(relevant_sentences)}")
            
            formatted.append('')
        
        return '\n'.join(formatted)
    
    def _extract_contact_info(self, text):
        """Extract email, phone, GitHub, LinkedIn from text"""
        contact = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact['email'] = emails[0]
        
        # Phone
        phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact['phone'] = phones[0]
        
        # GitHub
        if 'github' in text.lower():
            github_match = re.search(r'github[:\s/]*([a-zA-Z0-9_-]+)', text, re.IGNORECASE)
            if github_match:
                contact['github'] = github_match.group(1)
        
        # LinkedIn
        if 'linkedin' in text.lower():
            linkedin_match = re.search(r'linkedin[:\s/]*([a-zA-Z0-9_-]+)', text, re.IGNORECASE)
            if linkedin_match:
                contact['linkedin'] = linkedin_match.group(1)
        
        return contact if contact else None
    
    def enhance_summary(self, original_text, raw_summary):
        """
        Main function to enhance summary with intelligent formatting
        """
        # Get sentences from raw summary
        sentences = sent_tokenize(raw_summary) if isinstance(raw_summary, str) else raw_summary
        
        # Create formatted summary
        formatted_summary = self.create_formatted_summary(original_text, sentences)
        
        return formatted_summary


# Singleton instance
formatter = SmartDocumentFormatter()

def format_smart_summary(original_text, summary):
    """
    Main entry point for smart formatting
    """
    return formatter.enhance_summary(original_text, summary)
