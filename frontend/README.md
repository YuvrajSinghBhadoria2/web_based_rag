# RAG System Frontend

React + TypeScript frontend for the Production-Grade RAG System.

## Tech Stack

- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **HTTP Client**: Axios
- **File Upload**: react-dropzone
- **Icons**: lucide-react
- **Notifications**: react-hot-toast

## Project Structure

```
src/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── MainContent.tsx
│   ├── documents/
│   │   ├── FileUpload.tsx
│   │   ├── DocumentList.tsx
│   │   └── DocumentCard.tsx
│   ├── query/
│   │   ├── QueryInput.tsx
│   │   └── ModeSelector.tsx
│   ├── results/
│   │   ├── ResultsDisplay.tsx
│   │   ├── AnswerCard.tsx
│   │   ├── ConfidenceIndicator.tsx
│   │   ├── SourcesList.tsx
│   │   └── SourceCard.tsx
│   ├── common/
│   │   └── EmptyState.tsx
│   └── settings/
│       └── SettingsModal.tsx
├── services/
│   └── api.ts
├── hooks/
├── context/
│   └── AppContext.tsx
├── types/
│   └── index.ts
├── App.tsx
└── index.tsx
```

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Configuration

Copy `.env.example` to `.env` and configure:

```
VITE_API_URL=http://localhost:8000/api/v1
```

## Features

- PDF document upload with drag-and-drop
- Document management (list, select, delete)
- Multiple query modes (Web, PDF, Hybrid, Restricted)
- Real-time confidence scoring
- Source citations and attribution
- Dark/light theme
- Responsive design
- Keyboard shortcuts (Enter to submit)
