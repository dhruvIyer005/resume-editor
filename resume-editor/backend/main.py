from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import json
import os
from datetime import datetime
import random

app = FastAPI(title="Resume Editor API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo purposes
resume_storage: Dict[str, Any] = {}

class AIEnhanceRequest(BaseModel):
    section: str
    content: str

class AIEnhanceResponse(BaseModel):
    success: bool
    enhanced_content: str

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str
    location: str

class Experience(BaseModel):
    id: str
    company: str
    position: str
    duration: str
    description: str

class Education(BaseModel):
    id: str
    institution: str
    degree: str
    year: str
    description: str

class ResumeData(BaseModel):
    personalInfo: PersonalInfo
    summary: str
    experience: List[Experience]
    education: List[Education]
    skills: List[str]

class SaveResumeResponse(BaseModel):
    success: bool
    message: str
    resume_id: str

def mock_enhance_content(section: str, content: str) -> str:
    """Mock AI enhancement function"""
    
    enhancements = {
        "summary": [
            "Results-driven professional with proven expertise in",
            "Accomplished specialist with extensive experience in",
            "Dynamic leader with a track record of success in",
            "Innovative problem-solver with deep knowledge of"
        ],
        "experience": [
            "Successfully led cross-functional teams to deliver high-impact projects, resulting in significant improvements to system performance and user experience.",
            "Spearheaded the development and implementation of scalable solutions, driving operational efficiency and reducing costs by implementing best practices.",
            "Collaborated with stakeholders to identify opportunities for process optimization, leading to measurable improvements in productivity and quality.",
            "Mentored junior developers and established coding standards that improved code quality and reduced technical debt across multiple projects."
        ]
    }
    
    if section == "summary":
        random_enhancement = random.choice(enhancements["summary"])
        return f"{random_enhancement} {content.lower()}. Demonstrated ability to drive innovation and deliver exceptional results in fast-paced environments."
    elif section == "experience":
        random_enhancement = random.choice(enhancements["experience"])
        return f"{content} {random_enhancement}"
    else:
        return f"Enhanced: {content}"

@app.get("/")
async def root():
    return {"message": "Resume Editor API is running!"}

@app.post("/ai-enhance", response_model=AIEnhanceResponse)
async def ai_enhance(request: AIEnhanceRequest):
    """
    Enhance resume content using mock AI
    """
    try:
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")
        
        enhanced_content = mock_enhance_content(request.section, request.content)
        
        return AIEnhanceResponse(
            success=True,
            enhanced_content=enhanced_content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")

@app.post("/save-resume", response_model=SaveResumeResponse)
async def save_resume(resume_data: ResumeData):
    """
    Save resume data to memory/disk
    """
    try:
        resume_id = str(int(datetime.now().timestamp() * 1000))
        
        # Add metadata
        resume_with_metadata = {
            "id": resume_id,
            "data": resume_data.dict(),
            "saved_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        # Store in memory
        resume_storage[resume_id] = resume_with_metadata
        
        # Optionally save to file
        os.makedirs("saved_resumes", exist_ok=True)
        file_path = f"saved_resumes/resume_{resume_id}.json"
        
        with open(file_path, "w") as f:
            json.dump(resume_with_metadata, f, indent=2)
        
        print(f"Resume saved with ID: {resume_id}")
        
        return SaveResumeResponse(
            success=True,
            message="Resume saved successfully",
            resume_id=resume_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Save failed: {str(e)}")

@app.get("/resume/{resume_id}")
async def get_resume(resume_id: str):
    """
    Retrieve a saved resume by ID
    """
    if resume_id not in resume_storage:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return {
        "success": True,
        "resume": resume_storage[resume_id]
    }

@app.get("/resumes")
async def list_resumes():
    """
    List all saved resumes
    """
    return {
        "success": True,
        "resumes": list(resume_storage.keys()),
        "count": len(resume_storage)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
