# Changelog

All notable changes to the Ultimate Sensor Monitor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-06-04

### Added
- Production-ready architecture with clean separation of concerns.
- Docker containerization with multi-stage builds.
- CI/CD pipeline with GitHub Actions.
- Comprehensive error handling and logging.
- Security layer with authentication and input validation.
- Professional Windows launcher system.
- Type-safe models and API contracts.
- WebSocket connection management with auto-reconnection.
- Environment-based configuration management.
- Comprehensive documentation suite.
- All Svelte components and documentation updated to strictly adhere to Svelte 4.xx standards.

### Changed
- Restructured project for production deployment.
- **Ensured all Svelte components utilize Svelte 4 syntax (props, reactive statements, lifecycle methods, event handling).**
- Removed any Svelte 5 specific syntax (Runes like `$state`, `$derived`, `$props`, `$effect`) from the Svelte codebase.
- Improved backend architecture with modular design.
- Enhanced frontend state management using Svelte 4 stores and patterns.
- Optimized performance and resource usage.

### Removed
- Legacy components and redundant files.
- Build artifacts and temporary files.
- Duplicate sensor implementations.
- Obsolete launcher scripts.
- Unused dependencies and configurations.
- Development-only files from production build.
- All Svelte 5 specific syntax and documentation references.

### Fixed
- WebSocket connection stability issues.
- Memory leaks in sensor monitoring.
- Cross-platform compatibility problems.
- Security vulnerabilities in dependencies.
- Ensured all Svelte code is Svelte 4 compliant.

### Security
- Added input validation and sanitization.
- Implemented CORS protection.
- Added security headers.
- Non-root Docker container execution.
- Dependency vulnerability scanning.

## [1.0.0] - 2023-XX-XX (Assumed previous version)

### Added
- Initial release with basic hardware monitoring.
- Svelte frontend with widget system (initially might have had Svelte 5 experiments).
- Python backend with FastAPI.
- LibreHardwareMonitor integration.
- Basic WebSocket communication.
- Windows launcher scripts.
