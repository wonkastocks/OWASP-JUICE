# Journal App

A beautiful, clean, and simple journaling application built with Next.js, TypeScript, and Tailwind CSS. Features a markdown editor for rich text formatting and local storage for data persistence.

## Features

- 📝 **Markdown Editor**: Write your journal entries with full markdown support
- 💾 **Local Storage**: All entries are saved locally in your browser
- 🎨 **Beautiful UI**: Clean and minimal design with dark mode support
- ⚡ **Auto-save**: Your entries are automatically saved as you type
- 📱 **Responsive**: Works great on desktop and mobile devices
- 🔍 **Entry List**: Easy navigation through all your journal entries
- 🗑️ **Delete Entries**: Remove entries you no longer need

## Tech Stack

- **Next.js 15** - React framework for production
- **TypeScript** - Type-safe development
- **Tailwind CSS v3** - Utility-first CSS framework
- **SimpleMDE** - Markdown editor
- **React Markdown** - Markdown rendering

## Getting Started

### Prerequisites

- Node.js 18+ installed on your machine
- npm or yarn package manager

### Installation

1. Clone the repository or navigate to the project directory:
```bash
cd journal-app
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the app.

## Usage

1. **Create a New Entry**: Click the "New Entry" button in the sidebar
2. **Edit Entry Title**: Click on the title at the top to edit it
3. **Write Content**: Use the markdown editor to write your journal entry
4. **Format Text**: Use the toolbar buttons or markdown syntax for formatting
5. **Auto-save**: Your changes are automatically saved as you type
6. **Switch Entries**: Click on any entry in the sidebar to view/edit it
7. **Delete Entry**: Hover over an entry and click the delete icon

## Keyboard Shortcuts

The markdown editor supports standard markdown shortcuts:
- `**bold**` for **bold text**
- `*italic*` for *italic text*
- `# Heading` for headings
- `- List item` for bullet points
- `1. Item` for numbered lists
- And many more!

## Data Storage

All journal entries are stored in your browser's local storage. This means:
- ✅ Your data stays private and never leaves your device
- ✅ No account or login required
- ✅ Works offline
- ⚠️ Data is tied to your browser - clearing browser data will delete your entries
- ⚠️ Entries are not synced across devices

## Project Structure

```
journal-app/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Main page component
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   ├── Sidebar.tsx      # Sidebar with entry list
│   │   └── Editor.tsx       # Markdown editor
│   ├── lib/
│   │   └── storage.ts       # Local storage utilities
│   └── types/
│       └── journal.ts       # TypeScript types
├── public/                  # Static files
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.ts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Customization

### Changing Colors

Edit the Tailwind configuration in `tailwind.config.ts` to customize colors.

### Modifying Editor

The markdown editor options can be customized in `src/components/Editor.tsx` in the `editorOptions` object.

### Storage Location

To change where data is stored, modify the `STORAGE_KEY` constant in `src/lib/storage.ts`.

## Future Enhancements

Potential features to add:
- Export entries to PDF or markdown files
- Search functionality
- Tags and categories
- Cloud sync option
- Themes and customization
- Rich media embedding

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Support

If you encounter any issues or have questions, please open an issue on the project repository.
