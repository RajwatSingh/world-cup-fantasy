import { useEffect, useMemo, useState } from 'react'
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts'
import { getRanks } from '../api.js'

const SERIES_COLORS = ['var(--series-1)', 'var(--series-2)', 'var(--series-3)', 'var(--series-4)']

function pivot(data, field) {
  const managers = Object.keys(data)
  const roundSet = new Set()
  managers.forEach((m) => data[m].rounds.forEach((r) => roundSet.add(r)))
  const rounds = [...roundSet].sort((a, b) => a - b)

  return rounds.map((round) => {
    const row = { round }
    managers.forEach((m) => {
      const idx = data[m].rounds.indexOf(round)
      row[m] = idx === -1 ? null : data[m][field][idx]
    })
    return row
  })
}

function Chart({ title, data, managers, colorFor, reversed }) {
  return (
    <div className="card">
      <h3 style={{ fontSize: 15, marginBottom: 12, color: 'var(--text-secondary)' }}>{title}</h3>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data} margin={{ left: 8, right: 16, top: 8 }}>
          <CartesianGrid stroke="var(--border)" vertical={false} />
          <XAxis
            dataKey="round"
            tick={{ fontSize: 12, fill: 'var(--text-muted)' }}
            label={{ value: 'Round', position: 'insideBottom', offset: -4, fontSize: 12, fill: 'var(--text-muted)' }}
          />
          <YAxis
            reversed={reversed}
            tick={{ fontSize: 12, fill: 'var(--text-muted)' }}
            width={40}
          />
          <Tooltip
            contentStyle={{
              background: 'var(--surface-1)',
              border: '1px solid var(--border)',
              borderRadius: 6,
              fontSize: 13,
            }}
          />
          <Legend wrapperStyle={{ fontSize: 13 }} />
          {managers.map((m) => (
            <Line
              key={m}
              type="monotone"
              dataKey={m}
              stroke={colorFor(m)}
              strokeWidth={2}
              dot={{ r: 3 }}
              connectNulls
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function ProgressionView() {
  const [round, setRound] = useState(4)
  const [playersInput, setPlayersInput] = useState('')
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [hidden, setHidden] = useState(new Set())

  function load() {
    const players = playersInput
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
    setLoading(true)
    setError(null)
    getRanks(players, round)
      .then((res) => setData(res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const allManagers = data ? Object.keys(data) : []
  const managers = allManagers.filter((m) => !hidden.has(m))
  const colorMap = useMemo(() => {
    const map = {}
    allManagers.forEach((m, i) => {
      map[m] = SERIES_COLORS[i % SERIES_COLORS.length]
    })
    return map
  }, [allManagers.join(',')])

  const rankData = data ? pivot(data, 'ranks') : null
  const pointsData = data ? pivot(data, 'points') : null

  function toggleManager(m) {
    setHidden((prev) => {
      const next = new Set(prev)
      if (next.has(m)) next.delete(m)
      else next.add(m)
      return next
    })
  }

  return (
    <div className="panel">
      <div className="controls">
        <label>
          Managers (comma-separated, blank = default)
          <input
            type="text"
            placeholder="ramborajwat, CHEKCHY"
            value={playersInput}
            onChange={(e) => setPlayersInput(e.target.value)}
            style={{ width: 260 }}
          />
        </label>
        <label>
          Through round
          <input
            type="number"
            min="1"
            value={round}
            onChange={(e) => setRound(Number(e.target.value) || 1)}
            style={{ width: 60 }}
          />
        </label>
        <button className="legend-toggle" onClick={load} disabled={loading}>
          {loading ? 'Loading…' : 'Reload'}
        </button>
      </div>

      {error && <p className="state-msg error">Failed to load progression: {error}</p>}
      {loading && !data && (
        <p className="state-msg">
          Loading live progression… this hits the FIFA API per round and can take a while.
        </p>
      )}

      {allManagers.length > 0 && (
        <div className="legend-toggles" style={{ marginBottom: 20 }}>
          {allManagers.map((m) => (
            <button
              key={m}
              className={`legend-toggle ${hidden.has(m) ? 'off' : ''}`}
              onClick={() => toggleManager(m)}
            >
              <span className="legend-swatch" style={{ background: colorMap[m] }} />
              {m}
            </button>
          ))}
        </div>
      )}

      {rankData && (
        <Chart
          title="Rank (lower is better)"
          data={rankData}
          managers={managers}
          colorFor={(m) => colorMap[m]}
          reversed
        />
      )}
      {pointsData && (
        <Chart
          title="Points"
          data={pointsData}
          managers={managers}
          colorFor={(m) => colorMap[m]}
        />
      )}
    </div>
  )
}
