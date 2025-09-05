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
            
            # Add enhanced exercises with solutions
            self._add_enhanced_exercises(nb, lesson_content)
            
            # Add solutions section
            self._add_solutions_section(nb, lesson_content)
            
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
    
    def _add_enhanced_exercises(self, nb, lesson_content: Dict[str, Any]):
        """Add enhanced exercises with multiple types and difficulty levels"""
        
        # Add practice section header
        practice_header = nbf.v4.new_markdown_cell("""# 🛠️ Hands-On Practice

Time to put your knowledge into action! Complete the following exercises to reinforce what you've learned.

**Instructions:**
- Try to solve each exercise on your own first
- Use the hints if you get stuck
- Check your solutions against the provided answers at the end
- Experiment with variations to deepen your understanding""")
        nb.cells.append(practice_header)
        
        # Process exercises from lesson content
        if 'exercises' in lesson_content:
            exercises = lesson_content['exercises']
            for i, exercise in enumerate(exercises, 1):
                self._add_single_exercise(nb, exercise, i)
        
        # Process hands_on_exercises if available (enhanced format)
        if 'hands_on_exercises' in lesson_content:
            hands_on = lesson_content['hands_on_exercises']
            start_num = len(lesson_content.get('exercises', [])) + 1
            
            for i, exercise in enumerate(hands_on, start_num):
                self._add_advanced_exercise(nb, exercise, i)
    
    def _add_single_exercise(self, nb, exercise: Dict[str, Any], exercise_num: int):
        """Add a single exercise with enhanced formatting"""
        
        # Exercise header
        title = exercise.get('title', f'Exercise {exercise_num}')
        description = exercise.get('description', '')
        difficulty = exercise.get('difficulty', 'Medium')
        
        # Difficulty emoji mapping
        difficulty_emoji = {
            'Easy': '🟢',
            'Medium': '🟡', 
            'Hard': '🔴',
            'Expert': '🟣'
        }
        
        exercise_header = f"""## 📝 Exercise {exercise_num}: {title}

**Difficulty:** {difficulty_emoji.get(difficulty, '🟡')} {difficulty}

{description}"""
        
        header_cell = nbf.v4.new_markdown_cell(exercise_header)
        nb.cells.append(header_cell)
        
        # Add requirements if available
        if 'requirements' in exercise:
            requirements = exercise['requirements']
            req_text = "**Requirements:**\n\n" + "\n".join([f"✅ {req}" for req in requirements])
            req_cell = nbf.v4.new_markdown_cell(req_text)
            nb.cells.append(req_cell)
        
        # Add starter code if available
        if 'starter_code' in exercise:
            starter_cell = nbf.v4.new_code_cell(exercise['starter_code'])
            nb.cells.append(starter_cell)
        else:
            # Default starter code
            starter_cell = nbf.v4.new_code_cell(f"# Exercise {exercise_num}: {title}\n# Your solution here\n\n")
            nb.cells.append(starter_cell)
        
        # Add hints
        if 'hints' in exercise:
            hints = exercise['hints']
            hints_text = """<details>
<summary>💡 <strong>Hints (Click to expand)</strong></summary>

""" + "\n".join([f"- {hint}" for hint in hints]) + "\n\n</details>"
            
            hints_cell = nbf.v4.new_markdown_cell(hints_text)
            nb.cells.append(hints_cell)
        
        # Add test cases if available
        if 'test_cases' in exercise:
            test_cell = nbf.v4.new_markdown_cell("**Test your solution with these examples:**")
            nb.cells.append(test_cell)
            
            test_code = "# Test cases\n"
            for test in exercise['test_cases']:
                test_code += f"# Expected: {test.get('expected', 'N/A')}\n"
                test_code += f"{test.get('input', '')}\n\n"
            
            test_code_cell = nbf.v4.new_code_cell(test_code)
            nb.cells.append(test_code_cell)
    
    def _add_advanced_exercise(self, nb, exercise: Dict[str, Any], exercise_num: int):
        """Add advanced exercise with comprehensive structure"""
        
        title = exercise.get('title', f'Advanced Exercise {exercise_num}')
        description = exercise.get('description', '')
        learning_outcome = exercise.get('learning_outcome', '')
        
        # Advanced exercise header
        exercise_header = f"""## 🚀 Exercise {exercise_num}: {title}

{description}

**Learning Outcome:** {learning_outcome}"""
        
        header_cell = nbf.v4.new_markdown_cell(exercise_header)
        nb.cells.append(header_cell)
        
        # Add step-by-step instructions
        if 'instructions' in exercise:
            instructions = exercise['instructions']
            inst_text = "**Step-by-step Instructions:**\n\n"
            for i, step in enumerate(instructions, 1):
                inst_text += f"{i}. {step}\n"
            
            inst_cell = nbf.v4.new_markdown_cell(inst_text)
            nb.cells.append(inst_cell)
        
        # Add starter code
        starter_code = exercise.get('starter_code', f"# Exercise {exercise_num}: {title}\n# Implement your solution here\n\n")
        starter_cell = nbf.v4.new_code_cell(starter_code)
        nb.cells.append(starter_cell)
        
        # Add hints with collapsible format
        if 'hints' in exercise:
            hints = exercise['hints']
            hints_text = """<details>
<summary>💡 <strong>Need Help? Click for Hints</strong></summary>

""" + "\n".join([f"**Hint {i}:** {hint}" for i, hint in enumerate(hints, 1)]) + "\n\n</details>"
            
            hints_cell = nbf.v4.new_markdown_cell(hints_text)
            nb.cells.append(hints_cell)
        
        # Add bonus challenge if available
        if 'bonus_challenge' in exercise:
            bonus = exercise['bonus_challenge']
            bonus_text = f"""### 🌟 Bonus Challenge

{bonus}

*This is optional but will help you master the concept!*"""
            
            bonus_cell = nbf.v4.new_markdown_cell(bonus_text)
            nb.cells.append(bonus_cell)
            
            bonus_code_cell = nbf.v4.new_code_cell("# Bonus challenge solution\n# Try the advanced version here\n\n")
            nb.cells.append(bonus_code_cell)
    
    def _add_solutions_section(self, nb, lesson_content: Dict[str, Any]):
        """Add comprehensive solutions section"""
        
        # Solutions header
        solutions_header = nbf.v4.new_markdown_cell("""---

# 📚 Solutions & Explanations

Below are the complete solutions to all exercises. Try to solve them yourself first before looking at the answers!

<details>
<summary><strong>⚠️ Click here to reveal all solutions</strong></summary>

""")
        nb.cells.append(solutions_header)
        
        # Add solutions for regular exercises
        if 'exercises' in lesson_content:
            exercises = lesson_content['exercises']
            for i, exercise in enumerate(exercises, 1):
                self._add_exercise_solution(nb, exercise, i)
        
        # Add solutions for hands-on exercises
        if 'hands_on_exercises' in lesson_content:
            hands_on = lesson_content['hands_on_exercises']
            start_num = len(lesson_content.get('exercises', [])) + 1
            
            for i, exercise in enumerate(hands_on, start_num):
                self._add_advanced_solution(nb, exercise, i)
        
        # Close the collapsible section
        closing_cell = nbf.v4.new_markdown_cell("</details>")
        nb.cells.append(closing_cell)
        
        # Add reflection questions
        reflection_cell = nbf.v4.new_markdown_cell("""## 🤔 Reflection Questions

Take a moment to reflect on what you've learned:

1. **What was the most challenging part of these exercises?**
2. **How do these concepts apply to real-world programming?**
3. **What would you like to explore further?**
4. **Can you think of variations or improvements to these solutions?**

Write your thoughts below:""")
        nb.cells.append(reflection_cell)
        
        # Reflection text area
        reflection_text_cell = nbf.v4.new_markdown_cell("""**Your Reflections:**

*Double-click this cell to add your thoughts...*

1. Most challenging part:

2. Real-world applications:

3. Further exploration:

4. Variations/improvements:
""")
        nb.cells.append(reflection_text_cell)
    
    def _add_exercise_solution(self, nb, exercise: Dict[str, Any], exercise_num: int):
        """Add solution for a single exercise"""
        
        title = exercise.get('title', f'Exercise {exercise_num}')
        solution = exercise.get('solution', f'# Solution for {title}\n# Implementation would go here')
        explanation = exercise.get('explanation', 'No explanation provided.')
        
        # Solution header
        sol_header = f"### 💡 Solution {exercise_num}: {title}"
        header_cell = nbf.v4.new_markdown_cell(sol_header)
        nb.cells.append(header_cell)
        
        # Solution code
        solution_cell = nbf.v4.new_code_cell(solution)
        nb.cells.append(solution_cell)
        
        # Explanation
        explanation_text = f"**Explanation:**\n\n{explanation}"
        exp_cell = nbf.v4.new_markdown_cell(explanation_text)
        nb.cells.append(exp_cell)
        
        # Add separator
        separator_cell = nbf.v4.new_markdown_cell("---")
        nb.cells.append(separator_cell)
    
    def _add_advanced_solution(self, nb, exercise: Dict[str, Any], exercise_num: int):
        """Add solution for advanced exercise"""
        
        title = exercise.get('title', f'Advanced Exercise {exercise_num}')
        solution = exercise.get('solution', f'# Solution for {title}\n# Advanced implementation')
        explanation = exercise.get('solution_explanation', 'Detailed explanation not provided.')
        
        # Solution header
        sol_header = f"### 🚀 Solution {exercise_num}: {title}"
        header_cell = nbf.v4.new_markdown_cell(sol_header)
        nb.cells.append(header_cell)
        
        # Solution code
        solution_cell = nbf.v4.new_code_cell(solution)
        nb.cells.append(solution_cell)
        
        # Detailed explanation
        explanation_text = f"**Detailed Explanation:**\n\n{explanation}"
        exp_cell = nbf.v4.new_markdown_cell(explanation_text)
        nb.cells.append(exp_cell)
        
        # Add key concepts
        if 'key_concepts' in exercise:
            concepts = exercise['key_concepts']
            concepts_text = "**Key Concepts Demonstrated:**\n\n" + "\n".join([f"- {concept}" for concept in concepts])
            concepts_cell = nbf.v4.new_markdown_cell(concepts_text)
            nb.cells.append(concepts_cell)
        
        # Add bonus solution if available
        if 'bonus_solution' in exercise:
            bonus_sol = exercise['bonus_solution']
            bonus_header = f"#### 🌟 Bonus Solution {exercise_num}"
            bonus_header_cell = nbf.v4.new_markdown_cell(bonus_header)
            nb.cells.append(bonus_header_cell)
            
            bonus_sol_cell = nbf.v4.new_code_cell(bonus_sol)
            nb.cells.append(bonus_sol_cell)
        
        # Add separator
        separator_cell = nbf.v4.new_markdown_cell("---")
        nb.cells.append(separator_cell)
