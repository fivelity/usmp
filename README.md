# Ultimate Sensor Monitor

🎉 **Version 2.0.0 - Svelte 5 Migration Complete!** This major update brings a production-ready, secure, and highly optimized Ultimate Sensor Monitor with modern Svelte 5 Runes architecture. See the [Changelog](CHANGELOG.md) for full details.

✅ **Latest Achievement**: Successfully migrated to **Svelte 5** with Rune-based state management  
✅ **Build Status**: Zero errors, production ready  
✅ **Performance**: Enhanced with reactive `$state()`, `$derived()`, and `$effect()`  
✅ **Modern Patterns**: Component architecture using `$props()` and `{@render}` snippets  

A professional hardware monitoring dashboard built with Python (FastAPI) backend and cutting-edge Svelte 5 frontend, providing real-time system monitoring with customizable widgets and modern UI.

## 🚀 Features

- **Real-time Hardware Monitoring**: CPU, GPU, memory, temperatures, and more
- **Customizable Dashboard**: Drag-and-drop widgets with multiple gauge types
- **Professional UI**: Modern, responsive design with theme support
- **WebSocket Integration**: Live data updates without page refresh
- **Production Ready**: Docker support, CI/CD pipeline, and comprehensive testing
- **Cross-platform**: Windows, Linux, and macOS support
- **Svelte 5 Frontend**: Modern, reactive UI leveraging Svelte's powerful Svelte 5 Runes for state management and performance
- **Type-Safe Development**: Comprehensive TypeScript types and interfaces for robust development
- **Advanced State Management**: Efficient store system with undo/redo support and type-safe operations
- **Docker & CI/CD**: Easy deployment and continuous integration
- **Professional Windows Launchers**: Simplified startup for Windows users
- **Enhanced Security**: Robust measures for safe operation

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **FastAPI**: High-performance async web framework
- **Pydantic**: Data validation and serialization
- **WebSockets**: Real-time communication
- **LibreHardwareMonitor**: Hardware sensor integration
- **Structured Logging**: Production-grade logging system

### Frontend (Svelte 5/TypeScript)
- **Svelte 5 with Runes**: Latest reactive UI framework with `$state()`, `$derived()`, and `$effect()` for optimal performance
- **TypeScript**: Type-safe development with comprehensive type definitions
- **Tailwind CSS 3.x**: Utility-first styling with CSS-first configuration and theme support
- **Vite 5.x**: Lightning-fast build tool and development server
- **SvelteKit**: Full-stack framework with static site generation
- **WebSocket Client**: Robust real-time communication with automatic reconnection
- **Rune-based State Management**: Modern reactive stores with undo/redo support
- **Component Architecture**: Modern `$props()` destructuring and `{@render}` snippets
- **Theme System**: Dynamic theming with CSS variables and dark mode support

## 📋 Prerequisites

- **Python 3.9+** with pip
- **Node.js 18+** with npm (or pnpm, see [Setup Guide](docs/SETUP_GUIDE.md))
- **LibreHardwareMonitor** (Windows) or equivalent sensors (Linux/macOS)

## 🛠️ Quick Start

### Windows (Recommended)

1. **Clone the repository**
\`\`\`bash
git clone <repository-url>
cd UltimateSensorMonitor
\`\`\`

2. **Run the launcher**
\`\`\`bash
# Full launcher with validation
start_ultimon_full.bat

# Quick start (minimal validation)
start_ultimon_quick.bat
\`\`\`

3. **Create desktop shortcuts**
\`\`\`bash
create_executable_shortcut.bat
\`\`\`

### Manual Setup

Refer to the [Setup Guide](docs/SETUP_GUIDE.md) for detailed instructions.

1. **Clone the repository**
\`\`\`bash
git clone <repository-url>
cd UltimateSensorMonitor
\`\`\`

2. **Install Dependencies (Root Directory):**
\`\`\`bash
# From the UltimateSensorMonitor root directory
pnpm install
\`\`\`

#### Backend Setup
\`\`\`bash
cd server
# pip install -r requirements.txt (pnpm might handle this if configured, but typically Python deps are separate)
python -m app.main 
# Or: uvicorn app.main:app --reload --port 8000 (adjust port as needed)
\`\`\`

#### Frontend Setup
\`\`\`bash
cd client
pnpm dev     # or npm run dev
\`\`\`

## 🐳 Docker Deployment

Refer to the `docker-compose.yml` and `Dockerfile`s for details.
\`\`\`bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment (example, may need specific prod compose file)
# docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
\`\`\`

## 📖 Documentation

- [User Guide](docs/USER_GUIDE.md) - How to use the application
- [Developer Guide (Svelte 5)](docs/DEVELOPER_GUIDE.md) - Development setup, architecture, and Svelte 5 practices
- [API Documentation](docs/API_DOCUMENTATION.md) - Backend API reference
- [Custom Widget Development (Svelte 5)](docs/CUSTOM_WIDGET_DEVELOPMENT.md) - Creating custom widgets using Svelte 5
- [Svelte 5 Standards](docs/SVELTE_STANDARDS.md) - Coding standards for Svelte 5
- [Store System Guide](docs/STORE_SYSTEM.md) - Understanding the state management system
- [Theme System Guide](docs/THEME_SYSTEM.md) - Working with themes and color schemes
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

## 🔧 Configuration

### Environment Variables

Create `.env` files in the respective `client` and `server` directories. See `.env.example` files for templates.

**Client (`client/.env`)**
\`\`\`env
VITE_API_BASE_URL=http://localhost:8000
VITE_WEBSOCKET_URL=ws://localhost:8000/ws
# Adjust ports if your backend runs on different ones
\`\`\`

**Server (`server/.env`)**
\`\`\`env
DEBUG=true
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:5173"] # Adjust for your frontend URL
SENSOR_UPDATE_INTERVAL=1.0 # seconds
\`\`\`

## 🧪 Testing

\`\`\`bash
# Backend tests
cd server
pytest

# Frontend tests (using Vitest, example command)
cd client
pnpm test # or npm test

# E2E tests (if configured, e.g., with Playwright)
# cd client && pnpm test:e2e 
\`\`\`

## 📊 Monitoring Endpoints

- **Dashboard**: `http://localhost:5173` (default Vite dev server port)
- **API Server**: `http://localhost:8000` (default backend port)
- **API Documentation (Swagger UI)**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **WebSocket**: `ws://localhost:8000/ws`

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Ensure your code adheres to the [Svelte 5 Standards](docs/SVELTE_STANDARDS.md) and general project guidelines.
4. Commit your changes (`git commit -m 'Add amazing feature'`).
5. Push to the branch (`git push origin feature/amazing-feature`).
6. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 🆘 Support

- Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md).
- Review existing [GitHub Issues](../../issues) or open a new one.
- Consult the detailed [Documentation](docs/).

## 🙏 Acknowledgments

- [LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor) for hardware monitoring.
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework.
- [Svelte](https://svelte.dev/) (specifically Svelte 5) for the frontend framework.
- [Tailwind CSS](https://tailwindcss.com/) for styling.

---

**Ultimate Sensor Monitor** - Professional hardware monitoring made simple with Svelte 5 and Python.
