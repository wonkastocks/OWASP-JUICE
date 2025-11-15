import { JournalEntry } from '@/types/journal';

const STORAGE_KEY = 'journal-entries';

export const loadEntries = (): JournalEntry[] => {
  if (typeof window === 'undefined') return [];

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];
    return JSON.parse(stored);
  } catch (error) {
    console.error('Error loading entries:', error);
    return [];
  }
};

export const saveEntries = (entries: JournalEntry[]): void => {
  if (typeof window === 'undefined') return;

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
  } catch (error) {
    console.error('Error saving entries:', error);
  }
};

export const createEntry = (title: string = 'Untitled Entry'): JournalEntry => {
  const now = new Date().toISOString();
  return {
    id: `entry-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
    title,
    content: '',
    createdAt: now,
    updatedAt: now,
  };
};

export const updateEntry = (
  entries: JournalEntry[],
  id: string,
  updates: Partial<JournalEntry>
): JournalEntry[] => {
  return entries.map((entry) =>
    entry.id === id
      ? { ...entry, ...updates, updatedAt: new Date().toISOString() }
      : entry
  );
};

export const deleteEntry = (entries: JournalEntry[], id: string): JournalEntry[] => {
  return entries.filter((entry) => entry.id !== id);
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) {
    return `Today at ${date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`;
  } else if (diffDays === 1) {
    return 'Yesterday';
  } else if (diffDays < 7) {
    return `${diffDays} days ago`;
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }
};
