import re
import os
import subprocess
import tempfile
import time

def extract_class_name(java_code: str) -> str:
    """Extract public class name or the first class name from Java code."""
    # Look for public class / record / interface / enum
    match = re.search(r'\bpublic\s+(?:final\s+|abstract\s+)?(?:class|record|enum|interface)\s+([A-Za-z0-9_$]+)', java_code)
    if match:
        return match.group(1)
    
    # Look for any class / record
    match = re.search(r'\b(?:class|record|enum|interface)\s+([A-Za-z0-9_$]+)', java_code)
    if match:
        return match.group(1)
        
    return "Main"

def wrap_code_if_needed(java_code: str) -> tuple[str, str]:
    """Wraps bare statements or methods in a Main class if missing."""
    trimmed = java_code.strip()
    
    # Check if there is already a class declaration
    if re.search(r'\b(class|record|interface|enum)\s+[A-Za-z0-9_$]+', trimmed):
        class_name = extract_class_name(trimmed)
        return trimmed, class_name
        
    # Check if it has a main method without class
    if "public static void main" in trimmed:
        code = f"""public class Main {{
    {trimmed}
}}"""
        return code, "Main"
        
    # Bare statements inside main
    code = f"""public class Main {{
    public static void main(String[] args) {{
        {trimmed}
    }}
}}"""
    return code, "Main"

def run_java_code(java_code: str, stdin_input: str = "", timeout: float = 8.0) -> dict:
    """Compiles and executes Java code safely."""
    code, class_name = wrap_code_if_needed(java_code)
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        java_file_path = os.path.join(tmp_dir, f"{class_name}.java")
        try:
            with open(java_file_path, "w", encoding="utf-8") as f:
                f.write(code)
        except Exception as e:
            return {
                "success": False,
                "compiled": False,
                "error": f"Failed to write Java source file: {str(e)}",
                "stdout": "",
                "stderr": "",
                "className": class_name
            }
            
        # 1. Compile with javac
        compile_start = time.time()
        try:
            compile_proc = subprocess.run(
                ["javac", f"{class_name}.java"],
                cwd=tmp_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "compiled": False,
                "error": "Compilation timed out.",
                "stdout": "",
                "stderr": "Compilation took longer than allowed timeout.",
                "className": class_name
            }
        except Exception as e:
            return {
                "success": False,
                "compiled": False,
                "error": f"Failed to execute javac: {str(e)}",
                "stdout": "",
                "stderr": "",
                "className": class_name
            }

        if compile_proc.returncode != 0:
            return {
                "success": False,
                "compiled": False,
                "error": "Compilation Error",
                "stdout": compile_proc.stdout,
                "stderr": compile_proc.stderr,
                "className": class_name
            }
            
        # 2. Execute with java
        exec_start = time.time()
        try:
            exec_proc = subprocess.run(
                ["java", "-cp", ".", class_name],
                cwd=tmp_dir,
                input=stdin_input,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            exec_duration = (time.time() - exec_start) * 1000
            
            return {
                "success": exec_proc.returncode == 0,
                "compiled": True,
                "stdout": exec_proc.stdout,
                "stderr": exec_proc.stderr,
                "exitCode": exec_proc.returncode,
                "executionTimeMs": round(exec_duration, 1),
                "className": class_name
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "compiled": True,
                "error": "Runtime Timeout (execution exceeded limit, possible infinite loop)",
                "stdout": "",
                "stderr": f"Execution exceeded {timeout} seconds limit.",
                "className": class_name
            }
        except Exception as e:
            return {
                "success": False,
                "compiled": True,
                "error": f"Failed to execute Java program: {str(e)}",
                "stdout": "",
                "stderr": "",
                "className": class_name
            }
