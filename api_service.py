
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from vector_store import FunctionFinder
from code_generator import ScriptMaker
from automation_functions import AutomationTools
from typing import Dict, List
import os
import time
import logging
import subprocess
import psutil

logging.basicConfig(filename="D:\\codde\\automation.log", level=logging.INFO, format="%(asctime)s - %(message)s")
app = FastAPI(title="Automation API")
function_finder = FunctionFinder(storage_path="D:\\codde\\vector_store")
script_maker = ScriptMaker()
recent_commands: List[Dict] = []

class UserPrompt(BaseModel):
    prompt: str

    @field_validator("prompt")
    def prompt_not_empty(cls, value):
        """Ensures the prompt isn’t just whitespace."""
        if not value.strip():
            raise ValueError("Prompt cannot be empty")
        return value

class TaskResponse(BaseModel):
    function: str
    code: str
    result: str = None
    execution_time: float = None
    status: str = "success"

class NewFunctionRequest(BaseModel):
    name: str
    description: str
    code: str

def _extract_command_params(prompt, function_name):
    if function_name == "run_shell_command" and "command" in prompt.lower():
        return prompt.split("command")[-1].strip()
    return None

@app.post("/execute", response_model=TaskResponse)
async def run_task(user_input: UserPrompt):
    logging.info(f"Received prompt: {user_input.prompt}")
    
    try:
        context = " ".join([f"{cmd['prompt']} -> {cmd['function']}" 
                          for cmd in recent_commands[-3:]]) + " " + user_input.prompt
        function_name = function_finder.find_function(context)
        params = _extract_command_params(user_input.prompt, function_name)
        generated_code = script_maker.create_script(function_name, params)
        
        tools = AutomationTools()
        task = getattr(tools, function_name, None)
        if not task:
            logging.error(f"Function not found: {function_name}")
            raise HTTPException(status_code=404, detail=f"No such function: {function_name}")
        
        start_time = time.time()
        result = task(params) if params else task()
        exec_time = time.time() - start_time
        
        recent_commands.append({
            "prompt": user_input.prompt,
            "function": function_name,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        logging.info(f"Ran {function_name} successfully")
        
        return TaskResponse(
            function=function_name,
            code=generated_code,
            result=result,
            execution_time=exec_time
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Task failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Something broke: {str(e)}")
    
@app.post("/add_function")
async def add_function(new_func: NewFunctionRequest):
    """Adds a custom function to the automation tools."""
    try:
        if hasattr(AutomationTools, new_func.name):
            raise HTTPException(status_code=400, detail="Function name already exists")
        
        # Define the custom function with safe namespace
        def custom_func(self):
            return eval(new_func.code, {"os": os, "subprocess": subprocess, "psutil": psutil})
        
        setattr(AutomationTools, new_func.name, custom_func)
        function_finder.function_descriptions[new_func.name] = new_func.description
        function_finder._load_functions()
        
        logging.info(f"Added custom function: {new_func.name}")
        return {"status": "Function added successfully"}
    except Exception as e:
        logging.error(f"Failed to add function {new_func.name}: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding function: {e}")