'use client';

import { useEffect, useRef, useState, memo, useMemo } from 'react';
import dynamic from 'next/dynamic';
import { JournalEntry } from '@/types/journal';

// Dynamically import SimpleMDE to avoid SSR issues
const SimpleMDE = dynamic(() => import('react-simplemde-editor'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-screen">
      <div className="text-gray-500">Loading editor...</div>
    </div>
  ),
});

interface EditorProps {
  entry: JournalEntry | null;
  onUpdateEntry: (id: string, updates: Partial<JournalEntry>) => void;
}

function Editor({ entry, onUpdateEntry }: EditorProps) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const titleInputRef = useRef<HTMLInputElement>(null);
  const hasAutoFocusedRef = useRef<string | null>(null);

  // Update local state when entry changes and focus title for new entries
  useEffect(() => {
    if (entry) {
      setTitle(entry.title);
      setContent(entry.content);

      // Auto-focus title if it's empty (new entry) and we haven't focused this entry yet
      if (!entry.title && titleInputRef.current && hasAutoFocusedRef.current !== entry.id) {
        hasAutoFocusedRef.current = entry.id;
        setTimeout(() => {
          titleInputRef.current?.focus();
        }, 100);
      }
    } else {
      setTitle('');
      setContent('');
      hasAutoFocusedRef.current = null;
    }
  }, [entry?.id]); // Only update when entry ID changes

  // Auto-save title with debounce
  useEffect(() => {
    if (!entry) return;
    if (title === entry.title) return; // Don't save if unchanged

    setIsSaving(true);
    const timer = setTimeout(() => {
      onUpdateEntry(entry.id, { title });
      setLastSaved(new Date());
      setIsSaving(false);
    }, 500);

    return () => {
      clearTimeout(timer);
      setIsSaving(false);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [title]);

  // Auto-save content with debounce
  useEffect(() => {
    if (!entry) return;
    if (content === entry.content) return; // Don't save if unchanged

    setIsSaving(true);
    const timer = setTimeout(() => {
      onUpdateEntry(entry.id, { content });
      setLastSaved(new Date());
      setIsSaving(false);
    }, 500);

    return () => {
      clearTimeout(timer);
      setIsSaving(false);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [content]);

  if (!entry) {
    return (
      <div className="flex-1 flex items-center justify-center bg-white dark:bg-gray-950">
        <div className="text-center">
          <svg
            className="w-16 h-16 text-gray-300 dark:text-gray-700 mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
            />
          </svg>
          <p className="text-gray-500 dark:text-gray-400 text-lg">
            Select an entry or create a new one to start writing
          </p>
        </div>
      </div>
    );
  }

  const editorOptions = useMemo(() => ({
    spellChecker: false,
    placeholder: 'Start writing your thoughts...',
    status: false,
    autofocus: false,
    toolbar: [
      'bold',
      'italic',
      'heading',
      '|',
      'quote',
      'unordered-list',
      'ordered-list',
      '|',
      'link',
      'image',
      '|',
      'preview',
      'side-by-side',
      'fullscreen',
      '|',
      'guide',
    ],
  }), []);

  return (
    <div className="flex-1 flex flex-col bg-white dark:bg-gray-950">
      {/* Title Input */}
      <div className="border-b border-gray-200 dark:border-gray-800 px-8 py-6">
        <input
          ref={titleInputRef}
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Click here to add a title..."
          className="w-full text-3xl font-bold bg-transparent border-2 border-transparent rounded-lg px-2 py-1 -mx-2 outline-none text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-600 hover:border-gray-200 dark:hover:border-gray-700 focus:border-blue-500 dark:focus:border-blue-500 focus:placeholder-gray-500 dark:focus:placeholder-gray-500 transition-colors"
        />
        <div className="flex items-center justify-between mt-3">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Last updated: {new Date(entry.updatedAt).toLocaleString()}
          </p>
          <div className="flex items-center gap-2">
            {isSaving ? (
              <span className="text-sm text-blue-600 dark:text-blue-400 flex items-center gap-1">
                <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Saving...
              </span>
            ) : lastSaved ? (
              <span className="text-sm text-green-600 dark:text-green-400 flex items-center gap-1">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Saved
              </span>
            ) : null}
          </div>
        </div>
      </div>

      {/* Markdown Editor */}
      <div className="flex-1 overflow-y-auto px-8 py-6">
        <SimpleMDE
          key={entry.id}
          value={content}
          onChange={setContent}
          options={editorOptions as any}
        />
      </div>
    </div>
  );
}

// Custom comparison function for React.memo
// Returns true if props are equal (skip re-render), false if different (re-render)
const arePropsEqual = (prevProps: EditorProps, nextProps: EditorProps) => {
  const prevEntryId = prevProps.entry?.id;
  const nextEntryId = nextProps.entry?.id;

  return (
    prevEntryId === nextEntryId &&
    prevProps.onUpdateEntry === nextProps.onUpdateEntry
  );
};

// Memoize the Editor component to prevent re-renders
const MemoizedEditor = memo(Editor, arePropsEqual);

export default MemoizedEditor;
