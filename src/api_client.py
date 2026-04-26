"""Udemy Instructor API istemcisi."""

import os
from typing import Optional

import httpx


class UdemyAPIClient:
    """Udemy Instructor API wrapper — Bearer token ile erisim."""

    BASE_URL = "https://www.udemy.com/instructor-api/v1"

    def __init__(self):
        self.token = os.getenv("UDEMY_BEARER_TOKEN", "")
        self.headers = {
            "Authorization": f"bearer {self.token}",
            "Accept": "application/json",
        }

    async def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """API'ye GET istegi gonder."""
        if not self.token or self.token == "your_token_here":
            return {"hata": "UDEMY_BEARER_TOKEN ayarlanmamis. config/.env dosyasini kontrol edin."}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{self.BASE_URL}/{endpoint}",
                headers=self.headers,
                params=params or {},
            )
            if resp.status_code == 200:
                return resp.json()
            return {"hata": f"API hatasi: {resp.status_code}", "detay": resp.text[:500]}

    async def get_courses(self) -> dict:
        """Kendi kurslarimi listele."""
        return await self._get("taught-courses/courses/", {
            "fields[course]": "title,headline,num_subscribers,rating,num_reviews,url,status"
        })

    async def get_reviews(self, course_id: str) -> dict:
        """Kurs yorumlarini cek."""
        return await self._get(f"taught-courses/courses/{course_id}/reviews/")

    async def get_questions(self, course_id: str) -> dict:
        """Kurs Q&A sorularini cek."""
        return await self._get(f"taught-courses/courses/{course_id}/questions/")

    async def get_course_detail(self, course_id: str) -> dict:
        """Tek kursun detaylarini cek."""
        return await self._get(f"taught-courses/courses/{course_id}/", {
            "fields[course]": "title,headline,description,num_subscribers,rating,"
                              "num_reviews,num_lectures,content_length_video,"
                              "avg_rating,url,status,created,last_update_date"
        })
