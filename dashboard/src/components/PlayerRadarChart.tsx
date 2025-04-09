"use client"

import React from "react"
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
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

export default function PlayerRadarChart({ player }: Props) {
  const data = [
    { attribute: "Overall", value: player.overall },
    { attribute: "Pace",    value: player.pace },
    { attribute: "Shooting",value: player.shooting },
    { attribute: "Passing", value: player.passing },
    { attribute: "Dribbling",value: player.dribbling },
    { attribute: "Defending",value: player.defending },
    { attribute: "Physical", value: player.physical },
  ]

  return (
    <div className="w-full h-64 bg-gray-800 rounded-lg p-4">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="attribute" stroke="#ccc" />
          <PolarRadiusAxis angle={30} domain={[0, 99]} />
          <Radar name="Stats" dataKey="value" fill="#10B981" fillOpacity={0.6} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
