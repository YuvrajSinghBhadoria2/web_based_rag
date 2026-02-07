import { AppProvider } from './context/AppContext';
import { Header } from './components/layout/Header';
import { Sidebar } from './components/layout/Sidebar';
import { MainContent } from './components/layout/MainContent';
import { SettingsModal } from './components/settings/SettingsModal';

function App() {
  return (
    <AppProvider>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Header />
        <Sidebar />
        <MainContent />
        <SettingsModal />
      </div>
    </AppProvider>
  );
}

export default App;
