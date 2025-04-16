import { create } from 'zustand';

// Define the state structure
interface AppState {
  // Example state:
  // currentUser: User | null;
  // Example action:
  // setCurrentUser: (user: User | null) => void;
}

// Create the store
const useAppStore = create<AppState>((set) => ({
  // Initial state
  // currentUser: null,
  // Actions
  // setCurrentUser: (user) => set({ currentUser: user }),
}));

export default useAppStore; 