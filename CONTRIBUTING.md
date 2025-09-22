# Contributing to Vomee

We welcome contributions to the Vomee multimodal sensing platform! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

### Code Contributions
- **Bug fixes**: Fix issues in the codebase
- **Feature development**: Add new sensing modalities or processing capabilities
- **Performance improvements**: Optimize capture performance and synchronization
- **Documentation**: Improve code documentation and examples

### Research Contributions
- **Use case examples**: Share your research applications
- **Dataset contributions**: Contribute sample datasets (with appropriate licenses)
- **Benchmarking**: Performance comparisons and evaluations
- **Hardware integration**: Support for new sensors and devices

### Community Contributions
- **Issue reporting**: Report bugs and suggest improvements
- **Testing**: Test on different platforms and hardware configurations
- **Tutorials**: Create tutorials and educational content
- **Translations**: Help translate documentation

## 🚀 Getting Started

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Vomee.git
   cd Vomee
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install in development mode
   pip install -e .[dev]
   ```

3. **Install development dependencies**
   ```bash
   pip install pytest black flake8 sphinx
   ```

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest tests/
   
   # Check code style
   black vomee/ examples/
   flake8 vomee/
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use the PR template
   - Provide clear description of changes
   - Link to related issues

## 📝 Coding Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Black](https://github.com/psf/black) for code formatting
- Maximum line length: 88 characters (Black default)
- Use type hints where applicable

### Code Organization
```python
# Example module structure
"""
Module docstring describing functionality.
"""

import standard_library
import third_party_packages
from local_package import local_module

# Constants
CONSTANT_VALUE = 42

class ExampleClass:
    """Class docstring."""
    
    def __init__(self, param: str):
        """Initialize with clear parameter descriptions."""
        self.param = param
    
    def public_method(self) -> str:
        """Public method with return type annotation."""
        return self._private_method()
    
    def _private_method(self) -> str:
        """Private method indicated by underscore prefix."""
        return f"Processed: {self.param}"
```

### Documentation Standards
- Use Google-style docstrings
- Include parameter types and descriptions
- Provide usage examples for public APIs
- Update README and documentation for new features

### Testing Guidelines
- Write unit tests for all new functionality
- Use pytest for testing framework
- Aim for >80% code coverage
- Include integration tests for hardware interfaces

## 🔧 Hardware Contributions

### Adding New Sensor Support

1. **Create sensor module** in `vomee/capture/`
   ```python
   # vomee/capture/new_sensor_capture.py
   class NewSensorCapture:
       def __init__(self, config):
           pass
       
       def start(self) -> bool:
           pass
       
       def capture(self) -> Optional[Data]:
           pass
       
       def stop(self):
           pass
   ```

2. **Integration with main capture system**
   - Update `VomeeCapture` class
   - Add configuration options
   - Ensure synchronization compatibility

3. **Documentation and examples**
   - Hardware setup instructions
   - Configuration examples
   - Code examples

### Hardware Testing
- Test on multiple platforms (Windows, Linux, macOS)
- Verify synchronization accuracy
- Performance benchmarking
- Error handling validation

## 📊 Data Format Contributions

### Adding New Data Formats
- Implement in `vomee/processing/` module
- Ensure compatibility with existing pipeline
- Add conversion utilities
- Update documentation

### Dataset Contributions
- Follow data licensing requirements
- Provide metadata and documentation
- Include example processing scripts
- Consider privacy and ethical implications

## 🐛 Issue Reporting

### Bug Reports
Use the bug report template and include:
- **Environment**: OS, Python version, hardware setup
- **Steps to reproduce**: Minimal example that triggers the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Logs**: Relevant error messages and stack traces

### Feature Requests
Use the feature request template and include:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: What other approaches were considered?
- **Implementation**: Any ideas on implementation approach?

## 📋 Pull Request Guidelines

### PR Requirements
- [ ] Descriptive title and summary
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Breaking changes documented
- [ ] Related issues linked

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

## 🏆 Recognition

Contributors will be recognized in:
- Repository contributors list
- Documentation acknowledgments
- Release notes
- Academic paper acknowledgments (for significant contributions)

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and community discussion
- **Email**: Direct contact for sensitive issues

### Resources
- [Documentation](https://weixijia.github.io/Vomee)
- [API Reference](docs/api_reference.md)
- [Examples](examples/)
- [Hardware Setup Guide](docs/hardware_setup.md)

## 📜 License

By contributing to Vomee, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Vomee! Your contributions help advance multimodal sensing research and applications. 🚀