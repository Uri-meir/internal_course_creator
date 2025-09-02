# AI Course Creator 🎓

An intelligent system that automatically generates complete online courses from a single domain input. Create professional-quality courses with AI presenters, Jupyter notebooks, and all necessary materials in minutes.

## ✨ Features

- **🤖 AI-Powered Content Generation**: Uses GPT-4 to create comprehensive lesson content
- **🎬 AI Presenter Videos**: Generates talking head videos using D-ID API
- **🎨 Visual Backgrounds**: Creates custom backgrounds with DALL-E 3
- **📓 Interactive Notebooks**: Generates Jupyter notebooks for coding lessons
- **📝 Speech Scripts**: Converts content into natural speech scripts
- **🎬 Video Assembly**: Combines presenter videos with backgrounds
- **📦 Course Packaging**: Creates ready-to-upload course packages
- **🧪 Test Mode**: Full testing environment with mock APIs

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd CourseCreator

# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy environment template
cp env_example.txt .env

# Edit .env with your API keys
nano .env
```

Required API keys:
- **OpenAI**: For GPT-4 content generation and DALL-E image creation
- **D-ID**: For AI presenter video generation

### 3. Run the System

```bash
# Test mode (no API costs)
python main.py --domain "Python Programming" --test

# Production mode
python main.py --domain "Machine Learning Fundamentals"

# End-to-end test
python main.py --test-e2e
```

## 🏗️ System Architecture

The system consists of 8 main components:

1. **Course Planner** - Analyzes domains and generates curriculum structure
2. **Content Generator** - Creates comprehensive lesson content using AI
3. **Notebook Creator** - Generates interactive Jupyter notebooks
4. **Script Writer** - Converts content into natural speech scripts
5. **Background Generator** - Creates visual backgrounds using DALL-E
6. **AI Presenter** - Generates talking head videos using D-ID
7. **Video Assembler** - Combines presenter videos with backgrounds
8. **Course Packager** - Assembles final course package

## 📁 Output Structure

```
output/
├── videos/
│   ├── presenter/          # AI presenter videos
│   ├── final/             # Assembled final videos
│   └── fallback/          # Fallback videos if generation fails
├── notebooks/              # Jupyter notebooks
├── backgrounds/            # Generated background images
├── marketing/              # Course thumbnails and descriptions
├── packages/               # Final course packages
└── resources/              # Lesson materials and code examples
```

## 🧪 Testing

### Test Mode
Run with `--test` flag to use mock APIs instead of real ones:
- No API costs
- Faster execution
- Mock data generation
- Full system validation

### End-to-End Testing
```bash
python main.py --test-e2e
```
Tests the complete workflow without external API calls.

### Unit Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=components

# Run specific test file
pytest tests/test_course_planner.py
```

## 🔧 Configuration

### Environment Variables
- `TEST_MODE`: Set to `true` for testing mode
- `OPENAI_API_KEY`: Your OpenAI API key
- `DID_API_KEY`: Your D-ID API key

### Config File
Create `config.yaml` for custom settings:
```yaml
test_mode: false
output:
  base_dir: output
ai:
  openai_model: gpt-4
  dalle_model: dall-e-3
video:
  resolution: 1920x1080
  fps: 30
```

## 📊 Course Generation Workflow

1. **Domain Analysis** → Understands the course topic
2. **Curriculum Planning** → Creates lesson structure
3. **Content Generation** → Generates lesson materials
4. **Script Writing** → Creates speech scripts
5. **Background Creation** → Generates visual backgrounds
6. **Video Generation** → Creates AI presenter videos
7. **Video Assembly** → Combines videos with backgrounds
8. **Course Packaging** → Creates final package

## 🎯 Supported Course Types

- **Programming & Development**: Python, JavaScript, Web Development
- **Data Science**: Machine Learning, Data Analysis, Statistics
- **Technology**: AI, Cloud Computing, Cybersecurity
- **Business**: Marketing, Finance, Project Management
- **Creative**: Design, Writing, Content Creation

## 💡 Use Cases

- **Online Educators**: Quickly create course content
- **Corporate Training**: Generate training materials
- **Content Creators**: Scale content production
- **EdTech Platforms**: Automate course generation
- **Individual Instructors**: Reduce course creation time

## 🚨 Requirements

- Python 3.8+
- FFmpeg (for video processing)
- Sufficient disk space for video generation
- API keys for OpenAI and D-ID

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For questions or issues:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🔮 Roadmap

- [ ] Multi-language support
- [ ] Advanced video editing features
- [ ] Integration with learning management systems
- [ ] Custom presenter avatars
- [ ] Automated assessment generation
- [ ] Course analytics and insights

---

**Happy Course Creating! 🎓✨** 
