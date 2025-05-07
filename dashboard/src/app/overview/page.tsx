"use client"

import React, { useEffect, useState } from "react"
import { motion } from "framer-motion"
import Link from "next/link"

type Player = {
  id: number
  track_id: number
  overall: number
  shooting: number
  passing: number
}

export default function Overview() {
  const [players, setPlayers] = useState<Player[]>([])
  const [loading, setLoading] = useState(true)

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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white">
        <p className="text-xl">Loading...</p>
      </div>
    )
  }

  // Derive top players
  const topRated   = players.slice(0, 3)
  const topScorers = [...players].sort((a,b) => b.shooting - a.shooting).slice(0, 3)
  const topPassers = [...players].sort((a,b) => b.passing - a.passing).slice(0, 3)

  // Render a single "category card"
  const renderCard = (title: string, list: Player[]) => (
    <motion.section
      whileHover={{ scale: 1.03, y: -4 }}
      transition={{ type: "spring", stiffness: 300 }}
      className="bg-gradient-to-br from-purple-700 to-indigo-700 rounded-2xl p-6 shadow-2xl text-white"
    >
      <h3 className="text-2xl font-extrabold mb-5 bg-clip-text text-transparent bg-gradient-to-r from-yellow-300 to-pink-400">
        {title}
      </h3>
      <div className="space-y-4">
        {list.map((p) => (
          <div
            key={p.id}
            className="flex justify-between items-center p-3 bg-gray-800 rounded-lg"
          >
            <span className="font-medium">Player {p.id}</span>
            <span className="text-lg font-bold">
              {title === "Top Rated" ? p.overall : title === "Top Scorers" ? p.shooting : p.passing}
            </span>
          </div>
        ))}
      </div>
    </motion.section>
  )

  return (
    // Fade-in for the entire page
    <motion.main
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-12 space-y-12"
    >
      <Link href="/" className="text-sm font-semibold text-gray-400 hover:text-white transition">
        &larr; Back to Home
      </Link>

      {/* Heading also animates (fade + slide up) */}
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="text-4xl font-extrabold text-center bg-clip-text text-transparent bg-gradient-to-r from-green-300 to-blue-500"
      >
        Overview
      </motion.h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {renderCard("Top Rated", topRated)}
        {renderCard("Top Scorers", topScorers)}
        {renderCard("Top Passers", topPassers)}
      </div>
    </motion.main>
  )
}