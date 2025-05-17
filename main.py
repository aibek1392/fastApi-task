from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage
applications = []

# Pydantic models
class Application(BaseModel):
    candidate_id: str
    name: str
    email: str
    job_id: str

class ApplicationUpdate(BaseModel):
    email: Optional[str] = None
    job_id: Optional[str] = None

# 1. POST /applications
@app.post("/applications")
def create_application(app_data: Application):
    applications.append(app_data)
    return {
        "status": "success",
        "message": f"Application submitted for {app_data.name}"
    }

# 2. GET /applications
@app.get("/applications")
def list_applications(company_name: Optional[str] = None, candidate_email: Optional[str] = None):
    if company_name:
        return {"message": f"Here is your application for {company_name}"}
    elif candidate_email:
        return {"message": f"Here is your application for {candidate_email}"}
    else:
        return {"message": "Here are all of your applications", "applications": applications}

# 3. GET /applications/{candidate_id}
@app.get("/applications/{candidate_id}")
def get_application(candidate_id: str):
    for app_item in applications:
        if app_item.candidate_id == candidate_id:
            return {"message": f"Application found for candidate ID: {candidate_id}"}
    raise HTTPException(status_code=404, detail="Application not found")

# 4. PUT /applications/{candidate_id}
@app.put("/applications/{candidate_id}")
def update_application(candidate_id: str, data: ApplicationUpdate):
    for app_item in applications:
        if app_item.candidate_id == candidate_id:
            if data.email:
                app_item.email = data.email
            if data.job_id:
                app_item.job_id = data.job_id
            return {"message": f"Application for {candidate_id} successfully updated"}
    raise HTTPException(status_code=404, detail="Application not found")

# 5. PATCH /applications/{candidate_id}
@app.patch("/applications/{candidate_id}")
def patch_application(candidate_id: str, patch: ApplicationUpdate):
    for app_item in applications:
        if app_item.candidate_id == candidate_id:
            updates = []
            if patch.email:
                app_item.email = patch.email
                updates.append(f"email updated to {patch.email}")
            if patch.job_id:
                app_item.job_id = patch.job_id
                updates.append(f"job_id updated to {patch.job_id}")
            if updates:
                return {"message": f"Application for {candidate_id} successfully updated: " + ", ".join(updates)}
            return {"message": "No fields updated"}
    raise HTTPException(status_code=404, detail="Application not found")

# 6. DELETE /applications/{candidate_id}
@app.delete("/applications/{candidate_id}")
def delete_application(candidate_id: str):
    for index, app_item in enumerate(applications):
        if app_item.candidate_id == candidate_id:
            applications.pop(index)
            return {
                "status": "success",
                "message": f"Application for {candidate_id} has been deleted"
            }
    raise HTTPException(status_code=404, detail="Application not found")