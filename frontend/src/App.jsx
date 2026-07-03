import { useState } from 'react'
import TeamsView from './components/TeamsView.jsx'
import PlayersView from './components/PlayersView.jsx'
import ProgressionView from './components/ProgressionView.jsx'
import './App.css'

const TABS = [
  { id: 'progression', label: 'League Progression', Component: ProgressionView },
  { id: 'players', label: 'Players', Component: PlayersView },
  { id: 'teams', label: 'Teams', Component: TeamsView },
]

function App() {
  const [activeTab, setActiveTab] = useState(TABS[0].id)
  const Active = TABS.find((t) => t.id === activeTab).Component

  return (
    <div className="app">
      <header className="app-header">
        <h1>World Fantasy</h1>
        <nav className="tabs" role="tablist">
          {TABS.map((t) => (
            <button
              key={t.id}
              role="tab"
              aria-selected={activeTab === t.id}
              className={`tab ${activeTab === t.id ? 'active' : ''}`}
              onClick={() => setActiveTab(t.id)}
            >
              {t.label}
            </button>
          ))}
        </nav>
      </header>
      <main>
        <Active />
      </main>
    </div>
  )
}

export default App
