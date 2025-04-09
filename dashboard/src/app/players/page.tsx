"use client"

import React, { useEffect, useState } from "react"
import { motion } from "framer-motion"
import Link from "next/link"

type Player = {
  id: number
  track_id: number
  pace: number
  shooting: number
  passing: number
  dribbling: number
  defending: number
  physical: number
  overall: number
  value: number
}

export default function PlayersPage() {
  const [players, setPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(true)

  // Client-side data fetch in useEffect
  useEffect(() => {
    async function fetchPlayers() {
      try {
        const res = await fetch("http://localhost:8000/api/players", { cache: "no-store" })
        if (!res.ok) throw new Error("Failed to fetch players")
        const data: Player[] = await res.json()
        setPlayers(data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchPlayers()
  }, [])

  // Show loading state until data arrives
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
        <p className="text-xl">Loading...</p>
      </div>
    )
  }

  // Render once data is loaded
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white px-4 sm:px-6 lg:px-8 py-10">
      <div className="mx-auto max-w-screen-2xl">
        {/* Animated heading with a bottom margin for spacing */}
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-4xl font-extrabold text-center bg-clip-text text-transparent 
                     bg-gradient-to-r from-green-300 to-blue-500 mb-8"
        >
          All Players
        </motion.h1>

        <div className="overflow-x-auto">
          <table className="w-full table-auto bg-gradient-to-r from-gray-800 to-gray-700 rounded-lg shadow-2xl border border-gray-700">
            <thead className="bg-gradient-to-r from-indigo-600 to-purple-600">
              <tr>
                {[
                  "ID",
                  "Overall",
                  "Value (SAR)",
                  "Pace",
                  "Shooting",
                  "Passing",
                  "Dribbling",
                  "Defending",
                  "Physical"
                ].map((col) => (
                  <th
                    key={col}
                    className="px-6 py-4 text-left text-lg font-bold uppercase tracking-wider"
                  >
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {players.map((p) => (
                <tr
                  key={p.id}
                  className="border-b border-gray-700 hover:bg-gray-700 transform hover:scale-105 transition-all duration-300"
                >
                  <td className="px-6 py-4">
                    <Link href={`/players/${p.id}`} className="hover:underline text-green-300">
                      Player {p.id}
                    </Link>
                  </td>
                  <td className="px-6 py-4">{p.overall}</td>
                  <td className="px-6 py-4">${p.value.toLocaleString()}</td>
                  <td className="px-6 py-4">{p.pace}</td>
                  <td className="px-6 py-4">{p.shooting}</td>
                  <td className="px-6 py-4">{p.passing}</td>
                  <td className="px-6 py-4">{p.dribbling}</td>
                  <td className="px-6 py-4">{p.defending}</td>
                  <td className="px-6 py-4">{p.physical}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  )
}
