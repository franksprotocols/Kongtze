"""AI service for test generation and explanations using Google Gemini"""

import hashlib
import json
from typing import List, Dict, Optional
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.cached_explanation import CachedExplanation


class AIService:
    """Service for AI-powered features using Google Gemini"""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        # Use gemini-2.5-flash which is available and supports generateContent
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    
    async def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API directly using REST"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.api_url}?key={self.api_key}",
                    json={
                        "contents": [{
                            "parts": [{"text": prompt}]
                        }]
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text if hasattr(e.response, 'text') else str(e)
            print(f"Gemini API HTTP error: {e.response.status_code} - {error_detail}")
            raise Exception(f"Gemini API returned {e.response.status_code}: {error_detail}")
        except httpx.TimeoutException as e:
            print(f"Gemini API timeout: {str(e)}")
            raise Exception(f"Gemini API request timed out after 30 seconds")
        except KeyError as e:
            print(f"Gemini API response parsing error: {str(e)}")
            raise Exception(f"Unexpected response format from Gemini API: missing {str(e)}")
        except Exception as e:
            print(f"Gemini API unexpected error: {type(e).__name__} - {str(e)}")
            raise Exception(f"Gemini API call failed: {type(e).__name__} - {str(e)}")

    async def generate_test_questions(
        self,
        subject: str,
        difficulty_level: int,
        num_questions: int,
        topics: Optional[List[str]] = None,
        context_text: Optional[str] = None,
    ) -> List[Dict]:
        """
        Generate test questions using Gemini AI.

        Args:
            subject: Subject name (Math, English, Chinese, Science)
            difficulty_level: 1=Beginner, 2=Intermediate, 3=Advanced, 4=Expert
            num_questions: Number of questions to generate
            topics: Optional list of specific topics to focus on

        Returns:
            List of question dictionaries with question_text, options, correct_answer
        """
        difficulty_names = {
            1: "Beginner (Primary 1-2 level)",
            2: "Intermediate (Primary 3-4 level)",
            3: "Advanced (Primary 5-6 level)",
            4: "Expert (PSLE preparation level)",
        }

        topics_context = ""
        if topics:
            topics_context = f"\nFocus on these specific topics: {', '.join(topics)}"

        prompt = f"""Generate {num_questions} multiple-choice questions for {subject} at {difficulty_names[difficulty_level]}.{topics_context}

Requirements:
1. Each question should have 4 options (A, B, C, D)
2. Questions should be age-appropriate and educational
3. Include a mix of conceptual understanding and problem-solving
4. For Math: Include word problems and calculations
5. For English: Include grammar, vocabulary, and comprehension
6. For Chinese: Include characters, vocabulary, and grammar
7. For Science: Include concepts from primary science curriculum

Format your response as a JSON array with this exact structure:
[
  {{
    "question_text": "Question here?",
    "options": {{
      "A": "Option A text",
      "B": "Option B text",
      "C": "Option C text",
      "D": "Option D text"
    }},
    "correct_answer": "A",
    "time_limit_seconds": 60
  }}
]

Important: Return ONLY the JSON array, no additional text or markdown formatting."""

        try:
            response_text = await self._call_gemini_api(prompt)

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            questions = json.loads(response_text.strip())
            return questions

        except Exception as e:
            # Fallback to sample questions if AI fails
            return self._get_fallback_questions(subject, num_questions)

    def _get_fallback_questions(self, subject: str, num_questions: int) -> List[Dict]:
        """Fallback questions if AI generation fails"""
        fallback = {
            "Math": {
                "question_text": "What is 5 + 3?",
                "options": {"A": "6", "B": "7", "C": "8", "D": "9"},
                "correct_answer": "C",
                "time_limit_seconds": 30,
            },
            "English": {
                "question_text": "Choose the correct spelling:",
                "options": {"A": "recieve", "B": "receive", "C": "recive", "D": "receeve"},
                "correct_answer": "B",
                "time_limit_seconds": 30,
            },
            "Chinese": {
                "question_text": "What is the meaning of '学习'?",
                "options": {"A": "to eat", "B": "to study", "C": "to play", "D": "to sleep"},
                "correct_answer": "B",
                "time_limit_seconds": 30,
            },
            "Science": {
                "question_text": "What do plants need to make food?",
                "options": {
                    "A": "Water only",
                    "B": "Sunlight only",
                    "C": "Water, sunlight, and carbon dioxide",
                    "D": "Soil only",
                },
                "correct_answer": "C",
                "time_limit_seconds": 45,
            },
        }

        return [fallback.get(subject, fallback["Math"])] * min(num_questions, 5)

    async def get_explanation(
        self,
        question_text: str,
        correct_answer: str,
        user_answer: str,
        db: AsyncSession,
    ) -> str:
        """
        Get AI explanation for a question, with caching.

        Args:
            question_text: The question text
            correct_answer: The correct answer
            user_answer: The user's answer
            db: Database session for caching

        Returns:
            AI-generated explanation
        """
        # Generate hash for caching
        cache_key = hashlib.sha256(
            f"{question_text}:{correct_answer}".encode()
        ).hexdigest()

        # Check cache
        result = await db.execute(
            select(CachedExplanation).where(
                CachedExplanation.question_hash == cache_key
            )
        )
        cached = result.scalar_one_or_none()

        if cached:
            # Update hit count and last accessed
            cached.hit_count += 1
            await db.flush()
            return cached.ai_explanation

        # Generate new explanation
        is_correct = user_answer == correct_answer

        prompt = f"""Explain this question to a primary school student:

Question: {question_text}
Correct Answer: {correct_answer}
Student's Answer: {user_answer}
Result: {"Correct! ✓" if is_correct else "Incorrect ✗"}

Provide:
1. A brief explanation of why the correct answer is right
2. If the student was wrong, explain why their answer was incorrect
3. A helpful tip to remember this concept

Keep the explanation simple, encouraging, and educational (2-3 sentences)."""

        try:
            response = self.model.generate_content(prompt)
            explanation = response.text.strip()

            # Cache the explanation
            new_cache = CachedExplanation(
                question_hash=cache_key,
                ai_explanation=explanation,
                hit_count=1,
            )
            db.add(new_cache)
            await db.flush()

            return explanation

        except Exception:
            return (
                f"The correct answer is {correct_answer}. "
                "Keep practicing to improve your understanding!"
            )

    async def generate_text(self, prompt: str) -> str:
        """
        Generate text using Gemini AI for general purposes.
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            Generated text response
        """
        try:
            return await self._call_gemini_api(prompt)
        except Exception as e:
            # Re-raise with the original error message
            error_msg = str(e) if str(e) else f"{type(e).__name__} occurred"
            print(f"generate_text error: {error_msg}")
            raise Exception(f"AI generation failed: {error_msg}")

    async def extract_topics_from_notes(
        self,
        ocr_text: str,
        subject: str,
    ) -> List[Dict[str, any]]:
        """
        Extract curriculum topics from class notes using AI.

        Args:
            ocr_text: Text extracted from class notes via OCR
            subject: Subject name

        Returns:
            List of topic dictionaries with name and confidence score
        """
        prompt = f"""Analyze this text from {subject} class notes and extract the main curriculum topics:

{ocr_text}

Identify up to 5 key topics covered in these notes. For each topic, provide:
1. A concise topic name (2-4 words)
2. A confidence score (0.0 to 1.0) indicating how clearly this topic is covered

Format your response as a JSON array:
[
  {{"topic": "Topic Name", "confidence": 0.95}},
  {{"topic": "Another Topic", "confidence": 0.80}}
]

Return ONLY the JSON array, no additional text."""

        try:
            response_text = await self._call_gemini_api(prompt)

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            topics = json.loads(response_text.strip())
            return topics

        except Exception:
            # Return empty list if extraction fails
            return []


# Singleton instance
ai_service = AIService()
