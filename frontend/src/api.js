async function getJSON(url) {
  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`${url} failed: ${res.status}`)
  }
  return res.json()
}

export function getTeams(minStrength = 0) {
  return getJSON(`/api/teams?min_strength=${minStrength}`)
}

export function getPlayers(position = '') {
  const qs = position ? `?position=${encodeURIComponent(position)}` : ''
  return getJSON(`/api/players${qs}`)
}

export function getRanks(players = [], round = 4) {
  const params = new URLSearchParams({ round })
  if (players.length) params.set('players', players.join(','))
  return getJSON(`/api/ranks?${params.toString()}`)
}
