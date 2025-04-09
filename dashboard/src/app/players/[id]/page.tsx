"use client"

import React, { useEffect, useState } from "react"
import Link from "next/link"
import { motion } from "framer-motion"
import PlayerRadarChart, { Player } from "@/components/PlayerRadarChart"
import { useParams } from "next/navigation"

export default function PlayerPage() {
  const { id } = useParams()
  const [player, setPlayer] = useState<Player | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchPlayer() {
      try {
        const res = await fetch("http://localhost:8000/api/players", { cache: "no-store" })
        if (!res.ok) throw new Error("Failed to fetch players")
        const players: Player[] = await res.json()
        const found = players.find(p => p.id === Number(id)) ?? null
        setPlayer(found)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    if (id) fetchPlayer()
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white flex items-center justify-center">
        <p className="text-xl">Loading...</p>
      </div>
    )
  }

  if (!player) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white flex items-center justify-center">
        <p className="text-center text-red-400 mt-10">Player not found</p>
      </div>
    )
  }

  return (
    <motion.main
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-10"
    >
      <div className="max-w-2xl mx-auto bg-gray-800 rounded-2xl shadow-2xl p-8 space-y-8">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-4xl font-extrabold text-center bg-clip-text text-transparent bg-gradient-to-r from-green-300 to-blue-500"
        >
          Player {player.id}
        </motion.h1>
        
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-xl text-center"
        >
          Estimated Market Value:{" "}
          <span className="font-semibold text-green-300">
            ${player.value.toLocaleString()}
          </span>
        </motion.p>

        <PlayerRadarChart player={player} />
        
        <div className="text-center">
          <Link href="/players" className="text-sm font-semibold text-gray-400 hover:text-white transition">
            &larr; Back to Players
          </Link>
        </div>
      </div>
    </motion.main>
  )
}
