'use client';

import { JournalEntry } from '@/types/journal';
import { formatDate } from '@/lib/storage';

interface SidebarProps {
  entries: JournalEntry[];
  currentEntryId: string | null;
  onSelectEntry: (id: string) => void;
  onNewEntry: () => void;
  onDeleteEntry: (id: string) => void;
}

export default function Sidebar({
  entries,
  currentEntryId,
  onSelectEntry,
  onNewEntry,
  onDeleteEntry,
}: SidebarProps) {
  const sortedEntries = [...entries].sort(
    (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
  );

  return (
    <div className="w-80 bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col h-screen">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-800">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Journal</h1>
        <button
          onClick={onNewEntry}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          New Entry
        </button>
      </div>

      {/* Entries List */}
      <div className="flex-1 overflow-y-auto">
        {sortedEntries.length === 0 ? (
          <div className="p-6 text-center text-gray-500 dark:text-gray-400">
            <p className="text-sm">No entries yet.</p>
            <p className="text-sm mt-1">Click "New Entry" to start writing!</p>
          </div>
        ) : (
          <div className="p-3">
            {sortedEntries.map((entry) => (
              <div
                key={entry.id}
                className={`group relative p-4 mb-2 rounded-lg cursor-pointer transition-all duration-200 ${
                  currentEntryId === entry.id
                    ? 'bg-blue-100 dark:bg-blue-900/30 border-l-4 border-blue-600'
                    : 'bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 border-l-4 border-transparent'
                }`}
                onClick={() => onSelectEntry(entry.id)}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-900 dark:text-white truncate">
                      {entry.title || 'Untitled'}
                    </h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {formatDate(entry.updatedAt)}
                    </p>
                    {entry.content && (
                      <p className="text-sm text-gray-600 dark:text-gray-300 mt-2 line-clamp-2">
                        {entry.content.substring(0, 100)}
                      </p>
                    )}
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm('Are you sure you want to delete this entry?')) {
                        onDeleteEntry(entry.id);
                      }
                    }}
                    className="opacity-0 group-hover:opacity-100 transition-opacity p-1.5 hover:bg-red-100 dark:hover:bg-red-900/30 rounded"
                    title="Delete entry"
                  >
                    <svg
                      className="w-4 h-4 text-red-600 dark:text-red-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-800 text-center">
        <p className="text-xs text-gray-500 dark:text-gray-400">
          {entries.length} {entries.length === 1 ? 'entry' : 'entries'}
        </p>
      </div>
    </div>
  );
}
