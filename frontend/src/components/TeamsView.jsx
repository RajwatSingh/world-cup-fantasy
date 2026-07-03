import { useEffect, useState } from 'react'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts'
import { getTeams } from '../api.js'

export default function TeamsView() {
  const [teams, setTeams] = useState(null)
  const [error, setError] = useState(null)
  const [minStrength, setMinStrength] = useState(0)

  useEffect(() => {
    let cancelled = false
    setError(null)
    getTeams(minStrength)
      .then((data) => {
        if (!cancelled) setTeams(data)
      })
      .catch((err) => {
        if (!cancelled) setError(err.message)
      })
    return () => {
      cancelled = true
    }
  }, [minStrength])

  const rows = teams
    ? Object.entries(teams)
        .map(([team, strength]) => ({ team, strength }))
        .sort((a, b) => b.strength - a.strength)
    : null

  return (
    <div className="panel">
      <div className="controls">
        <label>
          Min strength
          <input
            type="number"
            step="0.1"
            min="0"
            value={minStrength}
            onChange={(e) => setMinStrength(Number(e.target.value) || 0)}
            style={{ width: 70 }}
          />
        </label>
      </div>

      {error && <p className="state-msg error">Failed to load teams: {error}</p>}
      {!error && !rows && <p className="state-msg">Loading teams…</p>}

      {rows && rows.length === 0 && (
        <p className="state-msg">No teams at or above that strength.</p>
      )}

      {rows && rows.length > 0 && (
        <div className="card">
          <ResponsiveContainer width="100%" height={Math.max(320, rows.length * 22)}>
            <BarChart data={rows} layout="vertical" margin={{ left: 24 }}>
              <CartesianGrid horizontal={false} stroke="var(--border)" />
              <XAxis type="number" tick={{ fontSize: 12, fill: 'var(--text-muted)' }} />
              <YAxis
                type="category"
                dataKey="team"
                width={110}
                interval={0}
                tick={{ fontSize: 12, fill: 'var(--text-secondary)' }}
              />
              <Tooltip
                contentStyle={{
                  background: 'var(--surface-1)',
                  border: '1px solid var(--border)',
                  borderRadius: 6,
                  fontSize: 13,
                }}
                cursor={{ fill: 'color-mix(in srgb, var(--text-primary) 5%, transparent)' }}
              />
              <Bar dataKey="strength" fill="var(--series-1)" radius={[0, 4, 4, 0]} maxBarSize={16} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
