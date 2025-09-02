"""
Notebook Creator Component
Creates Jupyter notebooks for coding lessons
"""

import json
import logging
import nbformat as nbf
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class NotebookCreator:
    """
    Creates Jupyter notebooks for hands-on coding lessons
    """
    
    def __init__(self):
        """Initialize notebook creator"""
        pass
    
    def create_lesson_notebook(self, lesson_content: Dict[str, Any]) -> str:
        """
        Create Jupyter notebook from lesson content
        
        Args:
            lesson_content: Generated lesson content
            
        Returns:
            Notebook content as JSON string
        """
        try:
            lesson_num = lesson_content.get('lesson_number', 1)
            title = lesson_content.get('title', 'Lesson')
            
            logger.info(f"Creating notebook for lesson {lesson_num}: {title}")
            
            # Create new notebook
            nb = nbf.v4.new_notebook()
            
            # Add title cell
            title_cell = nbf.v4.new_markdown_cell(f"# {title}\n\n## Overview\n{lesson_content.get('introduction', '')}")
            nb.cells.append(title_cell)
            
            # Add learning objectives
            if 'learning_objectives' in lesson_content:
                objectives = lesson_content['learning_objectives']
                obj_cell = nbf.v4.new_markdown_cell(f"## Learning Objectives\n\n" + "\n".join([f"- {obj}" for obj in objectives]))
                nb.cells.append(obj_cell)
            
            # Add theory content if available
            if 'theory_content' in lesson_content:
                theory = lesson_content['theory_content']
                if 'main_concepts' in theory:
                    concepts = theory['main_concepts']
                    theory_cell = nbf.v4.new_markdown_cell(f"## Key Concepts\n\n" + "\n".join([f"- **{concept}**" for concept in concepts]))
                    nb.cells.append(theory_cell)
            
            # Add code examples
            if 'code_examples' in lesson_content:
                examples = lesson_content['code_examples']
                for i, example in enumerate(examples, 1):
                    # Example description
                    desc_cell = nbf.v4.new_markdown_cell(f"### Example {i}: {example.get('title', 'Code Example')}\n\n{example.get('description', '')}")
                    nb.cells.append(desc_cell)
                    
                    # Code cell
                    code_cell = nbf.v4.new_code_cell(example.get('code', '# Your code here'))
                    nb.cells.append(code_cell)
                    
                    # Explanation
                    if 'explanation' in example:
                        exp_cell = nbf.v4.new_markdown_cell(f"**Explanation:** {example['explanation']}")
                        nb.cells.append(exp_cell)
            
            # Add exercises
            if 'exercises' in lesson_content:
                exercises = lesson_content['exercises']
                for i, exercise in enumerate(exercises, 1):
                    # Exercise description
                    ex_cell = nbf.v4.new_markdown_cell(f"## Exercise {i}: {exercise.get('title', 'Practice Exercise')}\n\n{exercise.get('description', '')}")
                    nb.cells.append(ex_cell)
                    
                    # Hints
                    if 'hints' in exercise:
                        hints = exercise['hints']
                        hints_cell = nbf.v4.new_markdown_cell(f"**Hints:**\n\n" + "\n".join([f"- {hint}" for hint in hints]))
                        nb.cells.append(hints_cell)
                    
                    # Code cell for exercise
                    code_cell = nbf.v4.new_code_cell("# Your solution here\n# Try implementing the exercise")
                    nb.cells.append(code_cell)
            
            # Add summary
            if 'summary' in lesson_content:
                summary_cell = nbf.v4.new_markdown_cell(f"## Summary\n\n{lesson_content['summary']}")
                nb.cells.append(summary_cell)
            
            # Add next steps
            next_steps_cell = nbf.v4.new_markdown_cell("## Next Steps\n\n- Practice the concepts covered\n- Try the exercises\n- Experiment with variations\n- Review the key takeaways")
            nb.cells.append(next_steps_cell)
            
            # Convert to JSON
            notebook_json = nbf.writes(nb)
            
            logger.info("Notebook created successfully")
            return notebook_json
            
        except Exception as e:
            logger.error(f"Error creating notebook: {str(e)}")
            return self._create_fallback_notebook(lesson_content)
    
    def _create_fallback_notebook(self, lesson_content: Dict[str, Any]) -> str:
        """Create fallback notebook if generation fails"""
        
        nb = nbf.v4.new_notebook()
        
        # Basic structure
        title_cell = nbf.v4.new_markdown_cell(f"# {lesson_content.get('title', 'Lesson')}\n\n## Overview\nBasic lesson content")
        nb.cells.append(title_cell)
        
        code_cell = nbf.v4.new_code_cell("# Your code here\nprint('Hello World')")
        nb.cells.append(code_cell)
        
        summary_cell = nbf.v4.new_markdown_cell("## Summary\nKey concepts covered in this lesson")
        nb.cells.append(summary_cell)
        
        return nbf.writes(nb) 
