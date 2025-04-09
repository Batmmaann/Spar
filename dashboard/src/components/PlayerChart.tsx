"use client"

import React from "react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts"

export interface Player {
  id: number
  pace: number
  shooting: number
  passing: number
  dribbling: number
  defending: number
  physical: number
  overall: number
  value: number
}

interface Props {
  player: Player
}

export default function PlayerChart({ player }: Props) {
  const data = [
    { name: "Overall", value: player.overall },
    { name: "Pace", value: player.pace },
    { name: "Shooting", value: player.shooting },
    { name: "Passing", value: player.passing },
    { name: "Dribbling", value: player.dribbling },
    { name: "Defending", value: player.defending },
    { name: "Physical", value: player.physical },
  ]

  return (
    <div className="w-full h-64 bg-gray-800 rounded-lg p-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="#ccc" />
          <YAxis stroke="#ccc" />
          <Tooltip formatter={value => value.toLocaleString()} />
          <Bar dataKey="value" fill="#10B981" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
