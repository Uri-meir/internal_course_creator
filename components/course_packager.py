"""
Course Packager Component
Assembles complete course package ready for platform upload
"""

import os
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import zipfile

logger = logging.getLogger(__name__)

class CoursePackager:
    """
    Assembles complete course package ready for platform upload
    """
    
    def __init__(self, output_dir: str = "output"):
        """Initialize course packager"""
        self.output_dir = Path(output_dir)
        self.package_structure = self._define_package_structure()
        self.metadata_template = self._load_metadata_template()
    
    def _define_package_structure(self) -> Dict[str, str]:
        """Define the standard course package structure"""
        return {
            "videos": "videos/",
            "notebooks": "notebooks/",
            "resources": "resources/",
            "marketing": "marketing/",
            "metadata": "",
            "scripts": "scripts/",
            "backgrounds": "backgrounds/",
            "assessments": "assessments/"
        }
    
    def _load_metadata_template(self) -> Dict[str, Any]:
        """Load course metadata template"""
        return {
            "course_info": {
                "title": "",
                "description": "",
                "difficulty": "",
                "duration_hours": 0,
                "prerequisites": [],
                "learning_objectives": [],
                "target_audience": ""
            },
            "technical_info": {
                "video_format": "MP4",
                "video_resolution": "1920x1080",
                "audio_format": "AAC",
                "notebook_format": "Jupyter (.ipynb)",
                "total_file_size_mb": 0
            },
            "platform_info": {
                "ready_for_upload": False,
                "recommended_platforms": ["Udemy", "Coursera", "Teachable"],
                "pricing_tier": "intermediate",
                "category": "Technology"
            },
            "generation_info": {
                "created_date": "",
                "generator_version": "1.0",
                "ai_models_used": [],
                "total_generation_time_minutes": 0
            }
        }
    
    def create_course_package(self, course_data: Dict[str, Any], domain: str = None) -> str:
        """
        Create complete course package
        
        Args:
            course_data: Dictionary containing all course materials
                - course_info: Course outline and metadata
                - videos: Dictionary of lesson videos
                - notebooks: Dictionary of notebooks
                - content: Lesson content data
                - scripts: Speech scripts
                - backgrounds: Background images
                - assessments: Quiz and exercise data
            domain: Optional domain name for package naming
                
        Returns:
            Path to final course package directory
        """
        try:
            course_info = course_data.get('course_info', {})
            course_title = course_info.get('course_title', 'Unknown Course')
            
            # Use provided domain or extract from course title
            if domain:
                package_domain = domain
            else:
                package_domain = self._extract_domain_from_title(course_title)
            
            logger.info(f"Creating course package for: {course_title}")
            logger.info(f"Using domain for package name: {package_domain}")
            
            # Create package directory
            package_dir = self._create_package_directory(package_domain)
            
            # Organize all materials
            self._organize_videos(course_data.get('videos', {}), package_dir)
            self._organize_notebooks(course_data.get('notebooks', {}), package_dir)
            self._organize_resources(course_data.get('content', {}), package_dir)
            self._organize_marketing(course_data.get('thumbnails', {}), package_dir)
            self._organize_scripts(course_data.get('scripts', {}), package_dir)
            self._organize_backgrounds(course_data.get('backgrounds', {}), package_dir)
            self._organize_assessments(course_data.get('content', {}), package_dir)
            
            # Generate metadata
            self._generate_course_metadata(course_info, package_dir)
            self._generate_curriculum_file(course_info, package_dir)
            self._create_readme(course_info, package_dir)
            self._create_setup_instructions(package_dir)
            
            # Validate package
            validation_result = self._validate_package(package_dir)
            if validation_result['valid']:
                logger.info(f"Package validation complete. {validation_result['checks_passed']}/{validation_result['total_checks']} checks passed")
            else:
                logger.warning(f"Package validation issues: {validation_result['issues']}")
            
            # Create compressed archive
            archive_path = self._create_compressed_archive(package_dir)
            
            logger.info(f"Course package created successfully: {package_dir}")
            logger.info(f"Compressed archive: {archive_path}")
            
            return str(package_dir)
            
        except Exception as e:
            logger.error(f"Error creating course package: {str(e)}")
            raise
    
    def _extract_domain_from_title(self, course_title: str) -> str:
        """Extract a clean domain name from the course title"""
        
        # Remove common prefixes and suffixes
        title = course_title.replace("Complete ", "").replace(" Course", "").replace("Master ", "")
        
        # If title is still too long, truncate it
        if len(title) > 50:
            # Try to find a good breaking point
            words = title.split()
            truncated = ""
            for word in words:
                if len(truncated + word) <= 50:
                    truncated += word + " "
                else:
                    break
            title = truncated.strip()
        
        # Clean up the title for use as directory name
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')
        
        # Ensure it's not empty
        if not safe_title:
            safe_title = "course"
        
        return safe_title
    
    def _create_package_directory(self, domain: str) -> Path:
        """Create main package directory with proper structure"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"course_package_{domain}_{timestamp}"
        
        package_dir = self.output_dir / package_name
        
        # Create directory structure
        for folder_name, folder_path in self.package_structure.items():
            if folder_path:  # Skip empty paths (root files)
                (package_dir / folder_path).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Package directory created: {package_dir}")
        return package_dir
    
    def _organize_videos(self, videos: Dict[int, str], package_dir: Path) -> None:
        """Organize video files in package"""
        
        try:
            video_dir = package_dir / self.package_structure["videos"]
            
            for lesson_number, video_path in videos.items():
                if os.path.exists(video_path):
                    # Create descriptive filename
                    filename = f"lesson_{lesson_number:02d}.mp4"
                    destination = video_dir / filename
                    
                    # Copy video file
                    shutil.copy2(video_path, destination)
                    logger.info(f"Video copied: {filename}")
                else:
                    logger.warning(f"Video not found: {video_path}")
            
        except Exception as e:
            logger.error(f"Error organizing videos: {str(e)}")
    
    def _organize_notebooks(self, notebooks: Dict[int, str], package_dir: Path) -> None:
        """Organize notebook files in package"""
        
        try:
            notebook_dir = package_dir / self.package_structure["notebooks"]
            
            for lesson_number, notebook_content in notebooks.items():
                # Save notebook
                filename = f"lesson_{lesson_number:02d}_notebook.ipynb"
                notebook_path = notebook_dir / filename
                
                with open(notebook_path, 'w', encoding='utf-8') as f:
                    if isinstance(notebook_content, str):
                        f.write(notebook_content)
                    else:
                        json.dump(notebook_content, f, indent=2)
                
                logger.info(f"Notebook saved: {filename}")
            
        except Exception as e:
            logger.error(f"Error organizing notebooks: {str(e)}")
    
    def _organize_resources(self, lesson_contents: Dict[int, Dict[str, Any]], package_dir: Path) -> None:
        """Organize resource files and lesson materials"""
        
        try:
            resources_dir = package_dir / self.package_structure["resources"]
            
            # Create subdirectories
            (resources_dir / "lesson_materials").mkdir(exist_ok=True)
            (resources_dir / "slides").mkdir(exist_ok=True)
            (resources_dir / "datasets").mkdir(exist_ok=True)
            
            for lesson_number, content in lesson_contents.items():
                # Save lesson content as JSON
                lesson_file = resources_dir / "lesson_materials" / f"lesson_{lesson_number:02d}_content.json"
                with open(lesson_file, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Resources organized for lesson {lesson_number}")
            
        except Exception as e:
            logger.error(f"Error organizing resources: {str(e)}")
    
    def _organize_marketing(self, thumbnails: Dict[str, str], package_dir: Path) -> None:
        """Organize marketing materials"""
        
        try:
            marketing_dir = package_dir / self.package_structure["marketing"]
            
            # Copy course thumbnail if available
            if 'course_thumbnail' in thumbnails:
                thumbnail_path = thumbnails['course_thumbnail']
                if os.path.exists(thumbnail_path):
                    shutil.copy2(thumbnail_path, marketing_dir / "course_thumbnail.png")
            
            logger.info("Marketing materials organized")
            
        except Exception as e:
            logger.error(f"Error organizing marketing materials: {str(e)}")
    
    def _organize_scripts(self, scripts: Dict[int, str], package_dir: Path) -> None:
        """Organize speech scripts"""
        
        try:
            scripts_dir = package_dir / self.package_structure["scripts"]
            
            for lesson_number, script in scripts.items():
                filename = f"lesson_{lesson_number:02d}_script.txt"
                script_path = scripts_dir / filename
                
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(script)
                
                logger.info(f"Script saved: {filename}")
            
        except Exception as e:
            logger.error(f"Error organizing scripts: {str(e)}")
    
    def _organize_backgrounds(self, backgrounds: Dict[int, str], package_dir: Path) -> None:
        """Organize background images"""
        
        try:
            backgrounds_dir = package_dir / self.package_structure["backgrounds"]
            
            for lesson_number, background_path in backgrounds.items():
                if os.path.exists(background_path):
                    filename = f"lesson_{lesson_number:02d}_background.png"
                    destination = backgrounds_dir / filename
                    
                    shutil.copy2(background_path, destination)
                    logger.info(f"Background copied: {filename}")
                else:
                    logger.warning(f"Background not found: {background_path}")
            
        except Exception as e:
            logger.error(f"Error organizing backgrounds: {str(e)}")
    
    def _organize_assessments(self, lesson_contents: Dict[int, Dict[str, Any]], package_dir: Path) -> None:
        """Organize assessment materials"""
        
        try:
            assessments_dir = package_dir / self.package_structure["assessments"]
            
            # Create assessment structure
            (assessments_dir / "quizzes").mkdir(exist_ok=True)
            (assessments_dir / "exercises").mkdir(exist_ok=True)
            (assessments_dir / "projects").mkdir(exist_ok=True)
            
            logger.info("Assessment materials organized")
            
        except Exception as e:
            logger.error(f"Error organizing assessments: {str(e)}")
    
    def _generate_course_metadata(self, course_info: Dict[str, Any], package_dir: Path) -> None:
        """Generate comprehensive course metadata"""
        
        try:
            metadata = self.metadata_template.copy()
            metadata["course_info"].update({
                "title": course_info.get('course_title', ''),
                "description": course_info.get('description', ''),
                "difficulty": course_info.get('difficulty', ''),
                "duration_hours": course_info.get('total_duration_hours', 0),
                "prerequisites": course_info.get('prerequisites', []),
                "learning_objectives": course_info.get('learning_objectives', []),
                "target_audience": course_info.get('target_audience', '')
            })
            
            metadata["generation_info"]["created_date"] = datetime.now().isoformat()
            metadata["generation_info"]["ai_models_used"] = ["GPT-4", "DALL-E 3", "D-ID"]
            
            # Save metadata
            metadata_path = package_dir / "course_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info("Course metadata generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating metadata: {str(e)}")
    
    def _generate_curriculum_file(self, course_info: Dict[str, Any], package_dir: Path) -> None:
        """Generate curriculum file"""
        
        try:
            curriculum_path = package_dir / "curriculum.json"
            with open(curriculum_path, 'w', encoding='utf-8') as f:
                json.dump(course_info, f, indent=2, ensure_ascii=False)
            
            logger.info("Curriculum file generated")
            
        except Exception as e:
            logger.error(f"Error generating curriculum file: {str(e)}")
    
    def _create_readme(self, course_info: Dict[str, Any], package_dir: Path) -> None:
        """Create comprehensive README file"""
        
        try:
            readme_content = f"""# {course_info.get('course_title', 'Course')}

## Overview
{course_info.get('description', 'Comprehensive course covering essential topics.')}

## Course Details
- **Difficulty**: {course_info.get('difficulty', 'Intermediate')}
- **Duration**: {course_info.get('total_duration_hours', 0)} hours
- **Lessons**: {len(course_info.get('lessons', []))}
- **Target Audience**: {course_info.get('target_audience', 'Developers and learners')}

## Prerequisites
{chr(10).join([f"- {prereq}" for prereq in course_info.get('prerequisites', [])])}

## Learning Objectives
{chr(10).join([f"- {obj}" for obj in course_info.get('learning_objectives', [])])}

## Course Structure
This course package contains:

### 📹 Videos
- HD quality lesson videos with AI presenter
- Professional backgrounds and graphics
- Optimized for online learning platforms

### 📓 Notebooks
- Interactive Jupyter notebooks for hands-on learning
- Code examples and exercises
- Step-by-step solutions

### 📚 Resources
- Complete lesson materials
- Code examples and datasets
- Additional learning resources

### 🎯 Assessments
- Quizzes and exercises
- Project-based learning materials
- Progress tracking tools

## Getting Started
1. Review the course overview and prerequisites
2. Start with Lesson 1 and progress sequentially
3. Complete hands-on exercises in the notebooks
4. Take assessments to test your understanding

## Technical Requirements
- Python 3.8+
- Jupyter Notebook or JupyterLab
- Required packages listed in requirements.txt

## Support
For questions or issues, refer to the course materials or contact support.

---
*Generated by AI Course Creator*
"""
            
            readme_path = package_dir / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            logger.info("README file created successfully")
            
        except Exception as e:
            logger.error(f"Error creating README: {str(e)}")
    
    def _create_setup_instructions(self, package_dir: Path) -> None:
        """Create setup instructions"""
        
        try:
            setup_content = """# Course Setup Instructions

## Environment Setup

### 1. Python Environment
- Ensure Python 3.8+ is installed
- Create a virtual environment (recommended):
  ```bash
  python -m venv course_env
  source course_env/bin/activate  # On Windows: course_env\\Scripts\\activate
  ```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Jupyter Setup
```bash
pip install jupyter
jupyter notebook
```

## Course Navigation

### Video Lessons
- All video files are in the `videos/` directory
- Videos are numbered sequentially (lesson_01.mp4, lesson_02.mp4, etc.)
- Play videos in order for best learning experience

### Interactive Notebooks
- Notebooks are in the `notebooks/` directory
- Open with Jupyter Notebook or JupyterLab
- Follow along with the video lessons

### Additional Resources
- Lesson materials in `resources/lesson_materials/`
- Background images in `backgrounds/`
- Scripts in `scripts/`

## Best Practices

1. **Watch First**: View the video lesson before working with notebooks
2. **Practice**: Complete all exercises and code examples
3. **Review**: Use the resources to reinforce learning
4. **Build**: Apply concepts to your own projects

## Troubleshooting

### Common Issues
- **Video playback**: Ensure you have a modern video player
- **Notebook errors**: Check Python version and package compatibility
- **Missing files**: Verify all files were extracted from the package

### Getting Help
- Review lesson materials for clarification
- Check the course metadata for additional information
- Contact course support if issues persist

---
*Happy Learning!*
"""
            
            setup_path = package_dir / "setup_instructions.md"
            with open(setup_path, 'w', encoding='utf-8') as f:
                f.write(setup_content)
            
            logger.info("Setup instructions created successfully")
            
        except Exception as e:
            logger.error(f"Error creating setup instructions: {str(e)}")
    
    def _validate_package(self, package_dir: Path) -> Dict[str, Any]:
        """Validate package completeness"""
        
        try:
            validation = {
                "package_path": str(package_dir),
                "validation_date": datetime.now().isoformat(),
                "checks": {},
                "overall_status": "unknown",
                "valid": False,
                "checks_passed": 0,
                "total_checks": 0,
                "issues": []
            }
            
            # Check required directories
            required_dirs = list(self.package_structure.values())
            for dir_name in required_dirs:
                if dir_name:
                    dir_path = package_dir / dir_name
                    validation["checks"][f"directory_{dir_name.rstrip('/')}"] = dir_path.exists()
                    validation["total_checks"] += 1
                    if dir_path.exists():
                        validation["checks_passed"] += 1
            
            # Check course metadata
            metadata_path = package_dir / "course_metadata.json"
            validation["checks"]["metadata_file"] = metadata_path.exists()
            validation["total_checks"] += 1
            if metadata_path.exists():
                validation["checks_passed"] += 1
            
            # Check README
            readme_path = package_dir / "README.md"
            validation["checks"]["readme_file"] = readme_path.exists()
            validation["total_checks"] += 1
            if readme_path.exists():
                validation["checks_passed"] += 1
            
            # Check setup instructions
            setup_path = package_dir / "setup_instructions.md"
            validation["checks"]["setup_instructions"] = setup_path.exists()
            validation["total_checks"] += 1
            if setup_path.exists():
                validation["checks_passed"] += 1
            
            # Calculate overall status
            if validation["checks_passed"] == validation["total_checks"]:
                validation["overall_status"] = "complete"
                validation["valid"] = True
            elif validation["checks_passed"] >= validation["total_checks"] * 0.8:
                validation["overall_status"] = "mostly_complete"
                validation["valid"] = True
            else:
                validation["overall_status"] = "incomplete"
                validation["valid"] = False
            
            # Save validation report
            validation_path = package_dir / "validation_report.json"
            with open(validation_path, 'w', encoding='utf-8') as f:
                json.dump(validation, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Package validation complete. {validation['checks_passed']}/{validation['total_checks']} checks passed")
            return validation
            
        except Exception as e:
            logger.error(f"Error validating package: {str(e)}")
            return {"error": str(e), "overall_status": "error", "valid": False}
    
    def _create_compressed_archive(self, package_dir: Path) -> str:
        """Create compressed archive of the package"""
        
        try:
            archive_path = f"{package_dir}.zip"
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(package_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, package_dir.parent)
                        zipf.write(file_path, arcname)
            
            logger.info(f"Compressed archive created: {archive_path}")
            return archive_path
            
        except Exception as e:
            logger.error(f"Error creating compressed archive: {str(e)}")
            return "" 
