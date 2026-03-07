# Contributing to EMOTION CIPHER

Thank you for your interest in contributing to EMOTION CIPHER! This document provides guidelines for contributing to the project.

## 🎯 Project Vision

EMOTION CIPHER aims to bridge the gap between encryption and emotional intelligence, creating a system that preserves both privacy and emotional context.

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/emotion-cipher.git
   cd emotion-cipher
   ```
3. **Set up development environment**:
   ```bash
   ./start.sh  # or start.bat on Windows
   ```

## 🔧 Development Workflow

### Backend Development

1. **Create a virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

4. **Format code**:
   ```bash
   black src/
   ```

### Frontend Development

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server**:
   ```bash
   npm run dev
   ```

3. **Run tests**:
   ```bash
   npm test
   ```

4. **Lint code**:
   ```bash
   npm run lint
   ```

## 📝 Code Style

### Python

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for all public functions
- Use `black` for code formatting
- Maximum line length: 100 characters

### TypeScript/React

- Follow Airbnb React style guide
- Use functional components with hooks
- Use TypeScript for type safety
- Use ESLint and Prettier for formatting
- Maximum line length: 100 characters

## 🧪 Testing

### Backend Tests

- Write unit tests for all new functions
- Write integration tests for API endpoints
- Aim for 85%+ code coverage
- Use pytest fixtures for common setup

### Frontend Tests

- Write unit tests for components
- Write integration tests for user flows
- Use React Testing Library
- Aim for 75%+ code coverage

## 📦 Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   # Backend
   cd backend
   pytest tests/
   
   # Frontend
   cd frontend
   npm test
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   
   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for refactoring
   - `style:` for formatting

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes
   - Ensure all tests pass

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python version, Node version, browser
6. **Screenshots**: If applicable

## 💡 Feature Requests

When requesting features, please include:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Any alternative solutions considered?
4. **Additional Context**: Any other relevant information

## 🎨 Design Guidelines

### UI/UX

- Maintain glassmorphism design language
- Use consistent color palette for emotions
- Ensure responsive design (mobile, tablet, desktop)
- Add smooth animations with Framer Motion
- Follow accessibility best practices

### API Design

- Use RESTful conventions
- Return appropriate HTTP status codes
- Provide clear error messages
- Document all endpoints in OpenAPI/Swagger
- Version APIs when making breaking changes

## 📚 Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for technical changes
- Add inline comments for complex logic
- Write clear commit messages
- Update DEMO.md for new features

## 🔒 Security

- Never commit secrets or API keys
- Use environment variables for configuration
- Follow security best practices
- Report security vulnerabilities privately

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on what's best for the project
- Show empathy towards others

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions make EMOTION CIPHER better for everyone. We appreciate your time and effort!

---

**Questions?** Open an issue or reach out to the maintainers.
