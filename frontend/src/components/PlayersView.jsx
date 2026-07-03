import { useEffect, useMemo, useState } from 'react'
import { getPlayers } from '../api.js'

const POSITIONS = ['', 'GK', 'DEF', 'MID', 'FWD']
const COLUMNS = [
  { key: 'name', label: 'Player', num: false },
  { key: 'team', label: 'Team', num: false },
  { key: 'position', label: 'Pos', num: false },
  { key: 'opponent', label: 'Opponent', num: false },
  { key: 'score', label: 'Score', num: true },
  { key: 'selected', label: 'Selected %', num: true },
  { key: 'goals_scored', label: 'Goals', num: true },
  { key: 'shots', label: 'Shots', num: true },
  { key: 'minutes_played', label: 'Mins', num: true },
]

export default function PlayersView() {
  const [players, setPlayers] = useState(null)
  const [error, setError] = useState(null)
  const [position, setPosition] = useState('')
  const [sortKey, setSortKey] = useState('score')
  const [sortDir, setSortDir] = useState('desc')

  useEffect(() => {
    let cancelled = false
    setError(null)
    getPlayers(position)
      .then((data) => {
        if (!cancelled) setPlayers(data)
      })
      .catch((err) => {
        if (!cancelled) setError(err.message)
      })
    return () => {
      cancelled = true
    }
  }, [position])

  const rows = useMemo(() => {
    if (!players) return null
    const arr = Object.entries(players).map(([name, info]) => ({ name, ...info }))
    arr.sort((a, b) => {
      const av = a[sortKey]
      const bv = b[sortKey]
      const cmp =
        typeof av === 'number' && typeof bv === 'number'
          ? av - bv
          : String(av ?? '').localeCompare(String(bv ?? ''))
      return sortDir === 'asc' ? cmp : -cmp
    })
    return arr
  }, [players, sortKey, sortDir])

  function toggleSort(key) {
    if (key === sortKey) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortKey(key)
      setSortDir('desc')
    }
  }

  return (
    <div className="panel">
      <div className="controls">
        <label>
          Position
          <select value={position} onChange={(e) => setPosition(e.target.value)}>
            {POSITIONS.map((p) => (
              <option key={p} value={p}>
                {p || 'All'}
              </option>
            ))}
          </select>
        </label>
      </div>

      {error && <p className="state-msg error">Failed to load players: {error}</p>}
      {!error && !rows && <p className="state-msg">Loading players…</p>}
      {rows && rows.length === 0 && <p className="state-msg">No players found.</p>}

      {rows && rows.length > 0 && (
        <div className="card" style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                {COLUMNS.map((col) => (
                  <th
                    key={col.key}
                    className={`sortable ${col.num ? 'num' : ''}`}
                    onClick={() => toggleSort(col.key)}
                  >
                    {col.label}
                    {sortKey === col.key ? (sortDir === 'asc' ? ' ▲' : ' ▼') : ''}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.name}>
                  {COLUMNS.map((col) => (
                    <td key={col.key} className={col.num ? 'num' : ''}>
                      {col.key === 'score' && typeof r.score === 'number'
                        ? r.score.toFixed(2)
                        : r[col.key]}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
