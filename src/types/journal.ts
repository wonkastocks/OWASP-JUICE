export interface JournalEntry {
  id: string;
  title: string;
  content: string;
  createdAt: string;
  updatedAt: string;
}

export interface JournalState {
  entries: JournalEntry[];
  currentEntryId: string | null;
}
