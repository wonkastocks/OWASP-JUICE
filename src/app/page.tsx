'use client';

import { useEffect, useState, useCallback, useMemo } from 'react';
import Sidebar from '@/components/Sidebar';
import Editor from '@/components/Editor';
import { JournalEntry } from '@/types/journal';
import {
  loadEntries,
  saveEntries,
  createEntry,
  updateEntry as updateEntryUtil,
  deleteEntry as deleteEntryUtil,
} from '@/lib/storage';

export default function Home() {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [currentEntryId, setCurrentEntryId] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  // Load entries on mount
  useEffect(() => {
    setMounted(true);
    const loadedEntries = loadEntries();
    setEntries(loadedEntries);

    // Select the most recent entry if available
    if (loadedEntries.length > 0) {
      const mostRecent = loadedEntries.reduce((latest, entry) =>
        new Date(entry.updatedAt) > new Date(latest.updatedAt) ? entry : latest
      );
      setCurrentEntryId(mostRecent.id);
    }
  }, []);

  // Save entries whenever they change
  useEffect(() => {
    if (mounted) {
      saveEntries(entries);
    }
  }, [entries, mounted]);

  const handleNewEntry = useCallback(() => {
    const newEntry = createEntry();
    setEntries((prev) => [newEntry, ...prev]);
    setCurrentEntryId(newEntry.id);
  }, []);

  const handleSelectEntry = useCallback((id: string) => {
    setCurrentEntryId(id);
  }, []);

  const handleUpdateEntry = useCallback((id: string, updates: Partial<JournalEntry>) => {
    setEntries((prev) => updateEntryUtil(prev, id, updates));
  }, []);

  const handleDeleteEntry = useCallback((id: string) => {
    setEntries((prev) => {
      const updatedEntries = deleteEntryUtil(prev, id);
      return updatedEntries;
    });

    // If we deleted the current entry, select another one
    setCurrentEntryId((prevId) => {
      if (prevId === id) {
        const updatedEntries = deleteEntryUtil(entries, id);
        return updatedEntries.length > 0 ? updatedEntries[0].id : null;
      }
      return prevId;
    });
  }, [entries]);

  const currentEntry = useMemo(
    () => entries.find((e) => e.id === currentEntryId) || null,
    [entries, currentEntryId]
  );

  if (!mounted) {
    return (
      <div className="flex items-center justify-center h-screen bg-white dark:bg-gray-950">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar
        entries={entries}
        currentEntryId={currentEntryId}
        onSelectEntry={handleSelectEntry}
        onNewEntry={handleNewEntry}
        onDeleteEntry={handleDeleteEntry}
      />
      <Editor entry={currentEntry} onUpdateEntry={handleUpdateEntry} />
    </div>
  );
}
