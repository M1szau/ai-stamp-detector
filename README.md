# AI Stamp Detector

An automated tool for authenticating stamps using artificial intelligence. This project leverages machine learning to verify the authenticity of stamps in documents.

## Features

- **AI-Powered Authentication**: Uses advanced AI models to analyze and verify stamp authenticity
- **User-Friendly Interface**: Clean and intuitive web interface for easy stamp verification
- **PDF Support**: Upload and process PDF documents containing stamps
- **Real-Time Results**: Get instant verification results with detailed analysis

## Project Structure

```
ai-stamp-detector/
├── frontend/                 # React + TypeScript + Vite frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Box.tsx      # Reusable card component for displaying feature information
│   │   │   └── Dashboard/
│   │   │       ├── Header.tsx          # Application header
│   │   │       ├── Description.tsx     # "How it works" section with feature cards
│   │   │       └── FileUpload.tsx      # File upload interface
│   │   ├── App.tsx          # Main application component
│   │   ├── main.tsx         # Entry point
│   │   └── assets/          # Static assets
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   ├── postcss.config.js    # PostCSS configuration
│   └── tsconfig.json
├── backend/                  # Backend API (to be implemented)
├── docs/                     # Project documentation
└── README.md                # This file
```

## Tech Stack

### Frontend
- **React 19.2.0** - JavaScript library for building user interfaces
- **TypeScript** - JavaScript with static typing
- **Vite 7.2.4** - Fast frontend build tool and development server
- **Tailwind CSS** - Utility-first CSS framework for styling
- **React Icons** - Icon library with popular icon sets

### Backend
- (To be implemented)

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd ai-stamp-detector
```

### 2. Install frontend dependencies
```bash
cd frontend
npm install
```

## Running the Project

### Development Mode

1. Start the development server:
```bash
cd frontend
npm run dev
```

2. Open your browser and navigate to:
```
http://localhost:5173/
```

The application will automatically reload when you make changes to the code.

### Build for Production

```bash
cd frontend
npm run build
```

The optimized build will be generated in the `frontend/dist/` directory.

### Preview Production Build

```bash
cd frontend
npm run preview
```

## Features Overview

### How It Works

The application provides three main steps:

1. **Upload Image** - Users can upload PDF documents containing stamps by dragging and dropping or clicking to browse
2. **AI Analysis** - The artificial intelligence analyzes the stamp authenticity using advanced algorithms
3. **Get Results** - Users receive instant verification results with detailed analysis

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint to check code quality

### Project Structure

The frontend is organized with a component-based architecture:
- **Box Component** - Reusable card component that displays feature information with customizable icons and colors
- **Header** - Application header with branding
- **Description** - Section showcasing the three-step process with colored icon cards
- **FileUpload** - Drag-and-drop file upload interface

## Component Props

### Box Component
```tsx
interface BoxProps {
  icon: ReactNode;           // React icon component
  title: string;             // Card title
  description: string;       // Card description
  iconColor: string;         // Tailwind color class (e.g., "bg-blue-400")
}
```

## Styling

This project uses **Tailwind CSS** for styling. All styles are utility-based using Tailwind classes.

Key Tailwind configurations:
- Custom content paths configured in `tailwind.config.js`
- PostCSS integration via `postcss.config.js`
- Responsive design support
- Color palette: Blue, Violet, and Green for primary interactive elements

## Future Enhancements

- Backend API implementation for AI model integration
- User authentication and account management
- History of uploaded documents and verification results
- Advanced filtering and search capabilities
- Batch processing for multiple documents
- Export verification reports

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is part of an academic AI project. Please refer to your institution's policies regarding code sharing and distribution.

## Contact & Support

For questions or issues, please open an issue on the project repository.

---

**Last Updated**: December 17, 2025
