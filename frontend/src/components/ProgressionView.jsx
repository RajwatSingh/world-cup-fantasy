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
  const [roundFilter, setRoundFilter] = useState(null)

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

  const allRounds = useMemo(() => {
    if (!data) return []
    const roundSet = new Set()
    Object.values(data).forEach((e) => e.rounds.forEach((r) => roundSet.add(r)))
    return [...roundSet].sort((a, b) => a - b)
  }, [data])

  useEffect(() => {
    if (allRounds.length && (roundFilter === null || !allRounds.includes(roundFilter))) {
      setRoundFilter(allRounds[allRounds.length - 1])
    }
  }, [allRounds])

  const roundRows = useMemo(() => {
    if (!data || roundFilter === null) return null
    return allManagers
      .map((m) => {
        const entry = data[m]
        const idx = entry.rounds.indexOf(roundFilter)
        if (idx === -1) return null
        const cumulative = entry.points[idx]
        const prevCumulative = idx > 0 ? entry.points[idx - 1] : 0
        const roundPoints =
          cumulative == null || prevCumulative == null ? null : cumulative - prevCumulative
        return { manager: m, roundPoints, cumulative, rank: entry.ranks[idx] }
      })
      .filter(Boolean)
      .sort((a, b) => (b.roundPoints ?? -Infinity) - (a.roundPoints ?? -Infinity))
  }, [data, allManagers, roundFilter])

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

      {allRounds.length > 0 && (
        <div className="card" style={{ marginBottom: 20 }}>
          <div className="controls" style={{ marginBottom: 12 }}>
            <label>
              Round
              <select
                value={roundFilter ?? ''}
                onChange={(e) => setRoundFilter(Number(e.target.value))}
              >
                {allRounds.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </label>
          </div>
          {roundRows && roundRows.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Manager</th>
                  <th className="num">Points this round</th>
                  <th className="num">Overall points</th>
                  <th className="num">Rank</th>
                </tr>
              </thead>
              <tbody>
                {roundRows.map((r) => (
                  <tr key={r.manager}>
                    <td>{r.manager}</td>
                    <td className="num">{r.roundPoints ?? '—'}</td>
                    <td className="num">{r.cumulative ?? '—'}</td>
                    <td className="num">{r.rank ?? '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="state-msg">No data for this round.</p>
          )}
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
