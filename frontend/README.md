# Frontend - AI Stamp Detector UI

Modern React web interface for the AI Stamp Detector application, built with TypeScript, Vite, and Tailwind CSS.

## Features

- **Drag & Drop Upload** - Intuitive file upload with drag-and-drop support
- **PDF Processing** - Upload PDF documents for stamp detection
- **Real-time Results** - Instant display of detection results
- **Visual Annotations** - View annotated images with detected stamps highlighted
- **Responsive Design** - Modern UI with Tailwind CSS styling

## Tech Stack

- **React 19.2.0** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite 7.2.4** - Build tool and dev server
- **Tailwind CSS 4** - Utility-first CSS framework
- **React Icons** - Icon library

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Dashboard/
│   │       ├── Dashboard.tsx      # Main dashboard component
│   │       ├── Header.tsx         # Application header
│   │       ├── Description.tsx    # Feature showcase section
│   │       ├── FileUpload.tsx     # File upload interface with detection results
│   │       └── Box.tsx            # UI box component
│   ├── App.tsx                    # Main application component
│   ├── App.css                    # Application styles
│   ├── main.tsx                   # Entry point
│   └── index.css                  # Global styles
├── package.json                   # Dependencies and scripts
├── vite.config.ts                 # Vite configuration
├── tailwind.config.js             # Tailwind CSS configuration
├── tsconfig.json                  # TypeScript configuration
└── eslint.config.js               # ESLint configuration
```

## Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

The development server will start at `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build optimized production bundle
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint for code quality checks

## Configuration

### API Endpoint

The frontend connects to the backend API at `http://localhost:5000`. To change this, update the `API_URL` constant in `src/components/Dashboard/FileUpload.tsx`.

### File Upload Settings

- **Accepted formats**: PDF (`.pdf`)
- **Maximum file size**: 50MB
- **Validation**: File extension, MIME type, and size checks

## Build for Production

```bash
npm run build
```

Output files will be generated in the `dist/` directory.

## Notes

- Ensure the backend server is running before using the application
- CORS is enabled on the backend for frontend integration
- The application requires a modern browser with ES6+ support
