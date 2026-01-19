# Kongtze Project

## Overview

Welcome to the Kongtze project!

## Prerequisites

- Node.js >= 18.0.0
- npm or yarn
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Kongtze
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

## BMad Method Integration

This project uses the BMad Method (Build More, Architect Dreams) for project architecture and scaffolding.

### Installing BMad Method

```bash
npx bmad-method@alpha install
```

Follow the interactive prompts to configure BMad for this project.

**Resources:**
- Documentation: http://docs.bmad-method.org/
- GitHub: https://github.com/bmad-code-org/BMAD-METHOD/
- YouTube: https://www.youtube.com/@BMadCode

## Getting Started

```bash
# Development mode with hot reload
npm run dev

# Production mode
npm start

# Run tests
npm test
```

## Project Structure

```
Kongtze/
├── .bmad/              # BMad Method configuration (generated)
├── .git/               # Git repository
├── .env                # Environment variables (not in git)
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── package.json        # Node.js dependencies and scripts
├── README.md           # This file
└── index.js            # Main entry point
```

## Development

### Adding Dependencies

```bash
npm install <package-name>
```

### Environment Variables

Copy `.env.example` to `.env` and configure your environment-specific values.

## Contributing

1. Create a feature branch
2. Make your changes
3. Commit with descriptive messages
4. Push and create a pull request

## License

ISC

## Author

frankhu <frank@bytetradelab.io>

---

Built with ❤️ using BMad Method
